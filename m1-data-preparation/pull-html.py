from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import requests, json, time, re, sys

NOTICIAS_AO_MINUTO = "noticiasaominuto"
JORNAL_DE_NEGOCIOS = "jornaldenegocios"
EXAME_INFORMATICA = "exameinformatica"

domains = {
    NOTICIAS_AO_MINUTO: {
        "regex": re.compile("^(com,noticiasaominuto\)\/tech\/[0-9]+\/[a-z0-9-%]+)(?:(?:\?|&).*)?$"),
        "url": "https://www.noticiasaominuto.com/tech"
    },
    JORNAL_DE_NEGOCIOS: {
        "url": "https://www.jornaldenegocios.pt/empresas/tecnologias",
        "regex": re.compile("^(pt,jornaldenegocios\)\/empresas\/tecnologias\/[a-z0-9-%]+\/[a-z0-9-%]+)(?:\?.*)?$")
    },
    EXAME_INFORMATICA: {
        "url": "https://visao.sapo.pt/exameinformatica/noticias-ei",
        "regex": re.compile("^(pt,sapo,visao\)\/exameinformatica\/noticias-ei(?:\/[a-z0-9-%]+)?\/[0-9]+-[a-z0-9-%.]+)(?:\?.*)?$")
    }
}


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

def article_url(timestamp, url):
    return "https://arquivo.pt/noFrame/replay/{}/{}".format(timestamp, url)
    

def article_request(parsed, domain_dic, domain_id, article_validation_regex):
    # This checks if the entry is an article and captures the first part of the urlkey (without GET parameters)
    urlkey_match = article_validation_regex.match(parsed["urlkey"])
    if not urlkey_match:
        print(f"NOT an article: {parsed['urlkey']}", file=sys.stderr)
        return
    url = article_url(parsed["timestamp"], parsed["url"])

    r = None
    while True:
        first = r == None
        r = requests.get(url)
        
        if r.status_code == 200: break
        elif r.status_code == 429:
            if first: print("Threshold reached.", file=sys.stderr)
            time.sleep(10)
        else:
            print(f"Invalid url: {url}, status code: {r.status_code}", file=sys.stderr)
            return

    lock.acquire()
    urlkey_base = urlkey_match.group(1) # urlkey without get parameters
    
    article_entry = domain_dic.get(urlkey_base, {})
    article_entry[parsed["timestamp"]] = parsed
    article_entry[parsed["timestamp"]]['html'] = r.text
    domain_dic[urlkey_base] = article_entry
    lock.release()
    

news_links = {}
try:
    news_links = json.load(sys.stdin)
except Exception:
    print(f"Invalid JSON string from stdin", file=sys.stderr)
    exit()

lock = Lock()

for domain_id, links in news_links.items():
    domain_dic = {}
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(lambda cdx_entry: article_request(cdx_entry, domain_dic, domain_id, domains[domain_id]["regex"]), links)        

    d[domain_id] = domain_dic
    
json.dump(d, sys.stdout, indent = 4)