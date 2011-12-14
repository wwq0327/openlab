#!/usr/bin/env python
# -*- coding: utf-8 -*-
##################################################
#           accounts urls
##################################################

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('openlab.apps.accounts.views',
                       url(r'^logout/$', 'logout_view'),
                       url(r'^register/$', 'register_page'),
                       url(r'^register/success/$', direct_to_template,
                           {'template': 'accounts/register_success.html'}),
                       )

urlpatterns += patterns('',
                        url(r'^login/$', 'django.contrib.auth.views.login',
                            {'template_name': 'accounts/login.html'},
                            name='ac_login'),

                        )

