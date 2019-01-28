import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
from sqlite3 import Error

# statements for sql inserts/queries
sql_insert = "INSERT INTO spon (headline, link, article_short, date) VALUES(?,?,?,?)"

def scrapeArticleSPON():
    response = requests.get("https://www.spiegel.de")
    scraper = BeautifulSoup(response.content, "html.parser")
    query = scraper.select(".teaser")
    #esatblishing database connection
    conn = connect_db()
    for ind, element in enumerate(query):
        if element.text is not None:
            headline, text, link = getFeaturesSPON(element)
            c = conn.cursor()
            if not ((headline=="no") or (text == "no") or (link == "no")):
                print("Article {} \n".format(ind+1) + "Headline: " + headline + "\n" + "Link: " + link + "\n" + "Text: " + text + "\n")
                if rowExists(conn, headline):
                    c.execute(sql_insert,(headline, link, text, str(getTime())))
    conn.commit()
    conn.close()

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
        if in_query.a["href"][:4] == "http":
            link = in_query.a["href"]
        else:
            link = "http://www.spiegel.de" + in_query.a["href"]
    else:
        link = "no"
    if in_query.find("p"):
        text = in_query.p.text.strip()
    else:
        text = "no"
    return (headline, text, link)

def connect_db():
    try:
        conn = sqlite3.connect("/home/Raketenpaule/mysite/SpiegelScraper/db/spon.db")
    except Error as e:
        print(e)
    return conn

def rowExists(conn, headline):
    c = conn.cursor()
    row = c.execute("SELECT * FROM spon WHERE (headline=?)", (headline,)).fetchone()
    if row is None:
        return True
    else:
        return False


if __name__=="__main__":
    scrapeArticleSPON()
