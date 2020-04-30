import requests
from bs4 import BeautifulSoup

def toiIndia():
    toiRequestWorld=requests.get("https://timesofindia.indiatimes.com/briefs/india")
    soup = BeautifulSoup(toiRequestWorld.content, 'html.parser')
    # headings = soup.find("div", {"class": "briefs_outer clearfix"})
    hx= soup.find_all("div", {"class": "brief_box"})
    toi={}
    for i in hx:
        try:
            title=i.h2.text
            summary=i.p.text
            url=i.a['href']
            imgSrc = i.find_all("div", {"class": "posrel"})[0].img['data-src']
            toi[title]=[imgSrc,summary,url]
        except:
            continue
    return toi
