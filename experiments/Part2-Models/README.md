Experiment part 2 :

"models/struct" folder contains structured model and Python notebook to extract models from example files, populate a MongoDB database and generate structural model matching in root folder.
"models/sem" folder contains semantic model (vocabularies) and a Python notebook to merge into a single file the 3 models.

All models have been inserted in the same database MongoDB. Before making the requests, start a MongoDB database listening to port 27017 on localhost: 
    
    docker run -p 27017:27017 mongo  

