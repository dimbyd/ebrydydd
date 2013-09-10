'''
urls.py ar gyfer app rheolau 
'''
from django.conf.urls import patterns, url

from ebrydydd.rheolau import views

urlpatterns = patterns('',
    url(r'^$', views.hafan, name='hafan'),
    #url(r'^(?P<dosbarth>\w+)/$', views.detail, name='detail'),
)

