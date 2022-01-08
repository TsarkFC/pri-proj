#!/bin/bash

docker exec m3-search-system_solr_1 bin/solr delete -c arquivo
docker exec m3-search-system_solr_1 bin/solr create_core -c arquivo

curl -X POST -H 'Content-type:application/json' \
    --data-binary @../schema.json \
    http://localhost:8983/solr/arquivo/schema

docker cp ../dataset/data.json m3-search-system_solr_1:/data/arquivo.json
docker exec m3-search-system_solr_1 bin/post -c arquivo /data/arquivo.json
