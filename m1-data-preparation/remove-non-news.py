import json, re, sys

NOTICIAS_AO_MINUTO = "noticiasaominuto"
JORNAL_DE_NEGOCIOS = "jornaldenegocios"
EXAME_INFORMATICA = "exameinformatica"

domains = {
    NOTICIAS_AO_MINUTO: {
        "regex": re.compile("^(com,noticiasaominuto\)\/tech\/[0-9]+\/[a-z0-9-%]+)(?:(?:\?|&).*)?$"),
    },
    JORNAL_DE_NEGOCIOS: {
        "regex": re.compile("^(pt,jornaldenegocios\)\/empresas\/tecnologias\/[a-z0-9-%]+\/[a-z0-9-%]+)(?:\?.*)?$")
    },
    EXAME_INFORMATICA: {
        "regex": re.compile("^(pt,sapo,visao\)\/exameinformatica\/noticias-ei(?:\/[a-z0-9-%]+)?\/[0-9]+-[a-z0-9-%.]+)(?:\?.*)?$")
    }
}

d = {}
try:
    d = json.load(sys.stdin)
except Exception as e:
    print(f"Invalid JSON string from stdin", file=sys.stderr)
    exit()

news_links = {}

for domain_id, links in d.items():
    news_links[domain_id] = []
    for link in links:
        try:
            parsed = json.loads(link)
        except Exception:
            print(f"Invalid JSON string: {link}", file=sys.stderr)
            exit()
        if parsed["status"] != "200": continue
        if not domains[domain_id]['regex'].match(parsed['urlkey']):
            print(f"NOT an article: {parsed['urlkey']}", file=sys.stderr)
            continue
        news_links[domain_id].append(parsed)

json.dump(news_links, sys.stdout, indent = 4)