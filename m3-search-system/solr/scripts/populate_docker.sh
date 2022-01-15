#!/bin/bash

docker exec m3-search-system-solr-1 bin/solr delete -c arquivo
docker exec m3-search-system-solr-1 bin/solr create_core -c arquivo

curl -X POST -H 'Content-type:application/json' \
    --data-binary @../schema.json \
    http://localhost:8983/solr/arquivo/schema

docker cp ../synonyms.txt m3-search-system-solr-1:/var/solr/data/arquivo/conf/synonyms.txt

docker cp ../dataset/data.json m3-search-system-solr-1:/data/arquivo.json
docker exec m3-search-system-solr-1 bin/post -c arquivo /data/arquivo.json