import requests, json, sys

NOTICIAS_AO_MINUTO = "noticiasaominuto"
JORNAL_DE_NEGOCIOS = "jornaldenegocios"
EXAME_INFORMATICA = "exameinformatica"

domains = {
    NOTICIAS_AO_MINUTO: {
        "url": "https://www.noticiasaominuto.com/tech"
    },
    JORNAL_DE_NEGOCIOS: {
        "url": "https://www.jornaldenegocios.pt/empresas/tecnologias"
    },
    EXAME_INFORMATICA: {
        "url": "https://visao.sapo.pt/exameinformatica/noticias-ei"
    }
}

d = {}
'''
d = {
    "domain": [
        {
            "urlkey": "...",
            "timestamp": "...",     
        }
    ]
}
'''

def cdx_url(date_from, date_to, url):
    return "https://arquivo.pt/wayback/cdx?url={}/&from={}&to={}&output=json&filter==status:200&matchType=prefix".format(url, date_from, date_to)

def domain_request(domain_id, domain_data):
    print(f"Requesting CDX data for {domain_id}...", file=sys.stderr)

    r = requests.get(cdx_url(20210101000000, 20211101000000, domain_data["url"]))
    if r.status_code != 200: return

    data = r.text.split('\n')[:-1]
    print(f"Received {len(data)} CDX entries.", file=sys.stderr)

    d[domain_id] = data


for domain_id, domain_data in domains.items():
    domain_request(domain_id, domain_data)

json.dump(d, sys.stdout, indent=4)
