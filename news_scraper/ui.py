import codecs
import traceback
import collections
import time
import sys

import pyperclip

from . import display
from . import scrape


def mode_interactive(options):
    """Interactive Mode: terminal prompts for a source then repeatedly for a url"""
    articles = []
    failures = []

    url = input('Enter a URL: ')
    while url != '':
        try:
            article = scrape.fetch_and_parse(url, options.bodyLines)
        except NameError:
            if options.debug:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
            print('========= ERROR! =========\nNews source not programmed: ' + url + '\n')
        except Exception:
            print('========= ERROR! =========\nArticle cannot be parsed: ' + url + '\n')
            failures.append(url)
            if options.debug:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        else:
            articles.append(article)
            print('Got article: "' + article.headline + '"\n')
        url = input("Enter a URL (press enter to end): ")

    #display.output_to_term(articles)
    display.output_to_html(articles, options.outputFile)
    display.open_file(options.outputFile)
    with codecs.open(options.failureFile, encoding='utf-8', mode='w') as output:
        output.write('\n'.join(failures))


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
                    print("Value changed: %s" % str(url)[:30])
                try:
                    article = scrape.fetch_and_parse(url, options.bodyLines)
                except NameError:
                    if options.debug:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        traceback.print_exception(exc_type, exc_value, exc_traceback)
                    print('========= ERROR! =========\nNews source not programmed: ' + url + '\n')
                except Exception:
                    print('========= ERROR! =========\nArticle cannot be parsed: ' + url + '\n')
                    failures.append(url)
                    if options.debug:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        traceback.print_exception(exc_type, exc_value, exc_traceback)
                else:
                    articles.append(article)
                    print('Got article: "' + article.headline + '"\n')
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    #display.output_to_term(articles)
    display.output_to_html(articles, options.outputFile)
    display.open_file(options.outputFile)
    with codecs.open(options.failureFile, encoding='utf-8', mode='w') as output:
        output.write('\n'.join(failures))
