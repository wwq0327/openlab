#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from openlab.apps.blog.models import Category

class EntryForm(forms.Form):
    title = forms.CharField(label="标题", widget=forms.TextInput(attrs={'size': 68}))

    content = forms.CharField(label="内容", widget=forms.Textarea(attrs={'cols':80, 'rows':12}))

    tags = forms.CharField(label="标签", required=False, widget=forms.TextInput(attrs={'size': 68}))

    ##category = forms.ModelChoiceField(queryset=None, label="分类", empty_label="------------")

    category = forms.ChoiceField(label="分类")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [('', '-----------')] + \
                                          [(o.id, o.name) for o in self.user.categories.all()]

class CategoryForm(forms.Form):
    name = forms.CharField(label="分类名称", widget=forms.TextInput(attrs={'size': 20}))
