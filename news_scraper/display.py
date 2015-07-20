import os
import sys
import subprocess
import codecs


def make_hyperlink(url, text):
    hyperlink = '<a href="' + url + '">' + text + '</a>'
    return(hyperlink)


def set_from_dict_attribute(dictionary, attribute):
    keys = dictionary.keys()
    return set(dictionary[key][attribute] for key in keys)


def output_to_html(articles, outFile):
    sources = set_from_dict_attribute(articles, 'source')

    with codecs.open(outFile, encoding='utf-8', mode='w') as output:
        output.write('<meta charset="utf-8">')

        for source in sources:
            output.write(source.upper() + '<br><br>')
            for url, article in articles.items():
                if article['source'] == source:
                    output.write(make_hyperlink(article['url'], article['headline']) + ' - ' + article['author'] + '<br>')

            output.write('<br><br>')
            for url, article in articles.items():
                if article['source'] == source:
                    output.write(make_hyperlink(article['url'], article['headline']) + '<br>')
                    output.write(source.upper() + ' - ' + article['author'] + '<br>')
                    output.write(article['body'] + '<br><br>')

            output.write('<br>')


def output_to_term(articles):
    sources = set_from_dict_attribute(articles, 'source')

    print("\n================================================================================")
    print("--------------------------------- Output ---------------------------------------")
    print("================================================================================")

    for source in sources:
        print(source.upper() + '\n')
        for url, article in articles.items():
            if article['source'] == source:
                print(article['headline'] + ' - ' + article['author'])

        print('\n\n')
        for url, article in articles.items():
            if article['source'] == source:
                print(article['headline'])
                print(source.upper() + ' - ' + article['author'])
                print(article['body'] + '\n')


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
