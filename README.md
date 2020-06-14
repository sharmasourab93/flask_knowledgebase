# Flask Knowledgebase 


A Sample Flask project to explore 

    - Flask 
    - Flask-SQLAlchemy 
    - Standard ways to build an application in Flask
    - HTTP Protocols
    - As standard for Improvization On Potential Flask Application 
    - A Docker Container to Execute the Application
    
--
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

__

## Solution

The Application uses `Python3`, `Flask` webframework and `MySQL` database remotely.  
The API requests and responses makes use of JSON format.  
The HTTP Protocols namely `GET`, `POST`, `PUT` and `DELETE` are implemented in each of the methods based on functionality.  
The Implementation of `Docker` container is explained in the Docker Components sub section.  


### File Structure 
    
    ```
        ./flask_knowledgebase/
        |-- Dockerfile
        |-- wsgi.py
        |-- app.py
        |-- config.yaml
        |-- init_db.py
        |-- load_configs.py
        |-- requirements.txt
        |-- venv/
        `-- README.md
    ```


The packages to execute the application as listed in `requirements.txt` are as below: 

    ```
        sqlalchemy
        flask==1.1.2
        flask_sqlalchemy==2.4.3
        werkzeug==0.16.1
        requests==2.23.0
        bs4==0.0.1
        eng-dictionary==0.0.3
        PyYaml==5.3.1
        mysql-connector-python-rf==2.2.2
    ```


One of the files in the root directory is `wsgi.py`, which looks like as below: 

    ```python 
        from app import flask_app
        
        application = flask_app
        
        
        if __name__ == '__main__':
            application.run()
    ```
   This modification was done to host the application on the Gunicorn server. `gunicorn` can be executed like a linux command and it takes in the `wsgi.py` as an argument along with bind and workers as below. 
   
    ``` gunicorn -w 4 --bind 0.0.0.0:5000 wsgi ```
    
   The `gunicorn` server binds the host and port of the server along with the variable `application` to run in the `wsgi.py` which it looks up by default. `flask_app` is the Flask application component which is imported from `app.py`. `app.py` contains SQLAlchemy DB components and the core Flask App components. 
   
   In later revisions, these will be segrated into separate modules or improvized along with further extensions. 


The explanation below makes use of key word like `<IP-address>` which is the IP address utilized by the application to make REST calls.  
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
    
    ```[DELETE] http//<IP-address>:5000/<id>```
    
    This method takes only the `<id>` which is expected to be an integer.   
    And after the query is filtered based on the integer id, the filtered entry is removed from the database.
    
    
    
### Docker Components 

A `Dockerfile` exists in the root directory which is utilitzed to build and run as a container.

The docker file is written as below: 

    ```
        FROM python:latest

        WORKDIR /src/

        ENV PYTHONDONTWRITEBYTECODE 1
        ENV PYTHONBUFFERED 1


        RUN pip install --upgrade pip
        COPY app.py /src/.
        COPY . .
        COPY wsgi.py /src/.
        COPY load_configs.py /src/.
        COPY requirements.txt /src/requirements.txt
        COPY config.yaml /src/.

        RUN pip install -r requirements.txt

        CMD ["gunicorn", "--bind", "0.0.0.0:5000","wsgi", "-w", "1"]
    ``` 
    
The dockerfile transfers all the necessary components of the application into the docker image and hosts the server on [Gunicorn](https://gunicorn.org/).

The Dockerfile is first built using the following command : 
    
    ``` docker build -t flaskkb:1.0 . ```

   This command builds the dockerfile into an image. Now to run the image as a container the image name `flaskkb:1.0` is used to run as below:
   
    ``` docker run --detach -p 5000:5000 flaskkb:1.0 ```

   `--detach` runs the container in the background. 
   

### Improvements 

1. Adding Security Features/ Extending with `flask_login`. 
2. Extending Docker with `minikube` and exploring `Kubernetes` components.
3. Deployment of the application server using [Nginx](https://www.nginx.com/). # Need exploration on this which will be explained once done.
4. Segragtion of Model Components and Flask App components. 
5. Writing unittests
