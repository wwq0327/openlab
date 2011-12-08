#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def all_home(request):
    """全站首页"""

    return render_to_response('index.html')

def home(request):
    """登录后所在的个人首页"""

    return render_to_response('accounts/home.html')
