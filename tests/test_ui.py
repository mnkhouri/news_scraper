import news_scraper.ui as ui


class TestFetch:
    def test_bad_source(self, capsys):
        article = ui._get_article(url='http://www.google.com', bodyLines=4, debug=False)
        out, err = capsys.readouterr()
        assert article is None
        assert out == '========= ERROR! =========\n' + 'News source not programmed: http://www.google.com\n\n'

    def test_bad_article(self, capsys):
        article = ui._get_article(url='http://www.nytimes.com/blahblah', bodyLines=4, debug=False)
        out, err = capsys.readouterr()
        assert article is None
        assert out == '========= ERROR! =========\n' + 'Article cannot be parsed: http://www.nytimes.com/blahblah\n\n'

    def test_valid_article(self, capsys):
        article = ui._get_article(bodyLines=2, debug=True, url='http://www.nytimes.com/2015/10/16/sports/gambling-regulators-block-daily-fantasy-sites-in-nevada.html')
        out, err = capsys.readouterr()
        assert article.headline == 'Nevada Says It Will Treat Daily Fantasy Sports Sites as Gambling'
        assert article.author == 'Joe Drape'
        assert article.body == 'Nevada regulators ruled on Thursday that playing daily fantasy sports should be considered gambling, not a game of skill, and ordered websites like DraftKings and FanDuel to stop operating immediately in the state until the companies and their employees receive state gambling licenses. It is perhaps the most significant setback yet for a booming, unregulated industry that has spent the past two weeks in the midst of allegations that have prompted federal and state investigations into whether its employees, armed with inside information, exploited paying customers. '
        assert article.source == 'NY Times'
        assert article.url == 'http://www.nytimes.com/2015/10/16/sports/gambling-regulators-block-daily-fantasy-sites-in-nevada.html'
        assert out == 'Got article: "Nevada Says It Will Treat Daily Fantasy Sports Sites as Gambling"\n\n'

    def test_mayoral_article(self, capsys):
        article = ui._get_article(bodyLines=2, debug=True, url='http://www.nytimes.com/2015/07/23/nyregion/new-york-minimum-wage-fast-food-workers.html?hp&action=click&pgtype=Homepage&module=first-column-region&region=top-news&WT.nav=top-news')
        try:
            out, err = capsys.readouterr()
        except IOError:
            pass
        assert article.headline == 'New York Plans $15-an-Hour Minimum Wage for Fast Food Workers'
        assert article.author == 'Patrick McGeehan'
        assert article.body == 'The labor protest movement that fast-food workers in New York City began nearly three years ago has led to higher wages for workers all across the country. On Wednesday, it paid off for the people who started it. A panel appointed by Gov. Andrew M. Cuomo recommended on Wednesday that the minimum wage be raised for employees of fast-food chain restaurants throughout the state to $15 an hour over the next few years. Wages would be raised faster in New York City than in the rest of the state to account for the higher cost of living there. '
        assert article.source == 'NY Times'
        assert article.url == 'http://www.nytimes.com/2015/07/23/nyregion/new-york-minimum-wage-fast-food-workers.html?hp&action=click&pgtype=Homepage&module=first-column-region&region=top-news&WT.nav=top-news'
        assert out == 'This article contains a Mayoral mention!\nDo you want to see the mentioned lines?  [y/n]:'
