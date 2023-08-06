__version__ = '0.1.1'

import bs4
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

class News:
    def news(self):
        url = "https://news.google.com/news/rss"
        client = urlopen(url)
        xml_page = client.read()
        client.close()
        page = bs4.BeautifulSoup(xml_page, 'xml')
        news_list = page.findAll("item")
        headlines=""
        for news in news_list:
            headlines+=news.title.text
        return headlines