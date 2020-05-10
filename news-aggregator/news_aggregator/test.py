import requests
from bs4 import BeautifulSoup

news = {}
htRequest = requests.get("https://www.hindustantimes.com/india-news/")
soup = BeautifulSoup(htRequest.content, "html.parser")
allDetails = soup.find("div", {"id": "scroll-container"})
ul = allDetails.find("ul")
li = ul.find_all("li")
for i in li:
    try:
        img = i.find("div", {"class": "media-left"}).a.img["src"]
        url = i.find("div", {"class": "media-left"}).a["href"]
        title = i.find("div", {"class": "media-body"}).div.text
        summary = (i.find("div", {"class": "media-body"}).p.text) or (
            "No summary available"
        )
        news[title] = [img, summary, url]
    except:
        continue
