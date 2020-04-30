from pyramid.view import view_config
from .scrapers.toi import *
papers={'toi':'Times of India','ht':'Hindustan Times'}
@view_config(route_name='home', renderer='templates/index.jinja2')
@view_config(route_name='paper', renderer='templates/index.jinja2')
def my_view(request):
    toi_news={}
    try:
        paperName=papers[request.matchdict['paperName']]
        if request.matchdict['paperName']=='toi':
            toi_news=toiIndia()
            return {'paperName':paperName,'toi_news':toi_news}
        if request.matchdict['paperName']=='ht':
            return {'paperName':paperName,'toi_news':toi_news}
    except:
        paperName="Front Page"
        return {'paperName':paperName,'toi_news':toi_news}