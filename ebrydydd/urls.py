from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import ebrydydd.views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', ebrydydd.views.hafan, name='hafan'),
    url(r'^dadansoddwr/', include('ebrydydd.dadansoddwr.urls', namespace="dadansoddwr")),
    url(r'^rheolau/', include('ebrydydd.rheolau.urls', namespace="rheolau")),

)
