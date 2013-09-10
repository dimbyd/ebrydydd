'''
urls.py (app dadansoddwr) 
'''
from django.conf.urls import patterns, url

from ebrydydd.dadansoddwr import views

urlpatterns = patterns('',
    url(r'^$', views.hafan, name='hafan'),
)

