from django.contrib import admin
from django.contrib.auth.models import User
from search.models import *

admin.site.register(SavedAllSearch)
admin.site.register(SavedRelatedSearch)
