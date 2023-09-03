import math
import flask
from flask import Flask
from flask import request
import json
import pickle
import requests as req
from urllib.parse import urlparse
#### Custom gateway to data management system
import pymongo
import os
import sys
import ast
from bson import json_util

app = Flask(__name__)
app.config["registry"] = pickle.loads(open("registry_FHIR.dict","rb").read())
app.config["PLATFORM-ID"] = os.environ["PLATFORM-ID"]
app.config["REQUEST-ID-LIST"] = []
app.config["REGISTRY-VERSION"]= "1"



# @app.route("/data")
# def hello_world():
#     return
@app.route("/platform_id",methods=['PUT'])
def modify_platform_id():
    print(request.headers)
    app.config["PLATFORM-ID"] = request.headers["platform-id"]
    rep = flask.Response(status=204)
    rep.set_data(app.config["PLATFORM-ID"])
    return rep
@app.route('/registry', methods=['POST'])
def overwrite_registry():
    # print(app.config["REGISTRY-VERSION"],file=sys.stderr)
    if request.headers["registry-version"] == app.config["REGISTRY-VERSION"]:
        return flask.Response(status=208)
    else:
        app.config["REGISTRY-VERSION"] = request.headers["registry-version"]
    data = request.get_json(force=True)
    # print(data,file=sys.stderr)
    with open("registry.dict", "wb") as fp:
        pickle.dump((data), fp)
        app.config["registry"] = data

    aux_header = dict(request.headers)
    # print(aux_header,file=sys.stderr)
    aux_header["Platform-Visited"]=aux_header["Platforms-Visited"] +","+app.config["PLATFORM-ID"]
    for platform_id in app.config["registry"]["platforms"][app.config["PLATFORM-ID"]]["links"]:
            # print(match,model,platform_list,file=sys.stderr)
        if platform_id not in request.headers["platforms-visited"] and platform_id != request.headers["platform-id"]:
            req.post(app.config["registry"]["platforms"][platform_id]["URL"][0]+"/registry", headers=aux_header,
                     data=json.dumps(data), timeout=5)
    return flask.Response(status=204)

@app.route('/registry', methods=['GET'])
def get_registry():
    print(flask.jsonify(open("registry.dict", "r").read()))
    return flask.jsonify(open("registry.dict","r").read())

# A voir plus tard si nécessaire
def operator_list_def(operator_var):

    import operator
    if app.config["PLATFORM-ID"]=="1":
        with open("operator_list_xml.dict","rb") as fp:

            return eval(pickle.load(fp)[operator_var])
    if app.config["PLATFORM-ID"]=="2" or app.config["PLATFORM-ID"]=="4" :
        with open("operator_list_mongo.dict","rb") as fp:

            return pickle.load(fp)[operator_var]
    if app.config["PLATFORM-ID"]=="3":
        with open("operator_list_sql.dict","rb") as fp:

            return pickle.load(fp)[operator_var]


def get_metadata(key, model, operator, operand, dicttoxml=None):
    '''
    Get metadata from request : gateway technical interoperability function
    :param key:
    :param model:
    :param operator:
    :param operand:
    :return: Results of request as list of objects
    '''

    if app.config["PLATFORM-ID"]=="1":
        import xml.etree.ElementTree as ET
        root = ET.parse("ODATIS/metadata.xml").getroot()
        # print(root)
        # # print(root)
        # print(root.findall(".//mri:southBoundLatitude"))
        aux_key = key.replace("@","")
        def walk_tree(key, root, operator, operand):
            bool = False
            if len(key.split(".")) > 1:
                aux = key.split(".")[1:]
            else:
                aux = key
            for i in root:
                # print(i.tag)
                # print(aux)
                # print(aux[:-1])
                if aux[0] in i.tag:
                    # print("TA GROSSE DARONNE")
                    # print(i.tag)
                    # print(aux)
                    print(key)
                    print(len(key.split(".")),file=sys.stderr)
                    if len(key.split(".")) == 3:
                        print(i.text,file=sys.stderr)
                        if operator(i.text, operand):
                            return True
                        else:
                            return False

                    bool = walk_tree(".".join(aux), i, operator, operand)
            if bool:
                return root
            else:
                return []
                # break
                # print(i)

        # print(root.tag)
        return str(ET.tostring(walk_tree(aux_key, root, operator_list_def(operator), operand)).decode("utf-8"))

