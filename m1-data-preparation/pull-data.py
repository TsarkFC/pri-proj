from concurrent.futures import ThreadPoolExecutor
from newspaper import Article
from tqdm import tqdm
import requests, json, time, re, sys

domains = {
    "https://www.noticiasaominuto.com/tech": re.compile("^(com,noticiasaominuto\)\/tech\/[0-9]+\/[a-z0-9-%]+)(?:(?:\?|&).*)?$"),
    "https://www.jornaldenegocios.pt/empresas/tecnologias": re.compile("^(pt,jornaldenegocios\)\/empresas\/tecnologias\/[a-z0-9-%]+\/[a-z0-9-%]+)(?:\?.*)?$"),
    "https://visao.sapo.pt/exameinformatica/noticias-ei": re.compile("^(pt,sapo,visao\)\/exameinformatica\/noticias-ei(?:\/[a-z0-9-%]+)?\/[0-9]+-[a-z0-9-%.]+)(?:\?.*)?$")
}
'''
domains = {
    domain_url: article_urlkey_verification_regex (regex to verify if urlkey belongs to an article and to capture the part of the url without get parameters)
}
'''

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

def domain_request(domain, article_validation_regex):
    print(f"\nRequesting CDX data for {domain}...")

    r = requests.get(cdx_url(20210101000000, 20211101000000, domain))
    if r.status_code != 200: return

    domain_dic = {}

    data = r.text.split('\n')[:-1]
    print(f"Received {len(data)} CDX entries.\n")

    progress_bar = tqdm(total=len(data), file=sys.stdout)

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(lambda cdx_entry: article_request(cdx_entry, domain_dic, article_validation_regex, progress_bar), data)

    progress_bar.close()
    d[domain] = domain_dic


def get_article_info(url, html = None):
    a = Article(url)

    if not html: a.download()
    else: a.set_html(html)

    a.parse()

    return {
        'title': a.title,
        'authors': a.authors,
        # 'publish_date': a.publish_date.str,
        'text': a.text,
        'top_image': a.top_image,
        'summary': a.summary
    }


def article_request(response, domain_dic, article_validation_regex, progress_bar):
    progress_bar.update(1)
    try:
        parsed = json.loads(response)
    except Exception:
        print(f"Invalid JSON string: {response}", file=sys.stderr)
        return
    if parsed["status"] != "200": return

    # This checks if the entry is an article and captures the first part of the urlkey (without GET parameters)
    urlkey_match = article_validation_regex.match(parsed["urlkey"])
    if not urlkey_match:
        print(f"NOT an article: {parsed['urlkey']}", file=sys.stderr)
        return

    urlkey_base = urlkey_match.group(1) # urlkey without get parameters
    
    article_entry = domain_dic.get(urlkey_base, {})
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

    # Running newspaper3k on the received HTML
    parsed["article"] = get_article_info(url, r.text)

    article_entry[parsed["timestamp"]] = parsed
    domain_dic[urlkey_base] = article_entry

print("Starting data retrieval.")
for domain, regex in domains.items():
    domain_request(domain, regex)

with open("data.json", "w") as file:
    json.dump(d, file, indent=4)
