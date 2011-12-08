#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class StatusForm(forms.Form):
    content = forms.CharField(label=u'情感状态', widget=forms.TextInput(attrs={'size':80}))

