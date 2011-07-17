from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from choice import LIST_CATEGORY_TYPE
import datetime

# Create your models here.


class Post(models.Model):
    name                     =  models.CharField(max_length = 300)
    slug                     =  models.SlugField(max_length = 255, unique = True)
    description              =  models.TextField()
    category               =  models.ManyToManyField('CategoryDefault',null=True,blank=True)
    published                =  models.BooleanField(default = False)
    location                =  models.ForeignKey('Location',null=True,blank=True)
    author                   =  models.ForeignKey(User)
    created_date =  models.DateTimeField(auto_now = True)
    modified_date  =  models.DateTimeField(auto_now = True, auto_now_add = True)
    
    #tags = TaggableManager()
    
    class Meta:
        ordering  =  ('name',)
        abstract=True
    
    def __unicode__(self):
        return self.name
    
    objects=models.Manager()
        
class CategoryDefault(models.Model):
    name                     =  models.CharField(max_length = 300)
    slug                     =  models.SlugField(max_length = 255, unique = True,null=True,blank=True)
    parent                   =  models.ForeignKey('self',blank=True,null = True)
    description              =  models.TextField(null=True,blank=True)
    created_date             =  models.DateTimeField(auto_now = True)
    modified_date            =  models.DateTimeField(auto_now = True, auto_now_add = True)
    type                     =  models.CharField(max_length = 200,choices = LIST_CATEGORY_TYPE)
    
    def __unicode__(self):
        return self.name
    class Meta:
        ordering  =  ('name',)
        
    def get_absolute_url(self):
        app = None
        model = None
        if self.type == 'video':
            app = 'video'
            model = 'Video'
        else:
            if self.type == 'job':
                app = 'job'
                model = 'Job'
            else:
                if self.type == 'calender':
                    app = 'calender'
                    model = 'Event'
                else:
                    if self.type == 'institute':
                        app = 'institute'
                        model = 'Institute'
                    else:
                        if self.type == 'article':
                            app = 'article'
                            model = 'Article'
                        else:
                            app = self.type
                            model = ''
        
        return ('generic_list', (app,model,self.slug,))
    get_absolute_url = models.permalink(get_absolute_url)
        

        
class Location(models.Model):
    name                     = models.CharField(max_length = 100)
    slug                     =  models.SlugField(max_length = 255, unique = True,null=True,blank=True)
    lat                      = models.CharField(max_length = 20,null=True,blank=True)
    long                     = models.CharField(max_length = 20,null=True,blank=True)
    parent                   = models.ForeignKey('self',null = True,blank=True)
    type                     = models.CharField(max_length = 100,null=True,blank=True)
    def __unicode__(self):
        return self.name
    
class ContactUs(models.Model):
    name                     = models.CharField(max_length = 100)
    message                     =models.TextField()
    email                      = models.EmailField(max_length = 200,null=True,blank=True)
    mobile                     = models.IntegerField()

    def __unicode__(self):
        return self.name
    
class Quote(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=200)
    description=models.TextField()
    
    def __unicode__(self):
        return self.title
    
class RandomLinks(models.Model):
    slug                     =  models.SlugField(max_length = 255, unique = True,null=True,blank=True)
    description              = models.CharField(max_length = 200,null=True,blank=True)
    object_id                     = models.CharField(max_length = 200,null=True,blank=True)
    def __unicode__(self):
        return self.slug
    

    
    
    
    
    
    
    
    
    
    
    
    