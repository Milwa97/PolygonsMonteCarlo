# FastAPI for beginners

This is a FastAPI training for beginners. This training includes building a simple web API using FastAPI library.
There are three files with the app and three files with response models.
The highest version, the more advanced techniques are used.
File main.py is compatible with response_models_v1,
Files main_v1.py, main_v2.py are compatible with response_models_v1, response_models_v2, response_models_v3.

More info: [FastAPI](https://fastapi.tiangolo.com/tutorial/)

## Contents
Currently, the repository consists of folders:
 - api - contains the FastAPI
 - power point presentation


## Requirements:

In order to run this module it is recommended to have installed
the following software versions:
- Python 3.9 (preferably 3.9.13)
- Package Manager (e.g. virtualenv)
- Docker

## How to run?

1. Clone project repository or download zip package from Wiki page

2. Create virtual environment in the project folder:
```
python -m venv venv_name
```

3. Activate virtual environment:
```
venv_name\Scripts\activate
```

4. Install all necessary python packages:

```
pip install -r requirements.txt
```

5. Run web api:

```
uvicorn main_v1:app --reload --port 1234 --host 127.0.0.1
```

Flags:
* --reload - Enable auto-reload.
* --port - Bind socket to this port.  [default: 8000]
* --host - Bind socket to this host.  [default: 127.0.0.1]


Automatic interactive API documentation (provided by Swagger UI) can be accessed on:
* http://127.0.0.1:8000/docs#/
* http://127.0.0.1:8000/redoc/

This web api also accept request for client REST API such as Insomia, PostMan


## Docker:

Configure 
1. Install and configure docker in WSL: [gitlab instruction](https://gitlab.comarch-cloud/ERP_ML/cluster/blob/master/docu/wsl_docker_config.md)
2. open linux terminal in project folder
3. build docker image from Dockerfile
```
sudo docker build -t image_name .
```

4. run docker image
```
sudo docker run --name container_name -p 5000:5005 image_name
```
where 
* 5005 is port exposed in dockerfile, 
* 5000 is the port, where  web api is available n the host machine

5. Navigate to [http://127.0.0.1:5000/docs#/](http://127.0.0.1:5000/docs#/)

### Useful docker commands:
Check image status:
```
sudo docker images
```

Check container status:
```
sudo docker ps -a
```
