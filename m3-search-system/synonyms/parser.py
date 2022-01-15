import json

file = open("source.txt", "r")
lines = file.readlines()

d = {}

for line in lines:
    source = line.split()
    synonym = source[1]
    word = source[3]

    l = d.get(word, [])
    l.append(synonym)
    d[word] = l

with open("../solr/synonyms.json", "w") as outfile:
    json.dump(d, outfile)
