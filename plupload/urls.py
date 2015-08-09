# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from plupload.upload import do_upload

urlpatterns = patterns(
    '',
    url(r'^upload/$', do_upload, name='plupload'),
)
