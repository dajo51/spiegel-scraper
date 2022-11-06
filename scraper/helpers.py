import urllib.request
from bs4 import BeautifulSoup
from collections import namedtuple


def get_article_links(year: int, issue: int) -> list:
    """Gets all the article links from an given issure

    Args:
        year (int): publishing year
        issue (int): issue number

    Returns:
        list: list of all article links as string
    """
    article_links = []
    Link = namedtuple("Link", "article_title article_link")

    with urllib.request.urlopen(
        f"https://www.spiegel.de/spiegel/print/index-{year}-{issue}.html"
    ) as response:
        html = response.read()

    for a in BeautifulSoup(html, "html.parser").findAll("article"):
        article_link = a.find("a")
        article_links.append(Link(article_link["title"], article_link["href"]))

    return article_links


print(get_article_links(2006, 1)[1])
