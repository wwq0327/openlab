#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from openlab.blog.models import Entry, Tag

## forms
from openlab.blog.forms import EntryForm

## 每页显示日志条数
_BLOG_PRE_PAGE = 5

def _get_username(r):
    return User.objects.get(username=r.user.username)

@login_required
def entry_list(request, username):
    #user = User.objects.get(username=request.user.username)
    user = _get_username(request)

    q_set = user.entry_set.all()

    paginator = Paginator(q_set, _BLOG_PRE_PAGE)

    try:
        page = int(request.GET['page'])
    except:
        page = 1

    try:
        lists = paginator.page(page)
    except:
        Http404


    var = RequestContext(request, {'lists': lists.object_list,
                                   'tag_show': False,
                                   'show_p': paginator.num_pages > 1,
                                   'has_prev': lists.has_previous(),
                                   'has_next': lists.has_next(),
                                   'page': page,
                                   'pages': paginator.num_pages,
                                   'next_page': page + 1,
                                   'prev_page': page - 1,
                                   })

    return render_to_response('blog/home.html', var)


@login_required
def entry_page(request, usernaem, id):
    entry = Entry.objects.get(id=id)
    ## 中文Tag解析
    tags = [tag.tag for tag in entry.tags.all()]

    var = RequestContext(request, {'entry': entry, 'tag_show': True, 'tags':tags})

    return render_to_response('blog/entry.html', var)

def _entry_save(request, user, form):

    entry, create = Entry.objects.get_or_create(
        title = form.cleaned_data['title'],
        content = form.cleaned_data['content'],
        user = user)

    if not create:
        entry.tags.clear()

    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(tag=tag_name, user=user)
        entry.tags.add(tag)

    entry.save()

    return entry

@login_required
def entry_new(request, username):
    user = _get_username(request)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = _entry_save(request, user, form)

            ## entry = Entry.objects.create(
            ##     title = form.cleaned_data['title'],
            ##     content = form.cleaned_data['content'],
            ##     user = user)
            ## tag_names = form.cleaned_data['tags'].split()
            ## for tag_name in tag_names:
            ##     tag, dummy = Tag.objects.get_or_create(tag=tag_name, user=user)
            ##     entry.tags.add(tag)

            ## entry.save()
            #return HttpResponseRedirect(reverse('entry_lst'))
            return HttpResponseRedirect('/%s/blog/' % user)
    else:
        form = EntryForm()

    var = RequestContext(request, {'form':form})

    return render_to_response('blog/entry_new.html', var)

@login_required
def entry_tag(request, username, tag):
    """根据tag查找相应的entry"""

    t = Tag.objects.get(tag=tag)

    lists = t.entry_set.all()

    var = RequestContext(request, {'lists': lists, 'bytag_show': True, 'tag': tag})

    return render_to_response('blog/home.html', var)

@login_required
def entry_edit(request, username, id):
    if not username == request.user.username:
        raise Http404()
    entry = get_object_or_404(Entry, id=id)
    title = entry.title
    content = entry.content
    tags = ''
    try:
        tags = ' '.join(tag.tag for tag in entry.tags.all())
    except:
        pass

    user = _get_username(request)


    if request.method == 'POST':
        myform = EntryForm(request.POST)
        if myform.is_valid():
            e = _entry_save(request, user, myform)

        return HttpResponseRedirect("/%s/blog/entry/%s/" % (user, id))
    else:
        form = EntryForm({'title': title, 'content': content, 'tags':  tags})

    var = RequestContext(request, {'form':form})

    return render_to_response('blog/entry_new.html', var)

@login_required
def entry_del(request, username, id):

    if username == request.user.username:
        entry = get_object_or_404(Entry, id=id)
    else:
        raise Http404()

    try:
        entry.delete()
    except:
        raise Http404()

    return HttpResponseRedirect('/%s/blog/' % request.user.username)


