from pyramid.view import view_config
import requests
from bs4 import BeautifulSoup

papers = {"toi": "Times of India", "ht": "Hindustan Times"}
toiCategories = {
    "world": "World News",
    "india": "India News",
    "sports": "Sports News",
    "entertainment": "Entertainment News",
}


@view_config(route_name="home", renderer="templates/home.jinja2")
def home(request):
    paperName = "Front Page"
    return {"paperName": paperName, "papers": papers}


@view_config(route_name="paper", renderer="templates/index.jinja2")
@view_config(
    route_name="paper", renderer="templates/index.jinja2", request_method="POST"
)
def toi(request):
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
        # headings = soup.find("div", {"class": "briefs_outer clearfix"})
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
            "toiCategories": toiCategories,
        }
    if request.matchdict["paperName"] == "ht":
        news = {}
        return {"paperName": paperName, "papers": papers, "news": news}
