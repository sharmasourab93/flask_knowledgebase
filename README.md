# Flask Knowledgebase 


A Sample Flask project to explore 

    - Flask 
    - Flask-SQLAlchemy 
    - Standard ways to build an application in Flask
    - HTTP Protocols
    - As standard for Improvization On Potential Flask Application 
    - A Docker Container to Execute the Application
    
---


## Problem Statement

**Tech Stack** : Python3 + Flask + MySQL 

Build a Flask Application, which takes *No UI* and Only has a *Backend* (make use of JSON for API).
The application should be able to do the following over HTTP Protocols \[ namely `GET`, `POST`, `PUT`, `DELETE` ] : 

    1. Get all the Knowledge Items
    2. Get a Knowledge Item based on UID
    3. Get a Knowledge Item based on a Row Value
    4. Insert Values 
    5. Alter Values 
    6. Delete Values


The application needs to operate on a database like `mysql` or `postgres`. 

The application should implement `unittest`. 

The application should be delivered as a `Docker` container.

___

## Solution

The Application uses `Python3`, `Flask` webframework and `MySQL` database remotely.  
The API requests and responses makes use of JSON format.  
The HTTP Protocols namely `GET`, `POST`, `PUT` and `DELETE` are implemented in each of the methods based on functionality.  
The Implementation of `Docker` container is explained in the Docker Components sub section.


___

## Index
1. File Structure & Introduction
2. Routes Explained  
3. Docker Components Reference

    1. Introduction to Docker Components
    2. Pushing Docker Images to Docker Hub
    3. Pushing Docker Images to GitHub Packages
    
4. Integration With Nginx
5. Improvements


___


### File Structure & Introduction

