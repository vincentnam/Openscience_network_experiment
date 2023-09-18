
Be sure to have venv install : 
On Ubuntu : 
    
    apt install python3.8-venv

The "expe_init.py" have to be run BEFORE and AFTER the docker compose is run. 
The before part is the creation of needed files.
The after part is populating the MongoDB database.

Don't forget to install experiment init requirements.

    python3 -m venv part1_expe_venv
    source part1_expe_venv/bin/active
    pip3 -r requirements_init.txt

Then run 
    
    python3 expe_init.py

Then run

    docker compose up --build 

("sudo docker compose up --build" if your user is not privileged)
Be sure to have up to date docker version. Otherwise use "docker-compose" command, and don't forget to install docker-compose.

Then run 

    python3 expe_init.py

(to populate MongoDB)

The POC is deployed. Execute experiment_exec.sh to query the system, add a new platform and query again the system.

    sh experiment_exec.sh

Experiment done !