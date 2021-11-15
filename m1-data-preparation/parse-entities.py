import json, sys, spacy
from slugify import slugify

nlp = spacy.load("pt_core_news_lg")

MISC = "MISC"
ORG = "ORG"
LOC = "LOC"
PER = "PER"

entities = {}

news_sites = None
try:
    news_sites = json.load(sys.stdin)
except Exception:
    print(f"Invalid JSON string from stdin", file=sys.stderr)
    exit()

entity_blacklist = {
    "Portugal\",realizada" : "Portugal"
}

# e.g. "em Portugal"
first_word_blacklist = [
    "em",
    "de",
    "a",
    "o"
]

def clean_entity_text(text):
    text = text.strip()
    text_lower = text[:3].lower()
    
    for word in first_word_blacklist:
        word += " "
        if text_lower.find(word, 0, len(word)) != -1: text = text[len(word):]

    text = text[0].upper() + text[1:]

    if text in entity_blacklist: return entity_blacklist[text]
    return text

current_entity_id = 0

for domain_id, news in news_sites.items():
    for article, timestamps in news.items():
        for timestamp, data in timestamps.items():
            doc = nlp(data["article"]["text"])
            data["article"]["entities"] = set()

            for entity in doc.ents:
                entity_text = clean_entity_text(entity.text)

                entity_id = None

                slug = slugify(entity_text)
                if slug not in entities:
                    current_entity_id += 1
                    entity_id = current_entity_id
                    entities[slug] = {
                        'id': entity_id,
                        'labels': {},
                        'names': {}
                    }
                else:
                    entity_id = entities[slug]['id']

                data["article"]["entities"].add(entity_id)

                # trying to decide between different labels
                # (resultant from multiple spacy interpretations)
                # and names for same entity

                if entity.label_ not in entities[slug]['labels']: entities[slug]['labels'][entity.label_] = 0
                entities[slug]['labels'][entity.label_] += 1
                
                if entity_text not in entities[slug]['names']: entities[slug]['names'][entity_text] = 0
                entities[slug]['names'][entity_text] += 1

            data["article"]["entities"] = list(data["article"]["entities"])


# deciding the best classigication for each entity
for slug, entity in entities.items():
    most_used = None
    for item in entity['labels'].items():
        if most_used == None:
            most_used = item
            continue
    
        if item[1] > most_used[1]:
            most_used = item
    
    del entity['labels']
    entity['label'] = most_used[0]

    most_used = None
    for item in entity['names'].items():
        if most_used == None:
            most_used = item
            continue
    
        if item[1] > most_used[1]:
            most_used = item
    
    del entity['names']
    entity['name'] = most_used[0]


csv_entities = "entity_pk,slug,title,label\n"
for slug, entity in entities.items():
    csv_entities += f"{entity['id']},{slug},{entity['name']},{entity['label']}\n"

json.dump(news_sites, sys.stdout, indent = 4)
print(csv_entities, file=sys.stderr, end="")
