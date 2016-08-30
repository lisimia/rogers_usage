from django.conf.urls import patterns, include, url

import rogers.views

urlpatterns = patterns('',
    url(r'^usage', rogers.views.usage, name='usage'),

)
