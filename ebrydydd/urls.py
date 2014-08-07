# -*- coding: utf-8 -*-
'''
ebrydydd: urls.py
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.views.generic import RedirectView
import ebrydydd.views

urlpatterns = patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/ebrydydd_logo.png')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', ebrydydd.views.hafan, name='hafan'),
    url(r'dadansoddiad/$', ebrydydd.views.dadansoddiad, name='dadansoddiad'),
    url(r'dyfarniad/$', ebrydydd.views.dyfarniad, name='dyfarniad'),
    url(r'cronfa/$', ebrydydd.views.cronfa, name='cronfa'),
    url(r'cwis/$', ebrydydd.views.cwis, name='cwis'),

    url(r'llinellau/$', ebrydydd.views.Llinell_ListView.as_view(), name='rhestr-llinellau'),
	url(r'^llinellau/creu/$', ebrydydd.views.Llinell_CreateView.as_view(), name='create-llinell',),
	url(r'^llinellau/golygu/(?P<pk>\d+)/$', ebrydydd.views.Llinell_UpdateView.as_view(), name='update-llinell',),
    url(r'^llinellau/dileu/(?P<pk>\d+)/$', ebrydydd.views.Llinell_DeleteView.as_view(), name='delete-llinell',),
    url(r'^llinellau/(?P<pk>\d+)/$', ebrydydd.views.Llinell_DetailView.as_view(), name='llinell',),

    url(r'aelodau/$', ebrydydd.views.Aelod_ListView.as_view(), name='rhestr-aelodau'),
	url(r'aelodau/(?P<pk>\d+)/$', ebrydydd.views.Aelod_DetailView.as_view(), name='aelod'),
    url(r'^cofrestru/$', ebrydydd.views.cofrestru, name='cofrestru',),

)