# # AERIS
# def get_metadata(key,model,operator,operand):
#     '''
#     Get metadata from request : gateway technical interoperability function
#     :param key:
#     :param model:
#     :param operator:
#     :param operand:
#     :return: Results of request as list of objects
#     '''
#     # GET_METADATA: FUNCTION TO MODIFY BASED ON NEEDS

    if app.config["PLATFORM-ID"]=="2" or app.config["PLATFORM-ID"]=="4":
        if app.config["registry"]["models"][model]["keys"][key] == "integer":
            return json_util.dumps(list(pymongo.MongoClient("database_json:27017").AERIS.metadata.find(
                    {key: {operator_list_def(operator): float(operand)}}, {"_id": False})))
        else:
            return json_util.dumps(list(pymongo.MongoClient("database_json:27017").AERIS.metadata.find(
                            {key: {operator_list_def(operator): operand}}, {"_id": False})))
#
#
#
#
# # FHIR
    if app.config["PLATFORM-ID"]=="3":
        from MySQLdb import _mysql
        print("TA GROSSE DARONNE",file=sys.stderr)
        aux_key = key.replace(".","_")
        # print("SELECT * FROM Location-hl7east WHERE "+aux_key + operator_list_def(operator) + operand + " ;",file=sys.stderr)
        db = _mysql.connect("database_sql", database="FHIR")
        query =  db.query("SELECT * FROM Location_hl7east WHERE "+aux_key + operator_list_def(operator) + operand + " ;")
        print(query,file=sys.stderr)
        print("SELECT * FROM Location_hl7east WHERE "+aux_key + operator_list_def(operator) + operand + " ;",file=sys.stderr)
        if query is None:
            return []
        else:
            return query









