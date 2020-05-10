from pyramid.view import view_config
import requests
from bs4 import BeautifulSoup
import pyramid.httpexceptions as exc

papers = {"toi": "Times of India", "ht": "Hindustan Times"}
categories = {
    "world": "World News",
    "india": "India News",
    "sports": "Sports News",
    "business": "Business News",
}


@view_config(route_name="home", renderer="templates/index.jinja2")
def home(request):
    paperName = "Front Page"
    return {"paperName": paperName, "papers": papers}


@view_config(route_name="paper", renderer="templates/paper.jinja2")
@view_config(
    route_name="paper", renderer="templates/paper.jinja2", request_method="POST"
)
def newsScraper(request):
    paperName = papers[request.matchdict["paperName"]]
    if request.matchdict["paperName"] == "toi":
        news = {}
        if request.POST:
            print(request.POST.get("category"))
            toiRequest = requests.get(
                "https://timesofindia.indiatimes.com/briefs/"
                + request.POST.get("category")
            )
        else:
            toiRequest = requests.get(
                "https://timesofindia.indiatimes.com/briefs/world"
            )
        soup = BeautifulSoup(toiRequest.content, "html.parser")
        allDetails = soup.find_all("div", {"class": "brief_box"})
        for i in allDetails:
            try:
                title = i.h2.text
                summary = i.p.text
                url = i.a["href"]
                imgSrc = i.find_all("div", {"class": "posrel"})[0].img["data-src"]
                news[title] = [imgSrc, summary, url]
            except:
                continue
        return {
            "paperName": paperName,
            "papers": papers,
            "news": news,
            "categories": categories,
        }
    elif request.matchdict["paperName"] == "ht":
        news = {}
        if request.POST:
            htRequest = requests.get(
                "https://www.hindustantimes.com/"
                + request.POST.get("category")
                + "-news/"
            )
        else:
            htRequest = requests.get("https://www.hindustantimes.com/world-news/")
        # htRequest = requests.get("https://www.hindustantimes.com/india-news/")
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
        return {
            "paperName": paperName,
            "papers": papers,
            "news": news,
            "categories": categories,
        }
