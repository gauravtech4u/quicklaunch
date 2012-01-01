# Create your views here.
from django.contrib.comments.views.comments import post_comment
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from core.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import get_model
from djangosphinx.models import SphinxSearch
from institute.models import Institute
from django.db.models import get_model
import re
from djangosphinx.models import SphinxQuerySet
from search.models import *
from core.views import pagination
# Create your views here.


class SimpleSearch(SearchWrapperView):
    def handle_request(self):
        template = 'search/search.html'
        self.add_params()
        self.add_facets( self.request.GET.copy())
        self.add_sorting()
        self.query()
        self.facets = self.sqs.facet_counts()
        args_dict = pagination( self.request, self.sqs )
        self.save_search()
        self.sqs = None
        if self.request.GET.get( 'ajaxtype' ) == 'content':
            template = 'search/searchcontnt.html'
        if self.request.GET.get( 'ajaxtype' ) == 'facet':
            template = 'widgets/refine_facets.html'
        args_dict.update( self.__dict__ )
        return render_to_response( template, args_dict, context_instance = RequestContext( self.request ) )
        
                
    def save_search(self):
        pass
