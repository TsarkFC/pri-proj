import requests, json

domains = [
    "https://www.publico.pt/tecnologia",
    "https://www.noticiasaominuto.com/tech",
    "https://www.sapo.pt/noticias/tecnologia"
]

d = {}
'''
d = {
    url (each domains entry) : {
        article_id: [multiple article versions (html), ...]
    }
}
'''

def cdx_url(date_from, date_to, url):
    return "https://arquivo.pt/wayback/cdx?url={}/*&from={}&to={}&output=json&filter==status:200".format(url, date_from, date_to)

def article_url(timestamp, url):
    return "https://arquivo.pt/noFrame/replay/{}/{}".format(timestamp, url)

def domain_request(domain):
    r = requests.get(cdx_url(2020, 2021, domain))
    if r.status_code != 200: return

    domain_dic = {}

    for response in r.text.split("\n"):
        article_request(response, domain_dic)
        
    d[domain] = domain_dic
    
def article_request(response, domain_dic):
    try:
        parsed = json.loads(response)
    except Exception:
        print("Invalid JSON string")
        return
    if parsed["status"] != "200": return
    
    article_entry = domain_dic.get(parsed["urlkey"], [])
    if article_entry:
        print("[updating entry] key =", parsed["urlkey"])
        article_entry[1].append(parsed["timestamp"])
    else:
        print("[getting data] key =", parsed["urlkey"])
        url = article_url(parsed["timestamp"], parsed["url"])
        r = requests.get(url)
        if r.status_code != 200: return
        article_entry = [r.text, [parsed["timestamp"]]]
    domain_dic[parsed["urlkey"]] = article_entry

for domain in domains:
    domain_request(domain)
print(d)