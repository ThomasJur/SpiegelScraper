import requests
from bs4 import BeautifulSoup
import datetime

def scrapeArticleSPON():
    response = requests.get("https://www.spiegel.de")
    scraper = BeautifulSoup(response.content, "html.parser")
    query = scraper.select(".teaser")
    for ind, element in enumerate(query):
        if element.text is not None:
            headline, text, link = getFeaturesSPON(element)
            if not ((headline=="no") or (text == "no") or (link == "no")):
                print("Article {} \n".format(ind+1) + "Headline: " + headline + "\n" + "Link: " + link + "\n" + "Text: " + text + "\n")

def getTime():
    now = datetime.datetime.now()
    return now.isoformat()

def getFeaturesSPON(in_query):
    if in_query.find("a"):
        if in_query.a.has_attr("title"):
            headline = in_query.a["title"]
        else:
            headline="no"
    else:
        headline = "no"
    if in_query.find("a"):    
        link = "http://www.spiegel.de" + in_query.a["href"]
    else:
        link = "no"
    if in_query.find("p"):
        text = in_query.p.text.strip()
    else:
        text = "no"
    return (headline, text, link)
