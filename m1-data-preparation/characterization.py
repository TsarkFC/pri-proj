import pandas as pd
import os, sys
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 500)
pd.options.mode.chained_assignment = None

domain = pd.read_csv("csv/domain.csv", delimiter=',', quotechar='"')
news = pd.read_csv("csv/news.csv", delimiter=',', quotechar='"')
urlkeys = pd.read_csv("csv/urlkeys.csv", delimiter=',', quotechar='"')

def save_to_file():
    if len(sys.argv) != 2:
        return False
    if sys.argv[1] == "save":
        return True
    return False

def access(data, i):
    return data[i]


def access_plus_one(data, i):
    return data[i+1]


def create_dir(dirname):
    check_folder = os.path.isdir(dirname)
    if not check_folder:
        os.makedirs(dirname)


def count_top_of_bar(plot, data, func):
    rects = plot.patches
    labels = [func(data, i) for i in range(len(rects))]

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        plot.text(
            rect.get_x() + rect.get_width() / 2, height + 5, label, ha="center", va="bottom"
        )


def set_plot(data, xlabel, ylabel, title, access_method, filename, colors=["blue"], y=None):
    if y is None:
        y = data

    plot = data.plot(kind="bar", title=title, color=colors)
    plot.set_xlabel(xlabel)
    plot.set_ylabel(ylabel)
    count_top_of_bar(plot, y, access_method)
    
    if save_to_file():
        create_dir("plots")
        fig = plot.get_figure()
        fig.savefig("plots/" + filename + ".png")
    else:
        plt.show()


def total_news_plot(grouped, title, xlabel, ylabel, filename):
    colors = {"noticiasaominuto.com": "red",
              "jornaldenegocios.pt": "green", "exameinformatica": "blue"}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label])
               for label in labels]
    plt.legend(handles, labels)

    set_plot(grouped, xlabel, ylabel, title, access_plus_one, filename, colors.values())


def total_news():
    grouped = urlkeys.groupby(by=["domain_pk"]).size()
    total_news_plot(
        grouped, "Number of tech news per domain in 2021, indexed by arquivo.pt", "domain", "number of news", "total_news")


def total_updated_news():
    news_urlkeys = news.merge(urlkeys, on="urlkey_pk", how="left")
    joined = news_urlkeys.merge(domain, on="domain_pk", how="left")

    grouped = joined.groupby(by=["domain_pk"]).size()
    total_news_plot(
        grouped, "Total number of indexed tech news per domain in 2021, indexed by arquivo.pt", "domain", "number of news", "total_updated_news")


def number_of_times_indexed(url=None):
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
    df = pd.DataFrame({y_label: y})
    df.index = pd.RangeIndex(1,len(df) + 1)

    title_str = "Number of times news were indexed at arquivo.pt at "
    if url: title_str += url
    else: title_str += "all domains"

    set_plot(df, x_label, y_label, title_str, access, "number_of_times_indexed", y=y)


def avg_article_length():
    news_urlkeys = news.merge(urlkeys, on="urlkey_pk", how="left")
    joined = news_urlkeys.merge(domain, on="domain_pk", how="left")

    joined["article_length"] = joined["text"].map(
        lambda x: 0 if isinstance(x, float) else len(x))
    grouped = joined.groupby("domain_pk")["article_length"].mean().astype(int)

    total_news_plot(grouped, "Mean of size article text per domain of pages indexed by arquivo.pt",
                    "domain", "mean length of article (characters)", "avg_article_length")


def group_by_year(url=None):
    data = news
    if url:
        domain_pk = int(domain[domain["domain"] == url]["domain_pk"])
        news_urlkeys = news.merge(urlkeys, on="urlkey_pk", how="left")
        data = news_urlkeys[news_urlkeys["domain_pk"] == domain_pk]

    data["publish_year"] = data["publish_date"].map(lambda x: str(x)[:4])
    grouped = data.groupby("publish_year").size()

    title_str = "News indexed by arquivo.pt in 2021 grouped by published year at "
    if url: title_str += url
    else: title_str += "all domains"

    set_plot(grouped, "year", "number of indexed articles", title_str, access, "group_by_year")


total_news()
total_updated_news()
number_of_times_indexed("exameinformatica")
avg_article_length()
group_by_year("exameinformatica")
