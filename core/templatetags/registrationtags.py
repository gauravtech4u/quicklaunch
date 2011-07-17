from django.template import Library, Node
from django.db.models import get_model
import re
from django.core.cache import cache
from django import template
register = Library()
from django.views.decorators.cache import cache_page
from django.template import TemplateSyntaxError
from registration.models import UserProfile
from django.db.models import Count
from django.contrib.auth.models import ContentType
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm
import random

class GenericUserNode(Node):
    def __init__(self,type,category, varname):
        self.varname = varname
        self.type=template.Variable(type)
        self.category = template.Variable(category)

        
    def render(self, context):
        #if not self.isVideo:
        #    kwargs={self.arg:self.obj.resolve(context).category.all()[0].slug}
        #else:
        #    kwargs={self.arg:self.obj.resolve(context).category.slug}
        kwargs={'type':self.type.resolve(context),'category':self.category.resolve(context)}
        context[self.varname] = UserProfile.objects.filter(**kwargs)
        return ''
 
def get_user_data(parser, token):
    bits = token.contents.split()

    return GenericUserNode(bits[1],bits[2],bits[4])

@register.inclusion_tag('widgets/login_register.html')
def build_login_form(generic_detail,request,app='institute',model_name='Institute'):
    login_form  = AuthenticationForm()
    register_form = RegistrationForm()
    
    return {'login_form':login_form,'generic_detail':generic_detail,'register_form':register_form,'path':request.path,'app':app,'model_name':model_name,}
        
@register.inclusion_tag('widgets/login_register.html')
def build_header_login_form(request,app='institute',model_name='Institute'):
    login_form  = AuthenticationForm()
    register_form = RegistrationForm()
    
    return {'login_form':login_form,'generic_detail':None,'register_form':register_form,'path':request.path,'app':app,'model_name':model_name,}
        

register.tag(get_user_data)
