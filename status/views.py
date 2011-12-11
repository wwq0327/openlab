#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from openlab.status.models import Status

@login_required
def st_del_page(request, username, id):
    st_page = get_object_or_404(Status, id=id)

    try:
        st_page.delete()
    except:
        raise Http404()

    return HttpResponseRedirect('/%s/home' % username)
