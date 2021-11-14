import pandas as pd
import matplotlib.pyplot as plt

domain = pd.read_csv("csv/domain.csv", delimiter=',', quotechar='"')
news = pd.read_csv("csv/news.csv", delimiter=',', quotechar='"')
urlkeys = pd.read_csv("csv/urlkeys.csv", delimiter=',', quotechar='"')

title2 = "Total number of indexed tech news per domain in 2021, indexed by arquivo.pt"

def count_top_of_bar(plot, data, func):
    rects = plot.patches
    labels = [func(data, i) for i in range(len(rects))]

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        plot.text(
            rect.get_x() + rect.get_width() / 2, height + 5, label, ha="center", va="bottom"
        )

def access(data, i):
    return data[i]

def access_plus_one(data, i):
    return data[i+1]

def total_news_plot(grouped, title):
    # set color legends
    colors = {"noticiasaominuto.com":"red", "jornaldenegocios.pt":"green", "exameinformatica":"blue"}         
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(handles, labels)

    # set plot properties
    plot = grouped.plot(
        kind="bar", title=title, color=colors.values())
    plot.set_xlabel("domain")
    plot.set_ylabel("number of news")
    count_top_of_bar(plot, grouped, access_plus_one)
    plt.show()

def total_news():
    grouped = urlkeys.groupby(by=["domain_pk"]).size()
    total_news_plot(grouped, "Number of tech news per domain in 2021, indexed by arquivo.pt")
    

def total_updated_news():
    news_urlkeys = news.merge(urlkeys, on="urlkey_pk", how="left")
    joined = news_urlkeys.merge(domain, on="domain_pk", how="left")

    grouped = joined.groupby(by=["domain_pk"]).size()
    total_news_plot(grouped, "Total number of indexed tech news per domain in 2021, indexed by arquivo.pt")
    

def number_of_times_news_were_indexed(url=None):
    if url:
        domain_pk = int(domain[domain["domain"] == url]["domain_pk"])
        news_urlkeys = news.merge(urlkeys, on="urlkey_pk", how="left")
        news_domain = news_urlkeys[news_urlkeys["domain_pk"] == domain_pk]
        grouped = news_domain.groupby("urlkey_pk")
    else:
        grouped = news.groupby("urlkey_pk")

    maximum = int(grouped.count().agg(["max"])["news_pk"])

    x = range(1, maximum+1)
    y = []
    for i in x:
        n = int(grouped.filter(lambda x: len(x) == i).count()["news_pk"])
        y.append(n)

    x_label = "index count"
    y_label = "number of news"
    df = pd.DataFrame({x_label:x, y_label:y})

    title_str = "Number of times news were indexed at arquivo.pt at "
    if url: title_str += url
    else: "all domains"

    plot = df.plot(x_label, y_label, kind="bar", title=title_str)
    count_top_of_bar(plot, y, access)
    # plot = df.plot(x_label, y_label, kind='scatter')    
    plt.show()


# total_news()
# total_updated_news()
# number_of_times_news_were_indexed("exameinformatica")
