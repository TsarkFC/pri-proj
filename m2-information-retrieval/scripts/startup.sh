#!/bin/bash

precreate-core arquivo

# Start Solr in background mode so we can use the API to upload the schema
solr start -m 2g

echo "Started, adding schema"

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/arquivo/schema

echo "Schema added, adding data"

# Populate collection
bin/post -c arquivo /data/arquivo.json

echo "Data addeed, restarting"

# Restart in foreground mode so we can access the interface
solr restart -f
