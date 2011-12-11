#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from django.contrib.auth.models import User

@login_required
def friends_page(request, username):
    user = get_object_or_404(User, username=username)
    friends = [friendship.to_friend for friendship in user.friend_set.all()]

    var = RequestContext(request, {
        'username': username,
        'friends': friends
        })

    return render_to_response('friendships/friends_page.html', var)

@login_required
def friend_all(request):
    if request.GET.has_key('username'):
        friend = get_object_or_404(User, username=request.GET['username'])
        friendship = Friendship(from_friend=request.user,
                                to_friend=friend)
        friendship.save()
        return HttpResponseRedirect('/%s/friends/' & request.user.username)
    else:
        raise Http404

