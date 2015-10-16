import news_scraper.display as display
import news_scraper.ui as ui
from news_scraper.article import Article


def test_output_to_html(tmpdir):
    outFile = tmpdir.join('output.html')
    articles = []
    Article.sourceList = set()  # Clear out sourceList from previous tests

    article = ui._get_article(bodyLines=2, debug=True, url='http://www.nytimes.com/2015/10/16/sports/gambling-regulators-block-daily-fantasy-sites-in-nevada.html')
    articles.append(article)
    article = ui._get_article(bodyLines=2, debug=True, url='http://www.silive.com/news/index.ssf/2015/07/donald_trump_wealth_details_re.html#incart_river')
    articles.append(article)

    display.output_articles_to_html(articles, outFile.relto(''))  # Get a string from outFile object by using .relto('')
    assert outFile.read() == '''<meta charset="utf-8"><b>NY TIMES</b><br><a href="http://www.nytimes.com/2015/10/16/sports/gambling-regulators-block-daily-fantasy-sites-in-nevada.html">Nevada Says It Will Treat Daily Fantasy Sports Sites as Gambling</a> - Joe Drape<br><b>SI ADVANCE</b><br><a href="http://www.silive.com/news/index.ssf/2015/07/donald_trump_wealth_details_re.html#incart_river">Donald Trump wealth details released by federal regulators</a> - Associated Press<br><br><br><a href="http://www.nytimes.com/2015/10/16/sports/gambling-regulators-block-daily-fantasy-sites-in-nevada.html">Nevada Says It Will Treat Daily Fantasy Sports Sites as Gambling</a><br>NY TIMES - Joe Drape<br>Nevada regulators ruled on Thursday that playing daily fantasy sports should be considered gambling, not a game of skill, and ordered websites like DraftKings and FanDuel to stop operating immediately in the state until the companies and their employees receive state gambling licenses. It is perhaps the most significant setback yet for a booming, unregulated industry that has spent the past two weeks in the midst of allegations that have prompted federal and state investigations into whether its employees, armed with inside information, exploited paying customers. <br><br><br><a href="http://www.silive.com/news/index.ssf/2015/07/donald_trump_wealth_details_re.html#incart_river">Donald Trump wealth details released by federal regulators</a><br>SI ADVANCE - Associated Press<br>WASHINGTON — Federal election regulators released new details Wednesday about Republican presidential candidate and celebrity businessman Donald Trump's wealth and financial holdings, weeks after he estimated his net worth at roughly $10 billion. Trump, widely believed to be the wealthiest person ever to run for president, holds leadership positions in more than 500 business entities, according to his 92-page personal financial disclosure, a report required of all presidential candidates. <br><br><br>'''
