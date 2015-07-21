import os
import sys
import subprocess
import codecs

from .article import Article


def make_hyperlink(url, text):
    hyperlink = '<a href="' + url + '">' + text + '</a>'
    return(hyperlink)


def output_to_html(articles, outFile):
    with codecs.open(outFile, encoding='utf-8', mode='w') as output:
        output.write('<meta charset="utf-8">')

        for source in Article.sourceList:
            output.write(source.upper() + '<br><br>')
            filteredArticles = (article for article in articles if article.source == source)
            for article in filteredArticles:
                output.write(make_hyperlink(article.url, article.headline) + ' - ' + article.author + '<br>')

            output.write('<br><br>')
            for article in filteredArticles:
                output.write(make_hyperlink(article.url, article.headline) + '<br>')
                output.write(source.upper() + ' - ' + article.autho + '<br>')
                output.write(article.body + '<br><br>')

            output.write('<br>')


def output_to_term(articles):
    print("\n================================================================================")
    print("--------------------------------- Output ---------------------------------------")
    print("================================================================================")

    for source in Article.sourceList:
        print(source.upper() + '\n')
        filteredArticles = (article for article in articles if article.source == source)
        for article in filteredArticles:
            print(article.headline + ' - ' + article.author)

        print('\n\n')
        for article in filteredArticles:
            print(article.headline)
            print(source.upper() + ' - ' + article.autho)
            print(article.body + '\n')


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
