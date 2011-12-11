#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from openlab.status.models import Status

from openlab.status.forms import StatusForm

_ST_PRE_PAGE = 10

def all_home(request):
    """全站首页"""

    var = RequestContext(request, {'user': request.user})

    return render_to_response('index.html', var)

@login_required
def home(request, username):
    """登录后所在的个人首页"""
    #username = request.user.username
    #user = User.objects.get(username=username)
    user = get_object_or_404(User, username=username)

    # 反向取得相应用户的数据
    q_set = user.status_set.all()
    paginator = Paginator(q_set, _ST_PRE_PAGE)

    try:
        page = int(request.GET['page'])
    except:
        page = 1

    try:
        st_list = paginator.page(page)
    except:
        raise Http404

    #form = StatusForm()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            st = Status.objects.create(
                content = form.cleaned_data['content'],
                user = user)
            st.save()
        return HttpResponseRedirect('/%s/home/' % user)
    else:
        form = StatusForm()

    var = RequestContext(request, {'user': request.user,
                                   'form': form,
                                   'st_list': st_list.object_list,
                                   'show_p': paginator.num_pages > 1,
                                   'has_prev': st_list.has_previous(),
                                   'has_next': st_list.has_next(),
                                   'page': page,
                                   'pages': paginator.num_pages,
                                   'next_page': page + 1,
                                   'prev_page': page - 1,
                                   })
    return render_to_response('accounts/home.html', var)

@login_required
def logout_view(request):
    """退出登录"""

    logout(request)
    return HttpResponseRedirect(reverse('index'))