The [file structure](#file-structure--introduction) of the project is as given below.
    
```
    ./flask_knowledgebase/
    |-- flask_kb/
    |   |-- __init__.py
    |   |-- configs/
    |   |   |-- __init__.py
    |   |   |-- load_configs.py
    |   |   |-- sql_configs.yaml
    |   |   `-- logging.yml
    |   |
    |   |-- log/
    |   |   |-- __init__.py
    |   |   |-- configuration_loader.py
    |   |   |-- log_configurator.py # the module which holds 
    |   |   |                       # LogConfigurator class
    |   |   `-- logger_test.py      # Testing Logger
    |   |
    |   |-- models/
    |   |   |-- __init__.py
    |   |   |-- dict_table.py
    |   |   `-- users.py
    |   |
    |   |-- routes.py
    |   |-- run.py
    |   |-- requirements.txt
    |   `-- Dockerfile              # Dockerfile for initiating Flask-KB application
    |
    |-- nginx/
    |   |-- nginx.conf
    |   |-- project.conf
    |   `-- Dockerfile              # Dockerfile for initiating Nginx-Container
    |
    |-- tests/
    |   |-- base.py                 # Base for all the test cases.
    |   |-- test_routes.py 
    |   `-- test_sessions.py
    |
    |-- docker-compose.yml          # docker-compose will build the Dockerfile(s) in nginx/ & flask_kb/
    |-- run_docker.sh               # Shell script to execute Docker commands
    |-- README.md
    |-- .gitignore                  # Git ignore file.
    |
    `-- venv/                       # Virtual Environment 
                                    # Marked as ignored in .gitignore file
```


The python packages required to execute the application as listed in `requirements.txt` are as below: 

``` 
    flask==1.1.2
    werkzeug==0.16.1
    flask_sqlalchemy==2.4.3
    Flask-Login==0.5.0
    Flask-Bcrypt==0.7.1
    gunicorn==20.0.4
    mysql-connector-python-rf==2.2.2
    sqlalchemy==1.3.17
    PyYaml==5.3.1
    bs4==0.0.1
    eng-dictionary==0.0.3
```

One of the files in the root directory is `run.py`, which looks like as below: 

```python 
    from app import flask_app as application
    
    
    if __name__ == '__main__':
        application.run()
```

To host it on Gunicorn server  
   
    gunicorn -w 4 --bind 0.0.0.0:5000 run
 

`flask_app` is the Flask application component which is imported from the module `flask_kb` as `application`.  
`flask_kb/models` has schema components.  
`flask_kb/configs` holds the configs to connect to the db.  
`flask_kb/log` holds the logger modulels & keeps `flask-kb.log` (an event log for the flask application).  


___


### Routes Explained
The explanation below makes use of key word like `<IP-address>` which is the IP address utilized by the application to make [REST calls](#routes-explained).  
The expectations were implemented in the following manner: 

1. **Get all the Knowledge Items**

    ```[GET] http://<IP-address>:5000/ ```
    
    yeilds all the entries made to the table. 
    
2. **Get a Knowledge Item based on UID**
    
    ```[GET] http://<IP-address>:5000/<id>```
    
    where `<id>` is the unique ID meant for a unique entry and is expects an integer.
    This endpoint fetches the id, word and meaning associated with the id argument passed in the URL. 
    
3. **Get a Knowledge Item based on a Row Value**

    ```[GET] http://<IP-address>:5000/by_word/<word>```
    
    where `<word>` is the string for which the entry is to be queried. 
    
4. **Insert a Value**

    ```[POST] http://<IP-address>:5000/add/```
    
    This method takes a JSON body and the JSON for sample looks like as follows: 
    
    ```json
       {
           "word": "something"
        }   
   ```
   
   This method adds a meaning using the `BrowseMeaning` module in the package `eng_dictionary`.  
   Refer to this url for more on [eng_dictionary](https://github.com/sharmasourab93/eng_dictionary). 

5. **Alter a Value** 

    ```[PUT] http://<IP-address>:5000/change/```
    
    This method takes a JSON body and the JSOn for sample looks as follows: 
    
    ```json
       {
           "word": "something", 
           "meaning": "new altered meaning"
         } 
   ```
   
   This method alters value stored in the database. 
 
6. **Delete a Value**
    
    ```[DELETE] http://<IP-address>:5000/<id>```
    
    This method takes only the `<id>` which is expected to be an integer.   
    And after the query is filtered based on the integer id, the filtered entry is removed from the database.

7. **Register**
    
    ```[POST] http://<IP-address>:5000/register```  
    
    This method registers a user to access resources.   
    The pre-condition to register is that the user must not be logged-in and the user must not be already registered.  
    
    This method takes JSON parameters in the format as below: 
    
    ```json
        {
          "user": "username", 
          "password": "password",
          "email": "user@email.com"
        } 
    ```

8. **Login**

    ```[POST] http://<IP-address>:5000/login```
    
    This method lets you login with a user and password passed in the JSON parameter. 

    ```json
        {
          "user": "username", 
          "password": "password"
        } 
    ```
    The only condition here is that the user must be a registered to be able to access resource. 
  
9. **Logout**

    ```[GET] http://<IP-Address>:5000/logout```  
    
    This method lets you logout from the logged in session. 
    
10. **Logged In**
    
     ```[GET] http://<IP-Address>:5000/loggedin```  
     
     This method lets you know the current logged in user, else No User.  
     
___    
    
### Docker Components Explained

A `Dockerfile` exists in the root directory which is utilitzed to build and run as a container.

The [docker file](#docker-components-explained) written for the `flask_kb` is as given below: 

```Dockerfile
FROM python:latest

WORKDIR /src/. 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt 

COPY run.py /src/
COPY ./configs /src/flask_kb/configs/
COPY ./routes.py /src/flask_kb/
COPY ./__init__.py /src/flask_kb/
COPY ./models /src/flask_kb/models/
COPY ./log /src/flask_kb/log/
COPY ./entrypoint.sh /src/

ENV PYTHONPATH "${PYTHONPATH}:/src/flask_kb/"
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "run", "&"]
``` 
    
The dockerfile transfers all the necessary components of the application into the docker image and hosts the server on [Gunicorn](https://gunicorn.org/).

On the `nginx` folder, exists a Dockerfile which is as given below: 

```Dockerfile
FROM nginx:1.15.8

RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/
COPY project.conf /etc/nginx/conf.d/
CMD ["nginx", "-g", "daemon off;"]
```

This `Dockerfile` sets the nginx context on to a Docker container. 


The Dockerfile(s) in the respective folders are composed using a docker-compose.   
Find the `docker-compose.yml` located on the root as given below. 

```docker-compose.yml
version: '3'

services: 
  flask_kb: 
   container_name: flask_kb
   build: ./flask_kb
   ports:
    - "5000:5000"
   command: gunicorn -b 0.0.0.0:5000 -w 1 run

  nginx:
   container_name: nginx
   build: ./nginx
   ports:
    - "80:80"
   depends_on: 
    - flask_kb

```

The docker-compose handles the Dockerfile in `flask_kb` and `nginx`.
<!--The Dockerfile is first built using the following command : 
    
    docker build -t flaskkb:X.X 


This command builds the dockerfile into an image. Now to run the image as a container the image name `flaskkb:X.X` is used to run as below:
   
    docker run --detach -p 5000:5000 flaskkb:X.X

   `--detach` runs the container in the background. -->


`run_docker.sh` is the shell script to intiate building of docker containers.   
The script likes as given below: 

```shell script
#!/bin/bash 

echo "Killing Old Docker Containers"
docker-compose rm -fs 

echo "Building Docker Containers"
docker-compose up --build -d
#docker build -t flaskkb_nginx:1.3 .
```

*Note: X.X refers to incremental Verison Sequences*   


##### Pushing Docker Images to Docker Hub
The built [docker image](#pushing-docker-images-to-docker-hub) can be uploaded to the [dockerhub](http://hub.docker.com).   

The preconditions ofcourse are:  
1. Having an account on Dockerhub  
2. The docker account must be logged into, on the working machine.  
3. Tag & Push the docker image to Dockerhub as referred in [this document](https://docs.docker.com/docker-hub/repos/).  


The Docker Image for this application `flaskkb:X.X` on docker hub can be found here: [flaskkb](https://hub.docker.com/repository/docker/sharmasourab93/flaskkb)  


##### Pushing Docker Images to Github Packages

After [building the image](#pushing-docker-images-to-github-packages) and verifying it, the given steps will upload the image to github.

1. Ensure you have a Github Auth Token to authenticate your docker github. 

     ```cat ~/GH_TOKEN.txt | docker login docker.pkg.github.com -u sharmasourab93 --password-stdin```  

2. Use the following command to tag the latest version of the image on Github

      ```docker tag IMAGE_ID docker.pkg.github.com/sharmasourab93/eng_dictionary/IMAGE_NAME:VERSION```

3. Then Use the command given below to push the latest version of the image on Github

      ```docker push docker.pkg.github.com/sharmasourab93/eng_dictionary/IMAGE_NAME:VERSION```  

The uploaded image is on github packages here: [flaskkb](https://github.com/sharmasourab93/flask_knowledgebase/packages)


___


### Integration With Nginx
[Integration](#integration-with-nginx) with [Nginx](https://www.nginx.com/) is done in the `nginx/` folder.  

The `nginx/` folder contains:  

```tree
|-- nginx/
    |   |-- nginx.conf
    |   |-- project.conf
    |   `-- Dockerfile  
```   

The `nginx.conf` file has the necessary configuration for the bringing up the server.   
The `project.conf` has the configuration set for intergrating with `flask_kb` app and it's endpoint.  
The `Dockerfile` has the necessary configurations to initiate/start `nginx` server.  


### Improvements 
The [improvements](#improvements) are being tracked as below:

1. ~~Structuring the Package/App~~
2. ~~Adding Security Features/ Extending with `flask_login`.~~
3. ~~Enabling Logger~~
4. ~~Deployment of the application server using [Nginx](https://www.nginx.com/).~~
5. Bug fixes with routes.   
6. Writing unittests.  
7. Minor Imporvements (if Needed) 
8. Extending Docker with `minikube` (exploring `Kubernetes` components).
9. Integrating with Jenkins/CI\CD pipeline is use case identified.

