#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from openlab.blog.models import Entry, Tag, Category

## forms
from openlab.blog.forms import EntryForm, CategoryForm

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
def entry_page(request, username, id):
    entry = Entry.objects.get(id=id)
    ## 中文Tag解析
    tags = [tag.tag for tag in entry.tags.all()]

    var = RequestContext(request, {'entry': entry, 'tag_show': True, 'tags':tags})

    return render_to_response('blog/entry.html', var)

def _entry_save(request, user, form):

    ## BUG: 当修改标题后，日志会重复发布一次。

    c_id = form.cleaned_data['category']

    category = Category.objects.get(id=c_id)

    entry, create = Entry.objects.get_or_create(
        title = form.cleaned_data['title'],
        content = form.cleaned_data['content'],
        user = user,
        category=category)

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

            return HttpResponseRedirect('/%s/blog/' % user)
        else:
            print form.errors
    else:
        form = EntryForm()
        #form.fields['category'].queryset = user.categories.all()
        form.fields['category'].choices = [(o.id, o) for o in user.categories.all()]

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

@login_required
def category_list(request, username):

    user = User.objects.get(username=username)

##    categories  = Category.objects.filter(user=user)
    categories = user.categories.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cate = Category.objects.create(
                name = form.cleaned_data['name'],
                user = user)
            cate.save()

            return HttpResponseRedirect("/%s/blog/category/" % request.user.username)
    else:
        form = CategoryForm()

    var = RequestContext(request, {'categories': categories,
                                   'form': form,
                                   'is_auth': username == request.user.username ## 判断当前分类所在用户是否为登录用户
                                   })

    return render_to_response('blog/category_list_add.html', var)

@login_required
def category_del(request, username, id):

    if username == request.user.username:

        try:
            cate = Category.objects.get(id=id)
            cate.delete()

        except ObjectDoesNotExist:
            pass
    else:
        raise Http404()

    return HttpResponseRedirect("/%s/blog/category/" % request.user.username)







