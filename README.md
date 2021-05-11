# Optical Objects Recognition API

###### This is a repository for an Optical Objects Recognition API.

The inference REST API works on CPU. It's only supported on Linux Operating systems.

This repository offers three services:

- **Optical Character Recognition** service using [Tesseract](https://github.com/tesseract-ocr/tesseract) to extract text boxes from images
- **Data Matrix** decoding service using [Libdmtx](https://github.com/NaturalHistoryMuseum/pylibdmtx) to extract and decode Data Matrices from images
- **QR Code** decoding service using [Zbar](https://github.com/NaturalHistoryMuseum/pyzbar) to extract and decode QR codes from images 

This repo can be deployed using either **docker** or **docker swarm**.

Please use **docker swarm** only if you need to:

* Provide redundancy in terms of API containers: In case a container went down, the incoming requests will be redirected to another running instance.

* Coordinate between the containers: Swarm will orchestrate between the APIs and choose one of them to listen to the incoming request.

* Scale up the Inference service in order to get a faster prediction especially if there's traffic on the service.

If none of the aforementioned requirements are needed, simply use **docker**.

## Prerequisites

- Ubuntu 18.04
- Docker CE latest stable release

### Check for prerequisites

To check if you have docker-ce installed:

```sh
docker --version
```

### Install prerequisites

Use the following command to install docker on Ubuntu:

```sh
chmod +x install_prerequisites.sh && source install_prerequisites.sh
```

## Build The Docker Image

In order to build the project run the following command from the project's root directory:    

```sh
sudo docker build -t optical_objects_recognition_api -f docker/dockerfile .
```

### Behind a proxy

```sh
sudo docker build --build-arg http_proxy='' --build-arg https_proxy='' -t optical_objects_recognition_api -f ./docker/dockerfile .
```

## Run the docker container

As mentioned before, this container can be deployed using either  **docker** or **docker swarm**. 

If you wish to deploy this API using **docker**, please issue the following run command. 

If you wish to deploy this API using **docker swarm**, please refer to following link [docker swarm documentation](./README-docker_swarm.md). After deploying the API with docker swarm, please consider returning to this documentation for further information about the API endpoints as well as the model structure sections.

To run the API, go the to the API's directory and run the following:

#### Using Linux based docker:

```sh
sudo docker run -p <docker_host_port>:4343 optical_objects_recognition_api
```

The <docker_host_port> can be any unique port of your choice.

The API file will be run automatically, and the service will listen to http requests on the chosen port.

## API Endpoints

To see all available endpoints, open your favorite browser and navigate to:

```
http://<machine_IP>:<docker_host_port>/docs
```

### Endpoints summary

#### /models/{model_name}/ocr (POST)

Takes an image and returns extracted text boxes

![predict image](./docs/5.gif)

#### /models/{model_name}/data_matrix (POST)

Takes an image and decodes extracted data matrices

![predict image](./docs/5.gif)

#### /models/{model_name}/qr_code (POST)

Takes an image and decodes extracted QR codes

![predict image](./docs/5.gif)



## Acknowledgment

[Anis Ismail](https://www.linkedin.com/in/anisdismail), Lebanese American University, Beirut, Lebanon

[robotron.de](https://robotron.de)

