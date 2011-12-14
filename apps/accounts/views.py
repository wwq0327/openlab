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
from openlab.apps.status.models import Status

from openlab.apps.status.forms import StatusForm
from openlab.apps.accounts.forms import RegistrationForm
from openlab.apps.friendships.models import Friendship

_ST_PRE_PAGE = 10

def all_home(request):
    """全站首页"""

    var = RequestContext(request, {'user': request.user})

    return render_to_response('index.html', var)

@login_required
def home(request, username):
    """登录后所在的个人首页"""
    #username = request.user.username
    user = User.objects.get(username=username)
    #user = get_object_or_404(User, username=username)

    # 反向取得相应用户的数据
    q_set = user.status_set.all()
    paginator = Paginator(q_set, _ST_PRE_PAGE)

    ## 好友关系
    is_friend = Friendship.objects.filter(from_friend=request.user,
                                          to_friend=user)


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
                                   'is_friend': is_friend,
                                   'username': username
                                   })
    return render_to_response('accounts/home.html', var)

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                email = form.cleaned_data['email']
                )
            ## 来自于邀请的注册
            ## if 'invitation' in request.session:
            ##     invitation = Invitation.objects.get(id=request.session['invistation'])
            ##     #建立好友关系
            ##     friendship = Friendship(from_friend=user, to_friend=invitation.sender)
            ##     friendship.save()

            ##     ## 双向
            ##     friendship = Friendship(from_friend=invitation.sender, to_friend=user)
            ##     friendship.save()

            ##     invitation.delete()
            ##     del request.session['invitation']

            return HttpResponseRedirect('/accounts/register/success/')

    else:
        form = RegistrationForm()

    return render_to_response('accounts/register.html',
                              {'form': form}
                              )

@login_required
def logout_view(request):
    """退出登录"""

    logout(request)
    return HttpResponseRedirect(reverse('index'))