@app.route('/request', methods=['GET'])
def request_metadata():

    '''
    Header variable doc :
    "initiator" : ID of the query initializer platform
    "model" : model requested
    "key" : key from the model requested
    "operator" : operator used for the request (see operator list)
    "value": value for the request
    :return:
    '''
    # print(request.headers)
    if "initiator" not in request.headers:
        return ("initiator header variable not defined (platform id that initiate the request), "
                "needed for request routage")
    if "key" not in request.headers:
        return "key from the model header variable not defined, needed for request and match finding"
    if "model" not in request.headers:
        return "model header variable not defined, needed for request and match finding"
    if "jump" not in request.headers:
        return "jump (inverse of time to live) header variable not defined ; needed for routing"
    if "platforms-visited" not in request.headers:
        return "platforms-visited header variable not defined ; needed for routing"
    if "operator" not in request.headers:
        return "operator header variable not defined ; needed for request"
    if "operand" not in request.headers:
        return "operand header variable not defined ; needed for request"
    if "request-id" not in request.headers:
        return "request-id header variable not defined; needed to avoid loop"
    # Platform id of the request creator
    if "platform-id" not in request.headers:
        return "platform-id header variable not defined; needed for routing"

    ret = []
    if request.headers["request-id"] in app.config["REQUEST-ID-LIST"]:
        return flask.Response(status=208)
    else:
        app.config["REQUEST-ID-LIST"].append(request.headers["request-id"])

    # print("GROSSE DARONNE",file=sys.stderr)
    ret.append( get_metadata(key = request.headers["key"], model = request.headers["model"],
                       operator = request.headers["operator"], operand = request.headers["operand"] ))

    # print("PETITE DARONNE",file=sys.stderr)


    matchs = []
    for match_id in app.config["registry"]["matchs"]:
        if  app.config["registry"]["matchs"][match_id]["keyA"] == request.headers["key"]:
            matchs.append((app.config["registry"]["matchs"][match_id]["keyB"],app.config["registry"]["matchs"][match_id]["modelB"],
                           app.config["registry"]["models"][app.config["registry"]["matchs"][match_id]["modelB"]]["platforms"]))
        if  app.config["registry"]["matchs"][match_id]["keyB"] == request.headers["key"]:
            matchs.append((app.config["registry"]["matchs"][match_id]["keyA"],app.config["registry"]["matchs"][match_id]["modelA"],
                           app.config["registry"]["models"][app.config["registry"]["matchs"][match_id]["modelA"]]["platforms"]))
    # print(matchs,file=sys.stderr)
    for match,model,platform_list in matchs:
        # print(platform_list, file=sys.stderr)
        # print( registry["platforms"][app.config.get("PLATFORM-ID")]["links"], file=sys.stderr)
        # print(request.headers["key"], file=sys.stderr)
        for platform in platform_list:
            if platform in app.config["registry"]["platforms"][app.config.get("PLATFORM-ID")]["links"]:

                if platform not in request.headers["platforms-visited"] and platform !=  request.headers["platform-id"]:
                    # print(match,model,platform_list,file=sys.stderr)
                    rep = req.get(app.config["registry"]["platforms"][platform]["URL"][0]+"/request", headers={"platforms-visited":
                                                                                 request.headers["platforms-visited"]+","
                                                                                 +app.config.get("PLATFORM-ID"),
                                                                                 "jump":str(int(request.headers["jump"])+1),
                                                                                 "key":match,
                                                                                 "model":model,
                                                                                 "operator":request.headers["operator"],
                                                                                "operand":request.headers["operand"],
                                                                                "platform-id":app.config["PLATFORM-ID"],
                                                                                 "initiator":request.headers["initiator"],
                                                                                "request-id":request.headers["request-id"]}
                                  , timeout=5)

                    if rep.status_code == 200:
                        # print(rep.content.decode("utf-8"),file=sys.stderr)
                        # print(type(rep.content.decode("utf-8")),file=sys.stderr)
                        # print(rep.content.decode("utf-8"), file=sys.stderr)
                        ret+= ast.literal_eval((rep.content.decode("utf-8")))

    # print(ret,file=sys.stderr)

    return flask.jsonify(ret)



def get_node_nearest_from_distribution():
    '''
    Calcul of best node to link to based on actual distribution of degree
    :param node:
    :return:
    '''
    print(app.config["registry"]["network"], file=sys.stderr)

    gamma=2.5
    node_degree = 2
    value_divkb= sys.float_info.max
    node_number = app.config["registry"]["network"]["node_number"]
    for index in range(len(degree_distrib:=app.config["registry"]["network"]["degrees_distribution"])-1):
        # If no node of degree X, it's not possible to connect a node to it
        if len(degree_distrib[index]) > 0:
            print(degree_distrib,file=sys.stderr)
            degree = index+2

            pn = ((len(degree_distrib[index]))-1)/node_number
            print(pn, file=sys.stderr)
            pn_one = ((len(degree_distrib[index+1]))+1)/node_number

            # based on the lim x log(x) = 0 for x -> 0
            if pn == 0:
                part_one = 0
            else:
                part_one = pn * math.log(pn/degree**gamma)
            if pn_one == 0:
                part_two = 0
            else:
                part_two = pn_one * math.log(pn_one/(degree+1)**gamma)
            if part_one + part_two < value_divkb:
                node_degree = degree
    list_of_platform_to_connect_to = list(app.config["registry"]["network"]["degrees_distribution"][node_degree-2])
    list_of_platform_to_connect_to.remove(app.config["PLATFORM-ID"])
    return list_of_platform_to_connect_to

# def add_platform(data,platform_id):
#     update_registry({"platforms":{platform_id:data}})
#
#
def add_model(model,model_id):
    update_registry({"models":{model_id:model}})
