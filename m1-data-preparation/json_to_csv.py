import pandas as pd, csv, sys, os

def check_args():
    if len(sys.argv) != 2:
        print("[error] run: python json_to_csv.py file")
        return False
    return True

def flatten_json(data):
    domains = []
    urlkeys = []
    news = []

    domain_pk = 1
    urlkey_pk = 1
    news_pk = 1

    for domain in data.keys():
        domains.append([domain_pk, domain])
        urls = data[domain]
        domain_pk += 1

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
                news_pk += 1

    return [domains, urlkeys, news]

def create_dir(dirname):
    check_folder = os.path.isdir(dirname)
    if not check_folder:
        os.makedirs(dirname)

def main():
    if not check_args(): return

    try:
        df = pd.read_json(sys.argv[1])
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