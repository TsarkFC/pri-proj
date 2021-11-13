from bs4 import BeautifulSoup
import json, re, sys

NOTICIAS_AO_MINUTO = "noticiasaominuto"
JORNAL_DE_NEGOCIOS = "jornaldenegocios"
EXAME_INFORMATICA = "exameinformatica"


dates_regex = {
    NOTICIAS_AO_MINUTO : re.compile("(\d\d):(\d\d) - (\d\d)\/(\d\d)\/(\d\d)"),
    JORNAL_DE_NEGOCIOS : re.compile("(\d\d) de (.*?) de (\d\d\d\d) às (\d\d):(\d\d)"),
    JORNAL_DE_NEGOCIOS + "_only_hour" : re.compile("(\d\d):(\d\d)"),
    EXAME_INFORMATICA : re.compile("(\d\d)\.(\d\d)\.(\d\d\d\d) às (\d\d)h(\d\d)")
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

    if newspaper == NOTICIAS_AO_MINUTO and match:
        return "20" + match.group(5) + match.group(4) + match.group(3) + match.group(1) + match.group(2) + "00"
    
    elif newspaper == JORNAL_DE_NEGOCIOS:
        if match:
            return match.group(3) + month_encoding[match.group(2).lower()] + match.group(1) + match.group(4) + match.group(5) + "00"
        
        hour_match = dates_regex[newspaper + "_only_hour"].match(date_string)
        if hour_match:
            return indexation_timestamp[:8] + hour_match.group(1) + hour_match.group(2) + "00"
    
    elif newspaper == EXAME_INFORMATICA and match:
        return match.group(3) + match.group(2) + match.group(1) + match.group(4) + match.group(5) + "00"
    
    return ""


def get_article_info(domain_id, indexation_timestamp, html = None):
    if not html: return

    soup = BeautifulSoup(html, "html.parser")

    if EXAME_INFORMATICA == domain_id:
        authors = soup.select_one(".author-meta .name")
        
        date = parse_date(indexation_timestamp, EXAME_INFORMATICA, soup.select_one(".publish-date").get_text())
        
        image = soup.select_one(".wp-block-image img")
        if image == None: image = soup.select_one(".thumbnail-image-wrapper img")

        if image != None and "src" not in image.attrs and "data-src" in image.attrs: image.attrs["src"] = image.attrs["data-src"]

        return {
            'title' : soup.select_one(".entry-title").get_text(),
            'summary' : soup.select_one(".entry-excerpt").get_text().strip("\n "),
            'image' : image.attrs['src'] if image != None else "",
            'publish_date' : date,
            'authors' : authors.get_text() if authors != None else "",
            'text' : newline_replace_regex.sub("\n", soup.select_one(".entry-content").get_text().strip("\r\n"))
        }

    if NOTICIAS_AO_MINUTO == domain_id:
        authors = soup.select_one(".author-hover")

        date = parse_date(indexation_timestamp, NOTICIAS_AO_MINUTO, soup.select_one(".news-info-time").contents[0])

        return {
            'title' : soup.select_one(".news-headline").get_text(),
            'summary' : soup.select_one(".news-subheadline").get_text(),
            'image' : soup.select_one(".news-main-image picture img").attrs['src'],
            'publish_date' : date,
            'authors' : authors.get_text() if authors != None else "",
            'text' : newline_replace_regex.sub("\n", soup.select_one(".news-main-text").get_text().strip("\r\n"))
        }
    
    if JORNAL_DE_NEGOCIOS == domain_id:
        authors = soup.select_one(".info_autor strong")
        
        date = parse_date(indexation_timestamp, JORNAL_DE_NEGOCIOS, soup.select_one(".info_autor span").get_text())
        
        return {
            'title' : soup.select_one(".article_title").get_text().strip(),
            'summary' : soup.select_one(".lead").get_text().strip(),
            'image' : soup.select_one(".multimedia_container img").attrs['src'],
            'publish_date' : date,
            'authors' : authors.get_text() if authors != None else "",
            'text' : newline_replace_regex.sub("\n", soup.select_one(".main_text .texto").get_text().strip("\r\n"))
        }

    return None

news_sites = {}
try:
    news_sites = json.load(sys.stdin)
except Exception:
    print(f"Invalid JSON string from stdin", file=sys.stderr)
    exit()
    
for domain_id, news in news_sites.items():
    for article, timestamps in news.items():
        for timestamp, data in timestamps.items():
            data['article'] = get_article_info(domain_id, data['timestamp'], data['html'])
            del data['html']
            
json.dump(news_sites, sys.stdout, indent = 4)