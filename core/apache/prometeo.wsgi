import os, sys
from django.core.handlers.wsgi import WSGIHandler

prometeo_path = os.path.abspath(os.getcwd() + '/../..')

sys.path.append(prometeo_path)
sys.path.append(prometeo_path + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'prometeo.settings'

application = WSGIHandler()
