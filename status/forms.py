#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class StatusForm(forms.Form):
    content = forms.CharField(label="情感状态",
                              widget=forms.Textarea(attrs={
                                  'rols': 60,
                                  'rows': 3})
                              )

