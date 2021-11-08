from concurrent.futures import ThreadPoolExecutor
import requests, json, time

domains = [
    "https://www.noticiasaominuto.com/tech",
    "https://www.jornaldenegocios.pt/empresas/tecnologias",
    "https://visao.sapo.pt/exameinformatica/noticias-ei"
]

d = {}
'''
d = {
    url (each domains entry) : {
        article_id: {
            timestamp: { dados cdx }
        }
    }
}
'''

def cdx_url(date_from, date_to, url):
    return "https://arquivo.pt/wayback/cdx?url={}/&from={}&to={}&output=json&filter==status:200&matchType=prefix".format(url, date_from, date_to)

def article_url(timestamp, url):
    return "https://arquivo.pt/noFrame/replay/{}/{}".format(timestamp, url)

def domain_request(domain):
    r = requests.get(cdx_url(20210101000000, 20211101000000, domain))
    if r.status_code != 200: return

    domain_dic = {}

    data = r.text.split('\n')[:-1]
    print(f"Amount of pages in {domain}: {len(data)}")

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(lambda cdx_entry: article_request(cdx_entry, domain_dic), data)

    d[domain] = domain_dic
    
def article_request(response, domain_dic):
    try:
        parsed = json.loads(response)
    except Exception:
        print(f"Invalid JSON string: {response}")
        return
    if parsed["status"] != "200": return
    
    article_entry = domain_dic.get(parsed["urlkey"], {})

    url = article_url(parsed["timestamp"], parsed["url"])
    print("[getting data] url =", url)

    r = None
    while True:
        first = r == None
        r = requests.get(url)
        
        if r.status_code == 200: break
        elif r.status_code == 429:
            if first: print("Threashold reached.")
            time.sleep(10)
        else: 
            print(f"Invalid url: {url}, status code: {r.status_code}")
            return

    parsed["html"] = r.text

    article_entry[parsed["timestamp"]] = parsed
    domain_dic[parsed["urlkey"]] = article_entry

for domain in domains:
    domain_request(domain)

with open("data1.json", "w") as file:
    json.dump(d, file, indent=4)
