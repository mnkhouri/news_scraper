import news_scraper.scrape as scrape


class TestScrape:
    def test_Daily_News(self):
        article = scrape.fetch_and_parse('http://www.nydailynews.com/new-york/businessman-charged-dwi-crash-killed-4-women-article-1.2297057', 4)
        assert article.url == 'http://www.nydailynews.com/new-york/businessman-charged-dwi-crash-killed-4-women-article-1.2297057'
        assert article.source == 'Daily News'
        assert article.headline == 'Long Island limousine crash victims were best pals with bright futures; accused drunken driver pleads not guilty to DWI'
        assert article.author == 'Keldy Ortiz'
        assert article.body == '''They were eight friends with bright futures celebrating a bride-to-be — until an alleged drunken driver smashed into their limousine, killing four and devastating their Long Island communities. Brittney Schulman, 23, and Lauren Baruch, 24, both of Smithtown; Stephanie Belli, 23, of Kings Park, and Amy Grabina, 23, of Commack, were leaving Vineyard 48 winery on the North Fork of Long Island when Steven Romeo rammed his red pickup truck into their stretch ride, the Southhold Town Police Department said Sunday. Steve Romeo (L), pleaded not guilty to DWI. Elizabeth Miller (R), Suffolk County assistant district attorney with the Vehicular Crimes Bureau speaks to the media on Sunday.  '''
