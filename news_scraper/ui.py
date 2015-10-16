import codecs
import traceback
import time
import sys
from distutils.util import strtobool

import pyperclip

from . import display
from . import scrape
from .article import Article


def prompt(query):
    print(query, ' [y/n]: ', end='')
    val = input()
    try:
        ret = strtobool(val)
    except ValueError:
        print('Please answer with a y/n')
        return prompt(query)
    return ret


def _get_article(url, bodyLines=4, debug=False):
    try:
        data = scrape.fetch_and_parse(url, bodyLines)
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
        article = Article(url)
        article.addData(data)
        if(article.mayoralMention or article.departmentalMention):
            print('This article contains a ' + ('Mayoral ' if article.mayoralMention else 'departmental ') + 'mention!')
            if(prompt('Do you want to see the mentioned lines?')):
                if(article.mayoralMention):
                    print('Mayoral mentions:')
                    print('\n'.join(article.mayoralText))
                if(article.departmentalMention):
                    print('Departmental mentions:')
                    print('\n'.join(article.departmentalText))
            if(prompt('Do you want to handle this article yourself?')):
                print('Adding article to manual handling list.\n')
                return False
        print('Got article: "' + article.headline + '"\n')
        return article


def _check_for_deblasio(article):
    pass


def _output(articles, outputFile, failures, failureFile):
    display.output_failures_to_html(failures, failureFile)
    display.open_file(failureFile)
    #display.output_articles_to_term(articles)
    display.output_articles_to_html(articles, outputFile)
    display.open_file(outputFile)


def mode_interactive(options):
    """Interactive Mode: terminal prompts repeatedly for a url to fetch"""
    articles = set()
    failures = set()

    url = input('Enter a URL: ')
    while url != '':
        article = _get_article(url=url, bodyLines=options.bodyLines, debug=options.debug)
        if (article):
            articles.add(article)
        else:
            failures.add(url)
        url = input('Enter a URL (press enter to end): ')

    _output(articles, options.outputFile, failures, options.failureFile)


def mode_clipboard_watch(options):
    """Clipboard Watch Mode: watches for a new string on the clipboard, and tries to fetch that URL"""
    articles = set()
    failures = set()

    print('Hello, this is news-scraper. Copy a URL to start!')
    print('To quit, press CTRL+C in this window.\n')
    url = pyperclip.paste()
    while True:
        try:
            tmp_value = pyperclip.paste()
            if tmp_value != url:
                url = tmp_value
                print('Fetching article...')
                if options.debug:
                    print("Value changed: %s" % str(url)[:100])

                article = _get_article(url=url, bodyLines=options.bodyLines, debug=options.debug)
                if (article):
                    articles.add(article)
                else:
                    failures.add(url)
                    time.sleep(0.2)
        except KeyboardInterrupt:
            break

    _output(articles, options.outputFile, failures, options.failureFile)
