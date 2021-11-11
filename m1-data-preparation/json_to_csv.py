import pandas as pd, csv, sys

def flatten_json(data):
    domains = []
    urlkeys = []
    news = []

    domain_pk = 1
    urlkey_pk = 1
    news_pk = 1

    for domain in data.keys():
        domains.append([domain_pk, domain])
        domain_pk += 1
        urls = data[domain]

        for urlkey in urls.keys():
            if str(urls[urlkey]) == "nan": continue
            timestamps = urls[urlkey]
            urlkeys.append([urlkey_pk, domain_pk, urlkey])
            urlkey_pk += 1

            for timestamp in timestamps.keys():
                element = [news_pk, urlkey_pk, timestamp]
                article_details = timestamps[timestamp]["article"]
                article_details_list = [article_details[key] for key in article_details]
                element.extend(article_details_list)
                news.append(element)

    return [domains, urlkeys, news]

df = pd.read_json(sys.argv[1])
df.head()
tables = flatten_json(df)

file_names = ['csv/domain.csv', 'csv/urlkeys.csv', 'csv/news.csv']
for i in range(len(file_names)):
    with open(file_names[i], 'w', newline='') as f:
        writer = csv.writer(f)
        for row in tables[i]:
            writer.writerow(row)