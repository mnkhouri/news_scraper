#!/usr/bin/env python3
# TODO: mayoral mentions
# TODO: clipboard integration
# TODO: fetch from feed (probably not rss, too polluted)

import sys
import codecs
import traceback
import collections

from . import display
from . import scrape

bodyLines = 4
DEBUGMODE = 'Verbose'  # Can be True, False, or 'Verbose'
outputFile = './output.html'
failureFile = './failedURLs.txt'
sources = ["Daily News", "NY Times"]


class Article:
    def __init__(self, url, source, headline, author, body):
        self.url = url
        self.source = source
        self.headline = headline
        self.author = author
        self.body = body


def mode_interactive():
    """Interactive Mode: terminal prompts for a source then repeatedly for a url"""
    articles = collections.OrderedDict()
    failures = []

    url = input('\nEnter a URL: ')
    #url = 'http://www.nytimes.com/2015/07/01/nyregion/uber-says-proposed-freeze-on-licenses-would-limit-competition.html?ref=nyregion'
    while url != '':
        try:
            article = scrape.fetch_and_parse(url, bodyLines)
        except Exception:
            print('========= ERROR! =========\nArticle cannot be parsed')
            failures.append(url)
            if DEBUGMODE:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        else:
            articles[url] = article
            print('Got article: "' + articles[url]['headline'] + '"\n')
        url = input("Enter a URL (press enter to end): ")

    #display.output_to_term(articles)
    display.output_to_html(articles, outputFile)
    display.open_file(outputFile)
    with codecs.open(failureFile, encoding='utf-8', mode='w') as output:
        output.write('\n'.join(failures))


def mode_clipboard_watch():
    """Clipboard Watch Mode: watches for a new string on the clipboard, and tries to fetch that URL"""
    pass


def main():
    mode_interactive()


if __name__ == "__main__":
    main()
