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

dates_regex = {
    "noticiasaominuto" : re.compile("(\d\d):(\d\d) - (\d\d)\/(\d\d)\/(\d\d)"),
    "jornaldenegocios" : re.compile("(\d\d) de (.*?) de (\d\d\d\d) às (\d\d):(\d\d)"),
    "jornaldenegocios_only_hour" : re.compile("(\d\d):(\d\d)"),
    "exameinformatica" : re.compile("(\d\d)\.(\d\d)\.(\d\d\d\d) às (\d\d)h(\d\d)")
}

newline_replace_regex = re.compile("\r?\n ?(?:\r?\n ?)+")

month_encoding = {
    "janeiro" : "01",
    "fevereiro" : "02",
    "março" : "03",
    "abril" : "04",
    "maio" : "05",
    "junho" : "06",
    "julho" : "07",
    "agosto" : "08",
    "setembro" : "09",
    "outubro" : "10",
    "novembro" : "11",
    "dezembro" : "12",
}

def parse_date(indexation_timestamp, newspaper, date_string):
    match = dates_regex[newspaper].match(date_string)

    if newspaper == "noticiasaominuto" and match:
        return "20" + match.group(5) + match.group(4) + match.group(3) + match.group(1) + match.group(2) + "00"
    
    elif newspaper == "jornaldenegocios":
        if match:
            return match.group(3) + month_encoding[match.group(2).lower()] + match.group(1) + match.group(4) + match.group(5) + "00"
        
        hour_match = dates_regex[newspaper + "_only_hour"].match(date_string)
        if hour_match:
            return indexation_timestamp[:8] + hour_match.group(1) + hour_match.group(2) + "00"
    
    elif newspaper == "exameinformatica" and match:
        return match.group(3) + match.group(2) + match.group(1) + match.group(4) + match.group(5) + "00"
    
    return ""


def get_article_info_bs(url : str, indexation_timestamp, html = None):
    if not html: return

    soup = BeautifulSoup(html, "html.parser")

    info = None
    if re.search("noticiasaominuto", url):
        authors = soup.select_one(".author-hover")

        date = parse_date(indexation_timestamp, "noticiasaominuto", soup.select_one(".news-info-time").contents[0])

        info = {
            'title' : soup.select_one(".news-headline").get_text(),
            'summary' : soup.select_one(".news-subheadline").get_text(),
            'image' : soup.select_one(".news-main-image picture img").attrs['src'],
            'publish_date' : date,
            'authors' : authors.get_text() if authors != None else "",
            'text' : newline_replace_regex.sub("\n", soup.select_one(".news-main-text").get_text().strip("\r\n"))
        }
    
    if re.search("jornaldenegocios", url):
        authors = soup.select_one(".info_autor strong")
        
        date = parse_date(indexation_timestamp, "jornaldenegocios", soup.select_one(".info_autor span").get_text())
        
        info = {
            'title' : soup.select_one(".article_title").get_text().strip(),
            'summary' : soup.select_one(".lead").get_text().strip(),
            'image' : soup.select_one(".multimedia_container img").attrs['src'],
            'publish_date' : date,
            'authors' : authors.get_text() if authors != None else "",
            'text' : newline_replace_regex.sub("\n", soup.select_one(".main_text .texto").get_text().strip("\r\n"))
        }
    
    print(url, file=sys.stderr)

    if re.search("exameinformatica", url):
        authors = soup.select_one(".author-meta .name")
        
        date = parse_date(indexation_timestamp, "exameinformatica", soup.select_one(".publish-date").get_text())
        
        image = soup.select_one(".wp-block-image img")
        if image == None: image = soup.select_one(".thumbnail-image-wrapper img")

        if image != None and "src" not in image.attrs and "data-src" in image.attrs: image.attrs["src"] = image.attrs["data-src"]

        info = {
            'title' : soup.select_one(".entry-title").get_text(),
            'summary' : soup.select_one(".entry-excerpt").get_text().strip("\n "),
            'image' : image.attrs['src'] if image != None else "",
            'publish_date' : date,
            'authors' : authors.get_text() if authors != None else "",
            'text' : newline_replace_regex.sub("\n", soup.select_one(".entry-content").get_text().strip("\r\n"))
        }

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
errors = []

def article_request(response, domain_dic, article_validation_regex, progress_bar):
    try:
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
        parsed["article"] = get_article_info_bs(url, parsed["timestamp"], r.text)

        article_entry[parsed["timestamp"]] = parsed
        domain_dic[urlkey_base] = article_entry
    except Exception as e:
        errors.append(f"{response}:\n{str(e)}")

print("Starting data retrieval.")
for domain, regex in domains.items():
    domain_request(domain, regex)

if len(errors):
    print("There have been thread exceptions!")
    print("!! THREAD EXCEPTIONS", file=sys.stderr)
    for e in errors: print(e, file=sys.stderr)

with open("data.json", "w") as file:
    json.dump(d, file, indent=4)
