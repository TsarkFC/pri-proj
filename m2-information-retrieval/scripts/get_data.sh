#!/bin/bash

cd ..
if [[ ! -d dataset ]]
then
    mkdir dataset
fi

unzip ../m1-data-preparation/dataset/dataset_json.zip -d dataset/

# Transform json data to list
echo "[$(cat dataset/data-final.json)]" > dataset/data-final.json
