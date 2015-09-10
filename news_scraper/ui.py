import codecs
import traceback
import time
import sys

import pyperclip

from . import display
from . import scrape


def _get_article(url, bodyLines=4, debug=False):
    try:
        article = scrape.fetch_and_parse(url, bodyLines)
    except NameError:
        if debug:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        print('========= ERROR! =========\nNews source not programmed: ' + url + '\n')
    except Exception:
        print('========= ERROR! =========\nArticle cannot be parsed: ' + url + '\n')
        if debug:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    else:
        print('Got article: "' + article.headline + '"\n')
        return article


def _output(articles, outputFile, failures, failureFile):
    #display.output_to_term(articles)
    display.output_to_html(articles, outputFile)
    display.open_file(outputFile)
    with codecs.open(failureFile, encoding='utf-8', mode='w') as output:
        output.write('\n'.join(failures))


def mode_interactive(options):
    """Interactive Mode: terminal prompts repeatedly for a url to fetch"""
    articles = []
    failures = []

    url = input('Enter a URL: ')
    while url != '':
        article = _get_article(url=url, bodyLines=options.bodyLines, debug=options.debug)
        if (article):
            articles.append(article)
        else:
            failures.append(url)
        url = input("Enter a URL (press enter to end): ")

    _output(articles, options.outputFile, failures, options.failureFile)


def mode_clipboard_watch(options):
    """Clipboard Watch Mode: watches for a new string on the clipboard, and tries to fetch that URL"""
    articles = []
    failures = []

    print('Hello, this is news-scraper. Copy a URL to start!')
    print('To quit, press CTRL+C in this window.\n')
    url = pyperclip.paste()
    while True:
        try:
            tmp_value = pyperclip.paste()
            if tmp_value != url:
                url = tmp_value
                print("Fetching article...")
                if options.debug:
                    print("Value changed: %s" % str(url)[:100])

                article = _get_article(url=url, bodyLines=options.bodyLines, debug=options.debug)
                if (article):
                    articles.append(article)
                else:
                    failures.append(url)
                    time.sleep(0.1)
        except KeyboardInterrupt:
            break

    _output(articles, options.outputFile, failures, options.failureFile)
