import sys, json
import pandas as pd

if len(sys.argv) != 3:
    print("We need an input and output file!", sys.stderr)

output_file = open(sys.argv[2], "w")
with open(sys.argv[1], "r") as f:
    data = json.load(f)

output = []

def format_date_to_solr(original):
    # YYYYMMDDhhmmss to YYYY-MM-DDThh:mm:ssZ
    if original == "":
        return None
    return original[:4] + "-" + original[4:6] + "-" + original[6:8] + "T" + original[8:10] + ":" + original[10:12] + ":" + original[12:14] + "Z"

entities = pd.read_csv("./dataset/entities.csv", sep=",")

entities_memo = {}
fields_to_remove = ["mime", "status", "digest", "length", "offset", "filename", "collection", "source", "source-coll"]

for newspaper in data.keys():
    for urlkey in data[newspaper]:
        for version in data[newspaper][urlkey]:
            obj = data[newspaper][urlkey][version]
            for field in fields_to_remove: del(obj[field])
            obj["urlkey"] = urlkey # update urlkey - some versions have different urlkeys that have query parameters
            obj["newspaper"] = newspaper
            obj["timestamp"] = format_date_to_solr(obj["timestamp"])
            obj["article"]["publish_date"] = format_date_to_solr(obj["article"]["publish_date"])
            new_entities = []
            for entity_id in obj["article"]["entities"]:
                if (entity_id in entities_memo):
                    new_entities.append(entities_memo[entity_id])
                else:
                    line = entities[entities["entity_pk"] == entity_id]
                    parsed = line.to_dict(orient="records")[0]
                    new_entities.append(parsed)
                    entities_memo[entity_id] = parsed

            obj["article"]["entities"] = new_entities

            for entity in new_entities:
                if "slug" in entity: del entity["slug"]
                if "entity_pk" in entity: del entity["entity_pk"]

            output.append(obj)

json.dump(output, output_file, indent=4)
