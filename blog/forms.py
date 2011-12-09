#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
#from blog.models import Entry

class EntryForm(forms.Form):
    title = forms.CharField(label="标题", widget=forms.TextInput(attrs={'size': 100}))

    content = forms.CharField(label="内容", widget=forms.Textarea(attrs={'cols':80, 'rows':12}))

    ## class Meta:
    ##     model = Entry
    ##     fileds = ('title', 'content')
