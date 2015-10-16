from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='news_scraper',
    version='0.3.0',
    description='Generates short snippets of news articles',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='news scraper',
    url='http://github.com/mnkhouri/news_scraper',
    author='Marc Khouri',
    author_email='marc@khouri.ca',
    license='GPLv2',
    packages=['news_scraper'],
    install_requires=[
        'beautifulsoup4',
        'requests',
        'lxml',
        'pyperclip'
    ],
    scripts=['bin/news-scraper'],
    include_package_data=True,
    zip_safe=False)
