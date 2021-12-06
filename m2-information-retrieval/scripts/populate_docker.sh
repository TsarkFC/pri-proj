#!/bin/bash

curl -X POST -H 'Content-type:application/json' \
    --data-binary @../schema.json \
    http://localhost:8983/solr/arquivo/schema

docker exec $(docker ps -lq) bin/post -c arquivo /data/arquivo.json