#!/bin/bash

cd ..
if [[ ! -d dataset ]]
then
    mkdir dataset
fi

unzip -o ../m1-data-preparation/dataset/dataset_json.zip -d dataset/

python3 ./scripts/get_solr_data.py ./dataset/data-final.json ./dataset/data.json

rm ./dataset/data-final.json
