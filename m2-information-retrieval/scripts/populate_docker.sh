#!/bin/bash

docker exec $(docker ps -lq) bin/solr delete -c arquivo
docker exec $(docker ps -lq) bin/solr create_core -c arquivo

curl -X POST -H 'Content-type:application/json' \
    --data-binary @../schema.json \
    http://localhost:8983/solr/arquivo/schema

docker cp ../dataset/data.json $(docker ps -lq):/data/arquivo.json
docker exec $(docker ps -lq) bin/post -c arquivo /data/arquivo.json
