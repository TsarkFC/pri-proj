from concurrent.futures import ThreadPoolExecutor
#from newspaper import Article
from tqdm import tqdm
from bs4 import BeautifulSoup
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

    r = requests.get(cdx_url(20210401000000, 20210501000000, domain))
    if r.status_code != 200: return

    domain_dic = {}

    data = r.text.split('\n')[:-1]
    print(f"Received {len(data)} CDX entries.\n")

    progress_bar = tqdm(total=len(data), file=sys.stdout)

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(lambda cdx_entry: article_request(cdx_entry, domain_dic, article_validation_regex, progress_bar), data)

    progress_bar.close()
    d[domain] = domain_dic


def get_article_info_bs(url : str, html = None):
    if not html: return

    soup = BeautifulSoup(html, "html.parser")

    info = {}
    if re.search("noticiasaominuto", url):
        info['title'] = soup.select_one(".news-headline").contents[0]
        info['summary'] = soup.select_one(".news-subheadline").contents[0]
        info['image'] = soup.select_one(".news-main-image picture img").attrs['src']
        info['date'] = soup.select_one(".news-info-time").contents[0]
        info['authors'] = soup.select_one(".author-hover").contents[0]
        info['text'] = soup.select_one(".news_capital_letter").contents
        info['text'].extend([a.contents[-1] for a in soup.select(".news-main-text > p")])
        info['text'] = info['text'][0] + "\n".join(info['text'][1:])
    
    if re.search("jornaldenegocios", url):
        info['title'] = soup.select_one(".article_title").contents[0].strip()
        info['summary'] = soup.select_one(".lead").contents[0].strip()
        info['image'] = soup.select_one(".main_article .image img").attrs['src']
        info['date'] = soup.select_one(".info_autor span").contents[0]
        info['authors'] = soup.select_one(".info_autor strong").contents[0]
        info['text'] = [a.contents[0] for a in soup.select(".main_text .texto > p")]
        info['text'] = "\n".join(info['text'][1:])

    if re.search("exameinformatica", url):
        info['title'] = soup.select_one(".entry-title").contents[0]
        info['summary'] = soup.select_one(".entry-excerpt").contents[0].strip('\n ')
        info['image'] = soup.select_one(".wp-block-image img").attrs['src']
        info['date'] = soup.select_one(".publish-date").contents[0]
        authors = soup.select_one(".author-meta name")
        info['authors'] = authors.contents[0] if authors != None else ""
        info['text'] = [a.contents[0] for a in soup.select(".entry-content > p")]
        info['text'] = "\n".join(info['text'][1:])

    return info

# def get_article_info(url, html = None):
#     a = Article(url)

#     if not html: a.download()
#     else: a.set_html(html)

#     a.parse()

#     return {
#         'title': a.title,
#         'authors': a.authors,
#         # 'publish_date': a.publish_date.str,
#         'text': a.text,
#         'top_image': a.top_image,
#         'summary': a.summary
#     }


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
    parsed["article"] = get_article_info_bs(url, r.text)

    article_entry[parsed["timestamp"]] = parsed
    domain_dic[urlkey_base] = article_entry

print("Starting data retrieval.")
for domain, regex in domains.items():
    domain_request(domain, regex)

with open("data.json", "w") as file:
    json.dump(d, file, indent=4)
