from news_scraper.article import Article


class TestSourceDetermination:
    def test_nyt(self):
        article = Article('http://www.nytimes.com/2015/07/20/world/middleeast/')
        assert article.source == 'NY Times'

    def test_dn(self):
        article = Article('http://www.nydailynews.com/new-york/businessman-charged-dwi-crash-killed-4-women-article-1.2297057')
        assert article.source == 'Daily News'

    def test_sourceList(self):
        assert Article.sourceList == set(['Daily News', 'NY Times'])
