#!/bin/bash

curl -X POST -H 'Content-type:application/json' \
    --data-binary @../schema.json \
    http://localhost:8983/solr/arquivo/schema

docker exec 4f bin/post -c arquivo /data/arquivo.json