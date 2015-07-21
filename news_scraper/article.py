from urllib.parse import urlparse


class Article:
    sourceList = set()

    def __init__(self, url):
        self.url = url
        self.source = self.getSourceFromUrl()
        self.sourceList.add(self.source)

        self.headline = None
        self.author = None
        self.body = None
        self.mayoralMention = None
        self.mayoralText = None

    def getSourceFromUrl(self):
        host = urlparse(self.url).hostname
        try:
            source = {
                'www.nytimes.com': 'NY Times',
                'www.nydailynews.com': 'Daily News',
                'www.dnainfo.com': 'DNA Info',
                'www.silive.com': 'SI Advance'
            }[host]
        except KeyError:
            raise NameError("This news source is not programmed yet")
        return source
