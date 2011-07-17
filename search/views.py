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


def search(request,app=None ,model_name=None,q=None):

    if request.GET.get('q'):
        q=request.GET.get('q')
        search_save=True
    else:
        search_save=False
    model = get_model(app,model_name)
    search_result=list(model.search.query(q.__str__()))
    paginator = Paginator(search_result, 10)          # Called the django default Paginator
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
    """
    Some hack for video_tutorial
    """
    temp = re.split('_',app)[0].lower()
    templatename = temp + '/' + temp + '_search.html'
    if len(search_result) > 0 and search_save and not q == '':
        try:
            SavedAllSearch(keyword=q,app=app,model_name=model_name).save()
        except:pass
    current=app
    return render_to_response(templatename, locals(), context_instance = RequestContext(request))


def sitesearch(request):
    search = SphinxQuerySet(index='article_indexes institute_indexes job_indexes video_indexes job_indexes',
                          mode='SPH_MATCH_ANY',
                          sort='SPH_SORT_RELEVANCE')
    if request.method =='GET':
        q=request.GET.get('q')
        search_result=list(search.query(q.__str__()))
        #search_result=list(Video.search.query(q.__str__()))
        category_list=CategoryDefault.objects.all()
        paginator = Paginator(search_result, 10)          # Called the django default Paginator
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
    #temp = re.split('_',app)[0].lower()
    templatename = 'search/search_list.html'
    if len(search_result) > 0:
        SavedAllSearch(keyword=q,app=app,model_name=model_name).save()
    #return render_to_response('search/search_list.html', locals(), context_instance = RequestContext(request))
    return render_to_response(templatename, locals(), context_instance = RequestContext(request))

def allsearches(request):
    search_list=SavedAllSearch.objects.all().order_by('-created_date')
    paginator = Paginator(search_list, 100)          # Called the django default Paginator
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
    return render_to_response('savedallsearch/savedallsearch_list.html', locals(), context_instance = RequestContext(request))