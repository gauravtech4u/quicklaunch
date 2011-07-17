from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('search.views',
        
        url(r'allsearches/$','allsearches',name='allsearches'),
        
        url(r'(?P<app>[-\w]+)/(?P<model_name>[-\w]+)/(?P<q>[-\S]+)/$', 'search', name="savedsearch"),
        
        url(r'(?P<app>[-\w]+)/(?P<model_name>[-\w]+)/$', 'search', name="search"),
        
        url(r'site/$', 'sitesearch', name="sitesearch"),
        
        url(r'$', 'search', name="search_institute"),
        
        
)