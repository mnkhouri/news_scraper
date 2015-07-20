#!/usr/bin/env python3
# TODO: mayoral mentions
# TODO: clipboard integration
# TODO: fetch from feed (probably not rss, too polluted)

import sys
import codecs
import traceback
import collections
import time
import getopt

import pyperclip

from . import display
from . import scrape

bodyLines = 4
DEBUGMODE = False
outputFile = './output.html'
failureFile = './failedURLs.txt'


def mode_interactive():
    """Interactive Mode: terminal prompts for a source then repeatedly for a url"""
    articles = collections.OrderedDict()
    failures = []

    url = input('Enter a URL: ')
    while url != '':
        try:
            article = scrape.fetch_and_parse(url, bodyLines)
        except NameError:
            print('========= ERROR! =========\nNews source not programmed' + url + '\n')
        except Exception:
            print('========= ERROR! =========\nArticle cannot be parsed' + url + '\n')
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
    articles = collections.OrderedDict()
    failures = []

    print('Hello, this is news-scraper. Copy a URL to start!')
    print('To quit, press CTRL+C in this window.\n')
    url = pyperclip.paste()
    while True:
        try:
            tmp_value = pyperclip.paste()
            if tmp_value != url:
                url = tmp_value
                if DEBUGMODE:
                    print("Value changed: %s" % str(url)[:30])
                try:
                    article = scrape.fetch_and_parse(url, bodyLines)
                except NameError:
                    print('========= ERROR! =========\nNews source not programmed ' + url + '\n')
                except Exception:
                    print('========= ERROR! =========\nArticle cannot be parsed: ' + url + '\n')
                    failures.append(url)
                    if DEBUGMODE:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        traceback.print_exception(exc_type, exc_value, exc_traceback)
                else:
                    articles[url] = article
                    print('Got article: "' + articles[url]['headline'] + '"\n')
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    #display.output_to_term(articles)
    display.output_to_html(articles, outputFile)
    display.open_file(outputFile)
    with codecs.open(failureFile, encoding='utf-8', mode='w') as output:
        output.write('\n'.join(failures))


def usage():
    print('news-scraper')
    print('\t-l <articleLength> to set # of lines in the summary')
    print('\t-o <outputFile>    to set the destination file')
    print('\t-d                 to set debug/verbose mode')
    print('\t-i                 to use interactive mode')
    print('\t-h                 to show this help menu')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdil:o:", ["length=", "ofile="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    mode = 'clipboard'
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-d':
            global DEBUGMODE
            DEBUGMODE = True
        elif opt in ("-l", "--length"):
            global bodyLines
            bodyLines = arg
        elif opt in ("-o", "--ofile"):
            global outputFile
            outputFile = arg
        elif opt == '-i':
            mode = 'interactive'

    if mode == 'clipboard':
        mode_clipboard_watch()
    elif mode == 'interactive':
        mode_interactive()


if __name__ == "__main__":
    main()
