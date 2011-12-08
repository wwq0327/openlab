#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

def all_home(request):
    """全站首页"""

    var = RequestContext(request, {'user': request.user})

    return render_to_response('index.html', var)

@login_required
def home(request, username):
    """登录后所在的个人首页"""
    var = RequestContext(request, {'user': request.user})
    return render_to_response('accounts/home.html', var)

@login_required
def logout_view(request):
    """退出登录"""

    logout(request)
    return HttpResponseRedirect(reverse('index'))
