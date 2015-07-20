import news_scraper.display as display


def test_set_from_dict_attribute():
    testDict = {
        'Marc': {'favorite': 'mango', 'dislikes': 'apple'},
        'John': {'favorite': 'apple'},
        'Xavier': {'favorite': 'apple'},
    }
    assert display.set_from_dict_attribute(testDict, 'favorite') == set(['apple', 'mango'])
