import os
import sys


os.environ['DJANGO_SETTINGS_MODULE'] = 'campus.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

sys.path.insert(0, '/home/projects')
sys.path.insert(0,'/home/projects/campus')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