#
#
# def add_match(matching,match_id):
#     update_registry({"matchs":{match_id:matching}})



@app.route('/inscription', methods=['GET'])
def get_node_to_link_to():
    from copy import deepcopy
    # print(request.get_json(),file=sys.stderr)
    # curl -X GET 193.168.1.10:5000/inscription -H 'platform-id:4'  -H 'Content-Type:application/json' -H 'existing-model:2' -d '{"platforms":{"4":{"name":"DATAVERSE","URL":["http://193.168.1.13:5000"], "links":["2"]}}}'

    aux_registry = deepcopy(app.config["registry"])
    data = request.get_json()
    if "platform-id" not in request.headers:
        return "No platform-id"
    if "existing-model-id" not in request.headers:
        if "models" not in data:
            return "No model defined"
        if "matchs" not in data:
            return "No matches defined"

    platform_toadd_id = request.headers["platform-id"]
    platform_data = request

    # add_platform(data["platforms"][platform_toadd_id], platform_toadd_id)

    # if "existing-model-id" in request.headers:
    #
    #     # modify_registry_content(data["models"][request.headers["existing-model-id"]]["platforms"],platform_toadd_id,"add")
    #     if "matchs" in data:
    #         for match_id in data["matchs"]:
    #             aux_registry["matchs"][match_id] = data["matchs"]
    #             # add_match(data["matchs"][match_id],match_id)
    # else :
    #     add_model(data["models"])
    #
    #     for match_id in data["matchs"]:
    #         add_match(data["matchs"][match_id], match_id)
    # print(aux_registry["network"],file=sys.stderr)
    aux_registry["network"]["node_number"] += 1

    aux_registry["network"]["degrees_distribution"][0].append(platform_toadd_id)
    aux_registry["network"]["degrees_distribution"][len(aux_registry["platforms"][app.config["PLATFORM-ID"]]["links"])-2].remove(app.config["PLATFORM-ID"])
    aux_registry["platforms"][app.config["PLATFORM-ID"]]["links"].append(platform_toadd_id)
    aux_registry["network"]["degrees_distribution"][len(aux_registry["platforms"][app.config["PLATFORM-ID"]]["links"])-2].append(app.config["PLATFORM-ID"])
    if len(aux_registry["network"]["degrees_distribution"][len(aux_registry["network"]["degrees_distribution"])-1]) != 0:
        aux_registry["network"]["degrees_distribution"].append([])
    # save_registry()
    return str(get_node_nearest_from_distribution())

    # modify_registry_content("network.node_number", "update", registry["network"]["node_number"] + 1)
@app.route('/inscription', methods=['POST'])
def link_platforms():

    platform_toadd_id = request.headers["platform-id"]
    platform_tolinkto_id = request.headers["platform-tolink"]
    data = request.get_json()
    app.config["registry"]["platforms"][platform_toadd_id] = data["platforms"][platform_toadd_id]



    # add_platform(data["platforms"][platform_toadd_id], platform_toadd_id)

    if "existing-model-id" in request.headers:
        app.config["registry"]["models"][request.headers["existing-model-id"]]["platforms"].append(platform_toadd_id)

    #
    #     # modify_registry_content(data["models"][request.headers["existing-model-id"]]["platforms"],platform_toadd_id,"add")

    else :

        # registry["models"][list(data["models"].keys())[0]] = data["models"]
        for model_id in data["models"]:
            add_model(data["models"],model_id)
    #
    #     for match_id in data["matchs"]:
    #         add_match(data["matchs"][match_id], match_id)

    if "matchs" in data:
        for match_id in data["matchs"]:
            app.config["registry"]["matchs"][match_id] = data["matchs"]
