#!/usr/bin/env python
# -*- coding: utf-8 -*-
##################################################
#           accounts urls
##################################################

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('openlab.accounts.views',
                       url(r'^logout/$', 'logout_view'),
                       )

urlpatterns += patterns('',
                        url(r'^login/$', 'django.contrib.auth.views.login',
                            {'template_name': 'accounts/login.html'},
                            name='ac_login'),

                        )

