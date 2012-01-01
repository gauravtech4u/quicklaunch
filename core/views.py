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
import urllib2,json

class WrapperView( object ):
    
    """
    This is a wrapper view that can be inherited by any class for creating
    class based generic views .
    
    __new__() is a static function that is used create a new instance if class
    
    handle_request() check if request is of type GET or POST and call appropriate handle
    """
    
    def __new__( cls, request, *args, **kwargs ):
        self = object.__new__( cls )
        self.args = args
        self.kwargs = kwargs
        self.request = request
        self.app = self.kwargs.get( 'app', None )
        self.model_name = self.kwargs.get( 'model_name', None )
        return self.handle_request()

    def __init__( self ):
        pass

class WrapperListingView( WrapperView ):
    """
    This class can be used by any class to show basic listing on templates
    This class can be overriden by any class to change the behavior(applying various filters)
    """
    
    def handle_request( self ):
        self.template = self.app + "/listing.html"
        self.model = get_model( self.app, self.model_name )        
        self.get_data()
        self.category = 'all'
        self.extra_data()
        self.search_data()
        args_dict = pagination( self.request, self.generic_list )
        args_dict.update( self.__dict__ )
        return render_to_response( self.template, args_dict, context_instance = RequestContext( self.request ) )
    
    def get_data( self ):
        order,self.order_type=self.request.GET.get('o','id'),'desc'
        if self.request.GET.get('ot') and self.request.GET.get('ot') == 'desc':
            order='-'+order
            self.order_type='asc'
        self.generic_list = self.model.objects.all().order_by(order)
        
    def search_data(self):
        q=self.request.GET.get('q')
        if q:
            kwargs={str(self.request.GET.get('search_on'))+'__contains':self.request.GET.get('q')}
            self.generic_list=self.generic_list.filter(**kwargs)
            
        
    def extra_data( self ):
        pass

class WrapperDetailView( WrapperView ):
    """
    This class can be used by any class to show basic detail of an object on templates
    This class can be overriden by any class to change the behavior
    """
    
    def handle_request( self ):
        self.model = get_model( self.app, self.model_name )
        self.template = self.app + "/detail.html"
        self.get_data()
        self.extra_data()
        args_dict = {}
        args_dict.update( self.__dict__ )
        return render_to_response( self.template, self.__dict__, context_instance = RequestContext( self.request ) )
        
    def get_data( self ):
        self.slug = self.kwargs.get( 'slug' )
        self.generic_detail = self.model._default_manager.get( slug = self.slug )
        
    def extra_data( self ):
        pass
    

class SearchWrapperView( CoreWrapperView ):
    """
    This class can be used by any class to show basic listing on templates
    This class can be overriden by any class to change the behavior(applying various filters)
    """
    
    def add_facets( self, args_dict,location='' ):
        if args_dict.get( 'sw' ):
            args_dict['sw'] = stringprocessing( args_dict.get( 'sw' ), 'simple' )
        for key, value in self.solrmapfields.items():
            if args_dict.has_key( key ):
                if args_dict.get( key ):
                    if type( value ) == list:
                        string = ''
                        for i in range( 0, len( value ), 1 ):
                            string = string + value[i] + ':(' + ' '.join( args_dict.getlist( key ) ) + ')'
                            if i < len( value ) - 1:
                                string = string + ' '
                        self.facets.append( string )
                    else:
                        self.facets.append( value + ':(' + ' '.join( args_dict.getlist( key ) ) + ')' )
        self.params['fq'] = self.facets
        
    def add_alphabet(self):
    
        self.alphabet_list=[]
        for data in self.sqs:
            if not self.alphabet_list.__contains__( data.slug[0] ):
                self.alphabet_list.append( data.slug[0] )
        self.alphabet_list.sort()
                
    def query( self ):

        self.sqs = SearchQuerySet().raw_search( self.q, **self.params )

    def add_params(self):
        self.facets = []
        self.params = {'display_flag':1, }
        self.q,self.location='*:*',''
        if self.request.GET.get('q'):
            self.q=self.request.GET.get('q','*:*')
        if self.request.GET.get('location'):
            self.location=self.request.GET.get('location','')
        if self.kwargs.get('q'):
            self.q,self.location=self.kwargs.get('q','*:*'),self.kwargs.get('location','')
            if self.location == 'all':
                self.location=''
            if self.q == 'all':
                self.q='*:*'
        weights = []
        searchweights = SearchWeight.objects.all()
        for record in searchweights:
            weights.append( record.field + "^" + str( record.weight ) )
        weights = " ".join( weights )
        #self.params = {'facet':'on', 'qf':'text ' + weights,'facet.field':['{!ex=facet_field_name}facet_field_name_in_schema'], 'facet.mincount':1}
        #self.solrmapfields = {'course_subcategory':'{!tag=course_subcategory}course_subcategory_exact','isaff':'affiliation'}
        
    def stringprocessing( arg ):
        arg = arg.lower()
        arg = arg.replace( ',', ' , ' )
        arg = arg.replace( '"', ' " ' )
        arg = arg.strip( ' ,' )
        arg = re.sub( r'(\s)+', ' ', arg )
        return ''.join( arg )
    
    def add_sorting( self ):
        sort=self.request.GET.get('sort')
        if sort:
            self.params['sort'] = sort+' asc'
            self.sort_order = sort
            

@login_required
def submit_comment(request,app,model_name,slug):
        
    post_comment(request)
    
    return GenericDetail(request,app=app,model_name=model_name,instance_slug=slug)
    
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

def get_tweets(q='technology'):
        url='http://search.twitter.com/search.json?q='+q+'&rpp=5&include_entities=true&with_twitter_user_id=true&result_type=mixed'
        opener = urllib2.build_opener()
        result = opener.open(url).read()
        jsonResult = json.loads(result)
        return jsonResult