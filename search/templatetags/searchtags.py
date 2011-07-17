from django.template import Library, Node
from django.db.models import get_model
import re
from django.core.cache import cache
from django import template
register = Library()
from django.views.decorators.cache import cache_page
from django.template import TemplateSyntaxError
from django.db.models import Count
from django.contrib.auth.models import ContentType
from search.models import *
from djangosphinx.models import SphinxQuerySet
from djangosphinx.models import SphinxSearch
from institute.models import Institute
from article.models import Article
import random

class GenericSearchContentNode(Node):
    def __init__(self, model,term, varname):
        self.varname = varname
        self.term=template.Variable(term)
        self.model = get_model(*model.split('.'))
        
    def render(self, context):
        search_term=self.term.resolve(context).strip('\\')
        result=list(self.model.search.query(search_term))[:20]
        
        if len(result) == 0 :
            result=list(self.model.search.query('institute'))[:20]
 
        context[self.varname]=result
        return ''
 
def get_generic_searches(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "second argument to get_latest tag must be 'as'"
    return GenericSearchContentNode(bits[1], bits[2],bits[4])
    

class GenericAnotherSearchContentNode(Node):
    def __init__(self, model,app,term, varname):
        self.varname = varname
        self.term=template.Variable(term)
        self.model = template.Variable(model)
        self.app = template.Variable(app)

    def render(self, context):
        self.model = self.model.resolve(context)
        self.app  = self.app.resolve(context)
        self.model = get_model(self.app,self.model)
        search_term=self.term.resolve(context).strip('\\')
        result=list(self.model.search.query(search_term))[:20]

        if len(result) == 0 :
            result=list(self.model.search.query('institute'))[:20]

        context[self.varname]=result
        return ''

def get_another_generic_searches(parser, token):
    bits = token.contents.split()
    if len(bits) != 6:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[4] != 'as':
        raise TemplateSyntaxError, "second argument to get_latest tag must be 'as'"
    return GenericAnotherSearchContentNode(bits[1], bits[2],bits[3],bits[5])


register.tag(get_generic_searches)
register.tag(get_another_generic_searches)