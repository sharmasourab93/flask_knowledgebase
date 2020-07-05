#!/bin/bash 

echo "Killing Old Docker Containers"
docker-compose rm -fs 

echo "Building Docker Containers"
docker-compose up --build -d
#docker build -t flaskkb_nginx:1.3 .
