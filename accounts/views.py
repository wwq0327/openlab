#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from openlab.status.models import Status

from openlab.status.forms import StatusForm

def all_home(request):
    """全站首页"""

    var = RequestContext(request, {'user': request.user})

    return render_to_response('index.html', var)

@login_required
def home(request):
    """登录后所在的个人首页"""

    user = User.objects.get(username=request.user.username)

    # 反向取得相应用户的数据
    st_list = user.status_set.all()

    #form = StatusForm()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            st = Status.objects.create(
                content = form.cleaned_data['content'],
                user = user)
            st.save()
        return HttpResponseRedirect('/home/')
    else:
        form = StatusForm()

    var = RequestContext(request, {'user': request.user,
                                   'form': form,
                                   'st_list': st_list
                                   })
    return render_to_response('accounts/home.html', var)

@login_required
def logout_view(request):
    """退出登录"""

    logout(request)
    return HttpResponseRedirect(reverse('index'))
