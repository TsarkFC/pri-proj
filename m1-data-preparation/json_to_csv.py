import pandas as pd, csv, sys, os

news_entity_relation_csv = ["news_pk,entity_pk\n"]

def flatten_json(data):
    global news_entity_relation_csv
    domains = [["domain_pk", "domain"]]
    urlkeys = [["urlkey_pk", "domain_pk", "urlkey"]]
    news = [["news_pk", "urlkey_pk", "timestamp", "title", "summary", "image", "publish_date", "authors", "text"]]

    domain_pk = 1
    urlkey_pk = 1
    news_pk = 1

    for domain in data.keys():
        domains.append([domain_pk, domain])
        urls = data[domain]

        for urlkey in urls.keys():
            if str(urls[urlkey]) == "nan": continue
            timestamps = urls[urlkey]
            urlkeys.append([urlkey_pk, domain_pk, urlkey])

            for timestamp in timestamps.keys():
                element = [news_pk, urlkey_pk, timestamp]
                article = timestamps[timestamp]["article"]
                for entity in article["entities"]:
                    news_entity_relation_csv.append(f"{news_pk},{entity}\n")
                article_details = [article[key] for key in article if key != "entities"] # we don't want to include the entities in the csv
                element.extend(article_details)
                news.append(element)
                news_pk += 1
            urlkey_pk += 1
        domain_pk += 1

    return [domains, urlkeys, news]

def create_dir(dirname):
    check_folder = os.path.isdir(dirname)
    if not check_folder:
        os.makedirs(dirname)

def main():
    try:
        df = pd.read_json(sys.stdin)
    except:
        print("[error] provided file is not loadable as json")
        return
    df.head()
    tables = flatten_json(df)

    create_dir("csv")

    file_names = ['csv/domain.csv', 'csv/urlkeys.csv', 'csv/news.csv']
    for i in range(len(file_names)):
        with open(file_names[i], 'w', newline='') as f:
            writer = csv.writer(f)
            for row in tables[i]:
                writer.writerow(row)

main()
with open("csv/news_entities.csv", "w") as f:
    f.writelines(news_entity_relation_csv)
