import pickle
import json
import os
from pymongo import MongoClient
# Run BEFORE the docker compose is up
registry = json.loads(open("registry.json","r").read())

with open("registry_ODATIS.dict", "wb") as fp:
    pickle.dump(registry,fp)
with open("registry_AERIS.dict", "wb") as fp:
    pickle.dump(registry,fp)
with open("registry_FHIR.dict", "wb") as fp:
    pickle.dump(registry,fp)

operator_list_mongo = {
    "equal":"$eq",
    "lower or equal":"$lte",
    "greater or equal":"$gte",
    "greater than":"$gt",
    "in":"$in",
    "lower than":"$lt",
    "not equal":"$ne",
    "not in":"$nin"
}

operator_list_sql= {
    "equal":"=",
    "lower or equal":"<=",
    "greater or equal":">=",
    "greater than":">",
    # "in":"$in",
    "lower than":"<",
    "not equal":"!=",
    # "not in":"$nin"
}
operator_list_xml = {
    "equal":"operator.eq",
    "lower or equal":"operator.le",
    "greater or equal":"operator.ge",
    "greater than":"operator.gt",
    "lower than":"operator.lt",
    "not equal":"operator.ne"
}

with open("operator_list_mongo.dict", "wb") as fp:
    pickle.dump(operator_list_mongo,fp)

with open("operator_list_sql.dict", "wb") as fp:
    pickle.dump(operator_list_sql,fp)

with open("operator_list_xml.dict", "wb") as fp:
    pickle.dump(operator_list_xml,fp)



# Run AFTER the docker compose is up
mongoclient = MongoClient("localhost:27017")
for folder in os.listdir("AERIS"):
    file = json.load(open("AERIS/"+folder+"/"+os.listdir("AERIS/"+folder)[0]))
    print(os.listdir("AERIS/"+folder))
    mongoclient.AERIS.metadata.insert_one(file)

