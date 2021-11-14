import json, sys, spacy
from tqdm import tqdm

nlp = spacy.load("pt_core_news_lg")

MISC = "MISC"
ORG = "ORG"
LOC = "LOC"
PER = "PER"

news_sites = {}
try:
    news_sites = json.load(sys.stdin)
except Exception:
    print(f"Invalid JSON string from stdin", file=sys.stderr)
    exit()

total = 0
for domain_id, news in news_sites.items():
    for article, timestamps in news.items():
        for timestamp, data in timestamps.items():
            total += 1

progress_bar = tqdm(total=total, file=sys.stdout)

for domain_id, news in news_sites.items():
    for article, timestamps in news.items():
        for timestamp, data in timestamps.items():
            progress_bar.update(1)
            doc = nlp(data["article"]["text"])
            data["article"]["entities"] = {
                MISC : set(),
                ORG : set(),
                LOC : set(),
                PER : set(),
            }

            for entity in doc.ents:
                data["article"]["entities"][entity.label_].add(entity.text)

            
            for label, content in data["article"]["entities"].items():
                data["article"]["entities"][label] = list(content)

progress_bar.close()

json.dump(news_sites, sys.stdout, indent = 4)
