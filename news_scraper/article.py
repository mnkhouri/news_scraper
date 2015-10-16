from urllib.parse import urlparse


class Article:
    sourceList = set()

    def __init__(self, url):
        self.url = url
        self.source = self.get_source_from_url()
        self.sourceList.add(self.source)

        self.headline = None
        self.author = None
        self.body = None
        self.mayoralMention = None
        self.mayoralText = None
        self.departmentalMention = None
        self.departmentalText = None

    def addData(self, entries):
        self.__dict__.update(entries)

    def get_source_from_url(self):
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

    def __eq__(self, other):
        if isinstance(other, Article):
            return ((self.url == other.url) and (self.body == other.body))
        else:
            return False

    def __hash__(self):
        return hash(self.url)
