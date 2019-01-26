import requests
from bs4 import BeautifulSoup
import datetime

def scrapeHeadlinesLong():
    response = requests.get("http://www.spiegel.de")
    content = response.content
    scraper = BeautifulSoup(content, "html.parser")
    headlines_long = scraper.select(".headline")
    headlines_long_list = []
    for entry in headlines_long:
        if entry.text != "":
            headlines_long_list.append(entry.text)
    return (headlines_long_list, getTime())

def scrapeHeadlinesShort():
    response = requests.get("http://www.spiegel.de")
    content = response.content
    scraper = BeautifulSoup(content, "html.parser")
    headlines_short = scraper.select(".headline")
    headlines_short_list = []
    for entry in headlines_short:
        if entry.text != "":
            headlines_short_list.append(entry.text)
    return (headlines_short_list, getTime())

def getTime():
    now = datetime.datetime.now()
    return now.isoformat()
