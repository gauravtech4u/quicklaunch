from django.template import Library, Node
from django.db.models import get_model
import re
from django.core.cache import cache
from django import template
register = Library()
from django.views.decorators.cache import cache_page
from django.template import TemplateSyntaxError
from voting.models import Vote
from django.db.models import Count
from django.contrib.auth.models import ContentType
from core.models import Quote
from search.models import *
from django.template import Context
import random

class GenericContentNode(Node):
    def __init__(self,*args):
        if len(args) == 5:
            self.varname = args[4]
            self.args=re.sub("\'","",args[2])
            self.model = get_model(*args[1].split('.'))
            self.obj_arg=None
        else:
            self.varname = args[5]
            self.args=re.sub("\'","",args[2])
            self.model = get_model(*args[1].split('.'))
            self.obj_arg=template.Variable(args[3])
    def render(self, context):
        kwargs={}
        if self.args !='':
            kwargs=dict(item.split("=") for item in self.args.split(";"))
        if self.obj_arg:
            kwargs['type']=self.obj_arg.resolve(context)
        context[self.varname] = self.model._default_manager.filter(**kwargs)
        return ''
 
# {% get_generic_data core.CategoryDefault 'type=job' as category_list %}

def get_generic_data(parser, token):
    bits = token.contents.split()
    if not len(bits) >= 5:
        raise TemplateSyntaxError, "get_generic tag takes exactly four arguments"
    if bits[4] != 'as' and bits[3] != 'as':
        raise TemplateSyntaxError, "third or fourth argument to get_latest tag must be 'as'"

    return GenericContentNode(*bits)
    
# for eg - {% get_related_data institute.Institute '' generic_detail as data_list %}
    
class GenericRelatedNode(Node):
    def __init__(self,model,arg,obj, varname):
        self.varname = varname
        self.arg=arg
        self.obj = template.Variable(obj)
        self.model = get_model(*model.split('.'))
        """
        Hacked for Video where category is Foreign key instaed of manytomany
        """
        if model.split('.')[1] == 'Video' or model.split('.')[1] == 'Job':
            self.isVideo = True
        else:
            self.isVideo = False
        
    def render(self, context):
        if not self.isVideo:
            try:
                kwargs={self.arg:self.obj.resolve(context).category.all()[0].slug}
            except:
                kwargs={}
        else:
            try:
                kwargs={self.arg:self.obj.resolve(context).category.slug}
            except:
                kwargs={}
        context[self.varname] = self.model._default_manager.filter(**kwargs).order_by('?')
        return ''
 
def get_related_data(parser, token):
    bits = token.contents.split()
    if len(bits) != 6:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[4] != 'as':
        raise TemplateSyntaxError, "second argument to get_latest tag must be 'as'"

    return GenericRelatedNode(bits[1],bits[2], bits[3],bits[5])
    
class GenericInstituteCourses(Node):
    def __init__(self,courses, varname):
        self.varname = varname
        self.courses = template.Variable(courses)
        
    def render(self, context):
        print self.courses.resolve(context).split(',')
        context[self.varname] = self.courses.resolve(context).split(',')
        return ''
 
def get_institute_courses(parser, token):
    bits = token.contents.split()

    if len(bits) != 4:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to get_latest tag must be 'as'"

    return GenericInstituteCourses(bits[1],bits[3])

class GenericRecentNode(Node):
    def __init__(self, model, varname):
        self.varname = varname
        self.model = get_model(*model.split('.'))
        self.model_name=model.split('.')[1]
    def render(self, context):
        kwargs={}
        content_type=ContentType.objects.get(name=self.model_name)
        context[self.varname] = map(lambda x:x,self.model._default_manager.filter(**kwargs))[:3]
        try:
            id_list=[x.id for x in context[self.varname]]
            result=map(lambda x:x['object_id'],Vote.objects.values('object_id','content_type').annotate(Count('object_id'),Count('content_type')).filter(content_type=content_type).exclude(object_id__in=id_list).order_by('-object_id__count'))
            if len(result) >0:
                context[self.varname].extend(map(lambda x:self.model._default_manager.get(id=x),result))
        except:
            pass
        return ''
 
def get_recent_data(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to get_latest tag must be 'as'"

    return GenericRecentNode(bits[1],bits[3])

@register.filter("get_random_list") 
def get_random_list(list):
    temp_list=[]
    length=len(list)
    for item in list:
        temp_list.insert(int(random.random()*length)+1,item)
    return temp_list

class GenericSearchNode(Node):
    def __init__(self, model_name,category, varname):
        self.varname = varname
        self.category = category
        self.model_name=model_name
    def render(self, context):
        content_type=ContentType.objects.get(name=self.model_name)
        if self.category != 'NA' :
            result=SavedRelatedSearch.objects.filter(category=self.category,model_name=self.model_name)[:5]
        else:
            result=SavedRelatedSearch.objects.filter(model_name=self.model_name)[:5]
        #print result[0].keyword
        context[self.varname]=result

        return ''


def get_related_searches(parser, token):
    bits = token.contents.split()

    if len(bits) != 6:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[4] != 'as':
        raise TemplateSyntaxError, "second argument to get_latest tag must be 'as'"

    return GenericSearchNode(bits[2],bits[3],bits[5])
    
register.tag(get_generic_data)
register.tag(get_related_data)
register.tag(get_recent_data)
register.tag(get_institute_courses)
register.tag(get_related_searches)