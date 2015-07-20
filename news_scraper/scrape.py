from bs4 import BeautifulSoup
from urllib.parse import urlparse

import requests


def getSourceFromUrl(url):
    host = urlparse(url).hostname
    try:
        source = {
            'www.nytimes.com': 'NY Times',
            'www.nydailynews.com': 'Daily News'
        }[host]
    except KeyError:
        raise NameError("This news source is not programmed yet")
    return source


def parse(source, pageHtml, bodyLines):
    soup = BeautifulSoup(pageHtml, "lxml")
    if source == 'Daily News':
        headline = soup.find(itemprop="headline").string
        try:
            author = soup.find(rel="author").string.strip()
        except AttributeError:
            author = soup.find(id="a-credits").string.strip()
        rawBody = soup.find_all('p', limit=bodyLines)
        body = ''
        for i in range(bodyLines):
            body += (rawBody[i].text.strip()) + ' '
    elif source == 'NY Times':
        headline = soup.find(itemprop="headline").string
        author = soup.find(attrs={"name": "author"})['content'].strip()  # Author is in the tag itself
        rawBody = soup.find_all(attrs={"class": "story-body-text story-content"}, limit=bodyLines)
        body = ''
        for i in range(bodyLines):
            body += (rawBody[i].text) + ' '
    else:
        raise NameError("The specified 'source' is not valid")
    return headline, author, body


def fetch_page(url):
    pageHtml = requests.get(url).text
    return pageHtml


def fetch_and_parse(url, bodyLines):
    """Takes a url, and returns a parsed article with 'bodyLines' lines"""

    article = {'url': url}
    article['source'] = getSourceFromUrl(url)
    article['headline'], article['author'], article['body'] = parse(article['source'], fetch_page(url), bodyLines)
    return article
