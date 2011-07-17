from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from voting.views import vote_on_object
from institute.models import Institute
from event.models import Event
from article.models import Article
import views

institute_dict = {
    'model': Institute,
    'template_object_name': 'institute',
}

article_dict = {
    'model': Article,
    'template_object_name': 'article',
}

event_dict = {
    'model': Event,
    'template_object_name': 'event',
}




urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls),name="core_admin"),
        
        #url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'education/home.html'},name="index"),
        
        url(r'^comment/(?P<app>[-\w]+)/(?P<model_name>[-\w]+)/(?P<slug>[-\w]+)/$', 'core.views.submit_comment',name='submit_comment'),
        
        url(r'^refine_data/$', 'core.views.refine_data',name='refine_data'),
        
        url(r'^listing/(?P<app>[-\w]+)/(?P<model_name>[-\w]+)/(?P<category>[-\w]+)/$', 'core.views.generic_list', name='generic_list'),
        
        url(r'^popular/(?P<app>[-\w]+)/(?P<model_name>[-\w]+)/$', 'core.views.data_by_voting_list', name='data_by_voting_list'),
        
        url(r'^listing/(?P<app>[-\w]+)/(?P<model_name>[-\w]+)/(?P<category>[-\w]+)/(?P<state>[-\w]+)/$', 'core.views.generic_list', name='generic_list'),
        
        url(r'^listing/(?P<app>[-\w]+)/(?P<model_name>[-\w]+)/$', 'core.views.generic_list', name='generic_list'),
        
        url(r'^detail/(?P<app>[-\w]+)/(?P<model_name>[-\w]+)/(?P<instance_slug>[-\w]+)/$', 'core.views.generic_detail', name='generic_detail'),
        
        url(r'^institute/Institute/(?P<object_id>.+)/(?P<direction>up|down|clear)/?$', vote_on_object, institute_dict, name='institute_vote'),
                
        url(r'^article/Article/(?P<object_id>.+)/(?P<direction>up|down|clear)/?$', vote_on_object, article_dict, name='article_vote'),
        
        url(r'^event/Event/(?P<object_id>.+)/(?P<direction>up|down|clear)/?$', vote_on_object, event_dict, name='event_vote'),
        
        url(r'^contact_us/$', 'core.views.contact_us',name='contactus'),
        
        url(r'^policy/$', 'django.views.generic.simple.direct_to_template', {'template': 'policy.html'},name="privacy_policy"),
        
        url(r'^terms/$', 'django.views.generic.simple.direct_to_template', {'template': 'terms.html'},name="terms"),
        
)