#!/usr/bin/env python3
# TODO: split body based on '. ' (period space or period newline), not <p> tags
# TODO: mayoral mentions + 1 line context before/after
# TODO: put clipboard check in a separate thread so it never misses an entry

import sys
import getopt

from . import ui


class Options:
    def __init__(self):
        self.bodyLines = 4
        self.debug = False
        self.outputFile = './output.html'
        self.failureFile = './manualURLs.html'


def usage():
    print('news-scraper')
    print('\t -l <articleLength> to set # of lines in the summary')
    print('\t -o <outputFile>    to set the destination file')
    print('\t -d                 to set debug/verbose mode')
    print('\t -i                 to use interactive mode')
    print('\t -h                 to show this help menu')


def main():
    options = Options()

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
            options.debug = True
        elif opt in ("-l", "--length"):
            options.bodyLines = arg
        elif opt in ("-o", "--ofile"):
            options.outputFile = arg
        elif opt == '-i':
            mode = 'interactive'

    if mode == 'clipboard':
        ui.mode_clipboard_watch(options)
    elif mode == 'interactive':
        ui.mode_interactive(options)


if __name__ == "__main__":
    main()