#             # add_match(data["matchs"][match_id],match_id)



    # for match_id in data["matchs"]:
    #     add_match(data["matchs"][match_id],match_id)
    # print(registry["network"],file=sys.stderr)
    # print(registry["platforms"], file=sys.stderr)
    app.config["registry"]["network"]["degrees_distribution"][0].append(platform_toadd_id)

    app.config["registry"]["network"]["degrees_distribution"][len(app.config["registry"]["platforms"][platform_tolinkto_id]["links"]) - 2].remove(platform_tolinkto_id)
    app.config["registry"]["platforms"][platform_tolinkto_id]["links"].append(platform_toadd_id)
    if len(app.config["registry"]["network"]["degrees_distribution"][len(app.config["registry"]["network"]["degrees_distribution"])-1]) != 0:
        app.config["registry"]["network"]["degrees_distribution"].append([])

    app.config["registry"]["network"]["degrees_distribution"][len(app.config["registry"]["platforms"][platform_tolinkto_id]["links"]) - 2].append(platform_tolinkto_id)

    app.config["registry"]["network"]["degrees_distribution"][len(app.config["registry"]["platforms"][app.config["PLATFORM-ID"]]["links"])-2].remove(app.config["PLATFORM-ID"])
    app.config["registry"]["platforms"][app.config["PLATFORM-ID"]]["links"].append(platform_toadd_id)
    app.config["registry"]["network"]["degrees_distribution"][len(app.config["registry"]["platforms"][app.config["PLATFORM-ID"]]["links"])-2].append(app.config["PLATFORM-ID"])

    save_registry()
    return flask.Response(status=204)


def update_registry(registry_add):

    for key in registry_add:
        if key == "platforms":
            for platforms_id in registry_add["platforms"]:
                if platforms_id in app.config["registry"]["platforms"]:
                    raise KeyError(platforms_id + " already exists. Change platform ID.")
                else :
                    app.config["registry"]["platforms"][platforms_id]=registry_add["platforms"][platforms_id]
        if key == "models":

            for models_id in registry_add["models"]:
                if models_id in app.config["registry"]["models"]:
                    raise KeyError(models_id + " already exists. Change models ID.")
                else :
                    app.config["registry"]["models"][models_id]=registry_add["models"][models_id]
        if key == "matchs":
            for match_id in app.config["registry"]["matchs"]:
                if match_id in app.config["registry"]["matchs"]:
                    raise KeyError(match_id + " already exists. Change match ID.")
                else :
                    app.config["registry"]["matchs"][match_id]=registry_add["matchs"][match_id]
    with open("registry.dict", "wb") as fp:
        pickle.dump(app.config["registry"], fp)

def modify_registry_content(key, value, op):

    if op == "add":
        aux = "registry"
        for sub_key in key.split("."):
            aux += '[' + sub_key + ']'
        aux +=".append("+value+")"
        eval(aux)
    if op == "remove":
        aux = "registry"
        for sub_key in key.split("."):
            aux += '[' + sub_key + ']'
        aux = "del("+aux+")"
        eval(aux)
    if op == "modify":
        aux = "registry"
        for sub_key in key.split("."):
            aux += '[' + sub_key + ']'
        aux += "=" + value
        eval(aux)


def save_registry():
    import time
    with open("registry.dict", "wb") as fp:
        pickle.dump(app.config["registry"], fp)
    # print(registry,file=sys.stderr)
    for platform_id in app.config["registry"]["platforms"][app.config["PLATFORM-ID"]]["links"]:
        # print(platform_id, file=sys.stderr)

        # PROBLEME DE MEDIA A GERER !!
        # SINON C4EST FINI JE CROIS
        # NE PAS OUBLIER DE MODIFIER LE CODE DANS TOUTES LES APP
        rep = req.post(app.config["registry"]["platforms"][platform_id]["URL"][0]+"/registry",
                 headers={"registry-version":str(time.time()), "Content-Type":"application/json",
                          "Accept":"application/json", "Platforms-visited":app.config["PLATFORM-ID"],
                          "Platform-Id":app.config["PLATFORM-ID"]},
                 data=json.dumps(app.config["registry"]), timeout=5)
        if rep.status_code == 400:
            print(rep.text)


if __name__ == '__main__':
    app.run()

