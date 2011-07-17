from django.contrib.comments.views.comments import post_comment
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from core.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import get_model
from django.utils import simplejson
from core.forms import ContactForm
from django.contrib.auth.models import ContentType
from django.http import Http404
from voting.models import Vote
from django.db.models import Count

def generic_list(request,app,model_name,category=None):
    model = get_model(app,model_name)
    try:
        if category and not category.__contains__('all-'):
            generic_list=model._default_manager.filter(category__slug=category).order_by('?')
        else:
            generic_list=model._default_manager.all()
            category  = 'all'
    except:
        raise Http404
    current=app
    state = 'all'
    limit=10
    if request.GET.get('limit'):
        limit=int(request.GET.get('limit'))
    paginator = Paginator(generic_list, limit)          # Called the django default Paginator       
    try:
       page = paginator.page(request.GET.get('page', 1))
    except InvalidPage:
       raise Http404
    startPage = max(page.number - 2, 1)
    if startPage <= 2: startPage = 1
    endPage = page.number + 2 + 1
    if endPage >= paginator.num_pages - 1: endPage = paginator.num_pages + 1
    page_numbers = [n for n in range(startPage, endPage) if n > 0 and n <= paginator.num_pages]
    pagenumbers= page_numbers
    show_first = 1 not in page_numbers
    show_last =  paginator.num_pages not in page_numbers
    model_name=model.__name__.lower()
    category_list=CategoryDefault.objects.filter(parent=None,type=model_name)
    template=model_name+'/'+model_name+'_list.html'
    return render_to_response(template, locals(), context_instance = RequestContext(request))

def generic_detail(request,app,model_name,instance_slug=None):
    model = get_model(app,model_name)
    try:
        generic_detail=model._default_manager.get(slug=instance_slug)
    except:
        raise Http404
    category_list=CategoryDefault.objects.all()
    current=app
    template=model.__name__.lower()+'/'+model.__name__.lower()+'_detail.html'
    return render_to_response(template, locals(), context_instance = RequestContext(request))

def submit_comment(request,app,model_name,slug):
        
    post_comment(request)
    
    return generic_detail(request,app,model_name,slug)
    
def refine_data(request):
    model = get_model(request.GET.get('app'),request.GET.get('model_name'))
    kwargs={str(request.GET.get('arg_name')):str(request.GET.get('arg_value')),}
    refine_data=model._default_manager.filter(**kwargs)
    response = {
            'data_id_list':map(lambda x:x.id,refine_data),
            'data_name_list':map(lambda x:x.name,refine_data),
    }
    return HttpResponse( simplejson.dumps( response ),mimetype='application/javascript' )
    
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Your query is submitted and will be reviewed by administrator soon ."
        else:
            message = "Kindly check submitted data or there may be maintenance activity going on."
    else:
        form=ContactForm()
    current='contact'
    return render_to_response('contact_us.html', locals(), context_instance = RequestContext(request))
    
def data_by_voting_list(request,app=None,model_name=None):
    model = get_model(app,model_name)
    content_type=ContentType.objects.get(name=model_name)
    list=Vote.objects.values('object_id','content_type').annotate(Count('object_id'),Count('content_type')).filter(content_type=content_type).order_by('-object_id__count')
    votes_list=map(lambda x:x['object_id'],list)
    generic_list=map(lambda x:x,model._default_manager.filter(id__in=votes_list))
    generic_list.extend(model._default_manager.exclude(id__in=votes_list))
    paginator = Paginator(generic_list, 10)          # Called the django default Paginator       
    try:
       page = paginator.page(request.GET.get('page', 1))
    except InvalidPage:
       raise Http404
    startPage = max(page.number - 2, 1)
    if startPage <= 2: startPage = 1
    endPage = page.number + 2 + 1
    if endPage >= paginator.num_pages - 1: endPage = paginator.num_pages + 1
    page_numbers = [n for n in range(startPage, endPage) if n > 0 and n <= paginator.num_pages]
    pagenumbers= page_numbers
    show_first = 1 not in page_numbers
    show_last =  paginator.num_pages not in page_numbers
    template=model.__name__.lower()+'/'+model.__name__.lower()+'_list.html'
    return render_to_response(template, locals(), context_instance = RequestContext(request))
    
def sitemap_redirect(request,section=None):
    import mimetypes,os,stat
    from django.utils.http import http_date
    from django.conf import settings
    fullpath = (settings.XML_ROOT+'sitemap_'+section).replace('\\', '/')
    statobj = os.stat(fullpath)
    mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
    contents = open(fullpath, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    response["Content-Length"] = len(contents)
    return response   

    
def show_list(app,model_name,arg,arg_value):
    model = get_model(app,model_name)
    generic_list=model._default_manager.filter(**{arg:arg_value}).order_by('?')
    return generic_list

def pagination(request,generic_list):
    paginator = Paginator(generic_list, 10)          # Called the django default Paginator       
    try:
       page = paginator.page(request.GET.get('page', 1))
    except InvalidPage:
       raise Http404
    startPage = max(page.number - 2, 1)
    if startPage <= 2: startPage = 1
    endPage = page.number + 2 + 1
    if endPage >= paginator.num_pages - 1: endPage = paginator.num_pages + 1
    page_numbers = [n for n in range(startPage, endPage) if n > 0 and n <= paginator.num_pages]
    pagenumbers= page_numbers
    show_first = 1 not in page_numbers
    show_last =  paginator.num_pages not in page_numbers
    return {'paginator':paginator,'page':page,'startPage':startPage,'endPage':endPage,'page_numbers':page_numbers,
            'pagenumbers':pagenumbers,'show_first':show_first,'show_last':show_last
            }
    
def index(request):
    current='index'
    return render_to_response('index.html', locals(), context_instance = RequestContext(request))