from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from core.models import CategoryDefault
from django.template.defaultfilters import slugify

class SavedRelatedSearch(models.Model):
    app         =   models.CharField(max_length = 100)
    model_name  =   models.CharField(max_length = 100)
    keyword     =   models.CharField(max_length = 240,unique=True)
    category    =   models.ForeignKey(CategoryDefault,null=True,blank=True)
    created_date   =   models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_date']

    def __unicode__(self):
        return self.keyword
    
class SavedAllSearch(models.Model):
    app         =   models.CharField(max_length = 100)
    model_name  =   models.CharField(max_length = 100)
    keyword     =   models.CharField(max_length = 240,unique=True)
    category    =   models.ForeignKey(CategoryDefault,null=True,blank=True)
    created_date   =   models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-created_date']
        
    def __unicode__(self):
        return self.keyword
    
    def get_absolute_url(self):
        return ('savedsearch', (self.app,self.model_name,slugify(self.keyword),))
    get_absolute_url = models.permalink(get_absolute_url)