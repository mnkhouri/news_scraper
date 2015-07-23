import news_scraper.display as display
import news_scraper.ui as ui
from news_scraper.article import Article


def test_output_to_html(tmpdir):
    outFile = tmpdir.join('output.html')
    articles = []
    Article.sourceList = set()  # Clear out sourceList from previous tests

    article = ui._get_article(bodyLines=2, debug=True, url='http://www.nytimes.com/2015/07/23/nyregion/new-york-minimum-wage-fast-food-workers.html?hp&action=click&pgtype=Homepage&module=first-column-region&region=top-news&WT.nav=top-news')
    articles.append(article)
    article = ui._get_article(bodyLines=2, debug=True, url='http://www.silive.com/news/index.ssf/2015/07/donald_trump_wealth_details_re.html#incart_river')
    articles.append(article)

    display.output_to_html(articles, outFile.relto(''))  # Get a string from outFile object by using .relto('')
    assert outFile.read() == '''<meta charset="utf-8"><b>NY TIMES</b><br><a href="http://www.nytimes.com/2015/07/23/nyregion/new-york-minimum-wage-fast-food-workers.html?hp&action=click&pgtype=Homepage&module=first-column-region&region=top-news&WT.nav=top-news">New York Plans $15-an-Hour Minimum Wage for Fast Food Workers</a> - Patrick McGeehan<br><b>SI ADVANCE</b><br><a href="http://www.silive.com/news/index.ssf/2015/07/donald_trump_wealth_details_re.html#incart_river">Donald Trump wealth details released by federal regulators</a> - Associated Press<br><br><br><a href="http://www.nytimes.com/2015/07/23/nyregion/new-york-minimum-wage-fast-food-workers.html?hp&action=click&pgtype=Homepage&module=first-column-region&region=top-news&WT.nav=top-news">New York Plans $15-an-Hour Minimum Wage for Fast Food Workers</a><br>NY TIMES - Patrick McGeehan<br>The labor protest movement that fast-food workers in New York City began nearly three years ago has led to higher wages for workers all across the country. On Wednesday, it paid off for the people who started it. A panel appointed by Gov. Andrew M. Cuomo recommended on Wednesday that the minimum wage be raised for employees of fast-food chain restaurants throughout the state to $15 an hour over the next few years. Wages would be raised faster in New York City than in the rest of the state to account for the higher cost of living there. <br><br><br><a href="http://www.silive.com/news/index.ssf/2015/07/donald_trump_wealth_details_re.html#incart_river">Donald Trump wealth details released by federal regulators</a><br>SI ADVANCE - Associated Press<br>WASHINGTON — Federal election regulators released new details Wednesday about Republican presidential candidate and celebrity businessman Donald Trump's wealth and financial holdings, weeks after he estimated his net worth at roughly $10 billion. Trump, widely believed to be the wealthiest person ever to run for president, holds leadership positions in more than 500 business entities, according to his 92-page personal financial disclosure, a report required of all presidential candidates. <br><br><br>'''
