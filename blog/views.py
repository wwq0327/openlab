#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from openlab.blog.models import Entry, Tag

## forms
from openlab.blog.forms import EntryForm

def _get_username(r):
    return User.objects.get(username=r.user.username)

@login_required
def entry_list(request):
    #user = User.objects.get(username=request.user.username)
    user = _get_username(request)

    lists = user.entry_set.all()

    var = RequestContext(request, {'lists': lists, 'tag_show': False})

    return render_to_response('blog/home.html', var)


@login_required
def entry_page(request, id):
    page = Entry.objects.get(id=id)
    #tags = page.tags.all()

    var = RequestContext(request, {'page': page, 'tag_show': True})

    return render_to_response('blog/entry.html', var)

@login_required
def entry_new(request):
    user = _get_username(request)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():

            entry = Entry.objects.create(
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                user = user)
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(tag=tag_name, user=user)
                entry.tags.add(tag)

            entry.save()
            #return HttpResponseRedirect(reverse('entry_lst'))
            return HttpResponseRedirect('/%s/blog/' % user)
    else:
        form = EntryForm()


    var = RequestContext(request, {'form':form})

    return render_to_response('blog/entry_new.html', var)

@login_required
def entry_tag(request, tag):
    """根据tag查找相应的entry"""

    t = Tag.objects.get(tag=tag)

    lists = t.entry_set.all()

    var = RequestContext(request, {'lists': lists, 'bytag_show': True, 'tag': tag})

    return render_to_response('blog/home.html', var)

@login_required
def entry_edit(request, id):
    pass

@login_required
def entry_del(request, id):
    entry = get_object_or_404(Entry, id=id)

    try:
        entry.delete()
    except:
        raise Http404()

    return HttpResponseRedirect('/%s/blog' % request.user.username)


