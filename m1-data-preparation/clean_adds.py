import json, sys

try:
    content = json.load(sys.stdin)
except Exception:
    print(f"Invalid JSON string from stdin", file=sys.stderr)
    exit()

news = content["noticiasaominuto"]
for article, timestamps in news.items():
    for timestamp, data in timestamps.items():
        text = data['article']["text"]
        data['article']["text"] = text.split("ACOMPANHE AQUI O")[0]
            
json.dump(content, sys.stdout, indent = 4)