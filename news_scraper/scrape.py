from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

from .article import Article


def parse(url, pageHtml, bodyLines):
    soup = BeautifulSoup(pageHtml, "lxml")
    host = urlparse(url).hostname

    if host == 'www.nydailynews.com':
        headline = soup.find(itemprop="headline").string
        try:
            author = soup.find(rel="author").string.strip()
        except AttributeError:
            author = soup.find(id="a-credits").string.strip()
        rawBody = soup.find_all('p', limit=bodyLines)
        body = ''
        for i in range(bodyLines):
            body += (rawBody[i].text.strip()) + ' '

    elif host == 'www.nytimes.com':
        headline = soup.find(itemprop="headline").string
        author = soup.find(attrs={"name": "author"})['content'].strip()  # Author is in the tag itself
        rawBody = soup.find_all(attrs={"class": "story-body-text story-content"}, limit=bodyLines)
        body = ''
        for i in range(bodyLines):
            body += (rawBody[i].text) + ' '

    elif host == 'www.dnainfo.com':
        headline = soup.find(attrs={"class": "social-group"})['data-title'].strip()  # Title is in the tag itself
        author = soup.find(attrs={"class": "name"}).string
        rawBody = soup.find_all('p', limit=bodyLines)
        body = ''
        for i in range(bodyLines):
            body += (rawBody[i].text.strip()) + ' '

    elif host == 'www.silive.com':
        headline = soup.find(attrs={"name": "title"})['content'].strip()  # Title is in the tag itself
        author = soup.find(attrs={"name": "article_author"})['content'].split('|')[0].strip()  # Author is in the tag itself, cutting out content right of '|'
        rawBody = soup.find_all('p', limit=bodyLines+1)  # So we can skip the first <p>
        body = ''
        for i in range(bodyLines):
            body += (rawBody[i+1].text.strip()) + ' '  # So we skip the first <p>

    else:
        raise NameError("The specified 'source' is not valid")
    return headline, author, body


def fetch_page(url):
    pageHtml = requests.get(url).text
    return pageHtml


def fetch_and_parse(url, bodyLines):
    """Takes a url, and returns a parsed article with 'bodyLines' lines"""

    article = Article(url)
    article.headline, article.author, article.body = parse(url, fetch_page(url), bodyLines)
    return article
