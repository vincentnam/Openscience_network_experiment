# Run as administrator docker command BEFORE requesting

# docker compose up -d --build

# First part : 3 platforms, initial setup with 1 XML based platform, 1 noSQL document based platform
# and 1 SQL based platform


# Request done on ODATIS platform ; created to simulate a GUI implemented on ODATIS platform
#curl -X GET 193.168.1.10:5000/request -H 'model:1' \
## Key off ISO 19115 model used in ODATIS ; choosed as example, geographic extent is easy to match \
#-H 'key:MD_Metadata.identificationInfo.MD_DataIdentification.extent.EX_Extent.geographicElement.EX_GeographicBoundingBox.southBoundLatitude.Decimal.@value'
## Platform that initiate the request = the platform that get first the request and will propagate it : 1 = ODATIS ; doesn't change \
#-H "initiator:1"
## Id of platform that make the request :\
#-H "platform-id:1"
## Number of jump : 1 as it's initial request \
#-H "jump:1"
## Liste of visited platform, ODATIS is already visited; allow to not compute 2 time the same request\
#-H "platforms-visited:'1'"
## Operator of the metadata request (see expe_init.py for list of operator available on each platform)\
#-H "operator:lower or equal"
## Operand for the request\
#-H "operand:90"
## Allow to not flood the network compute capacity with not computing 2 time the same request \
#-H "request-id:ll9s"

echo "Return the number of document of each platform (each platform is identified by an ID (from 1 to 4 in this experiment)"
curl -X GET 193.168.1.10:5000/request -H 'model:1' -H 'key:MD_Metadata.identificationInfo.MD_DataIdentification.extent.EX_Extent.geographicElement.EX_GeographicBoundingBox.southBoundLatitude.Decimal.@value' -H "initiator:1" -H "platform-id:1" -H "jump:1" -H "platforms-visited:'1'" -H "operator:lower or equal" -H "operand:90" -H "request-id:$(date)"


sleep 2

#######
# Part 2 : Add a platform, JSON based (AERIS 2 for simplicity), connected to ODATIS as choosed platform
#######

### Get the list of platform to link to (based on power law distribution with gamma = 2.5 (see paper)
echo "Adding of a new platform (number with ID '4') : get the list of platform to link to based on wanted distribution."


curl -X GET 193.168.1.10:5000/inscription -H 'platform-id:4'  -H 'Content-Type:application/json' -H 'existing-model-id:2' -d '{"platforms":{"4":{"name":"AERIS2","URL":["http://193.168.1.13:5000"], "links":["2"]}}}'
# Return ["2","3"], the list of platforms id that minimize the Kullback-Leibner divergence from power law distribution


sleep 2
# Simulate the requesting from AERIS 2 to ODATIS platforms
#curl -X POST 193.168.1.10:5000/inscription
#### Id of the platform AERIS 2
# -H 'platform-id:4'
#### Technical parameter
# -H 'Content-Type:application/json'
#### Chosed to use already existing model (model with id 2 = AERIS model) ; no matching needed because matches already exists
# -H 'existing-model-id:2'
#### Registry information off AERIS2 platform
# -d '{"platforms":{"4":{"name":"AERIS2","URL":["http://193.168.1.13:5000"], "links":["2","1"]}}}'
#### Platform chosed among list of platform return by precedent request
# -H "platform-tolink:2" -v
echo '\nSelected platform = "2" : inscription with linkage to platform "1" (the platform that is requested) and to platform "2"'

curl -X POST 193.168.1.10:5000/inscription -H 'platform-id:4'  -H 'Content-Type:application/json' -H 'existing-model-id:2' -d '{"platforms":{"4":{"name":"AERIS2","URL":["http://193.168.1.13:5000"], "links":["2","1"]}}}' -H "platform-tolink:2"
# Return 204 response : inscription is well done


sleep 2

#### Doing again the first request to see if new platform is request
echo "Return the number of document of each platform (with the newly registered platform, with ID '4')"

curl -X GET 193.168.1.10:5000/request -H 'model:1' -H 'key:MD_Metadata.identificationInfo.MD_DataIdentification.extent.EX_Extent.geographicElement.EX_GeographicBoundingBox.southBoundLatitude.Decimal.@value' -H "initiator:1" -H "platform-id:1" -H "jump:1" -H "platforms-visited:'1'" -H "operator:lower or equal" -H "operand:90" -H "request-id:$(date)"

# Return {
#  "1": 22862,
#  "2": 1,
#  "3": 1,
#  "4": 1
#} -> number of document of each platform (XML platform is the lenght of the document, the information needed is : is there any document returned ?)



### New platform is requested ! Well done !


# Be careful, don't forget to change "initiator" AND "platform-visited" unless the platform will be ignored
#curl -X GET 193.168.1.13:5000/request -H 'model:2' -H 'key:spatialExtents.area.southLatitude' -H "initiator:4" -H "platform-id:client" -H "jump:1" -H "platforms-visited:'4'" -H "operator:lower or equal" -H "operand:90" -H "request-id:$(date)"

echo "Querying platform 3 and return informations from each platforms"
curl -X GET 193.168.1.12:5000/request -H 'model:3' -H 'key:position.latitude' -H "initiator:3" -H "platform-id:client" -H "jump:1" -H "platforms-visited:'3'" -H "operator:lower or equal" -H "operand:90" -H "request-id:$(date)"
