#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : SundayCoder-俊勇
# @File    : froms.py
from django import forms
from django.contrib import auth
from myapp.models import Note
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# 设置登录的表格
class LoginForm(forms.Form):
    username=forms.CharField(label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名和密码出错')
        else:
            self.cleaned_data['user']=user
        return self.cleaned_data

class RegForm(forms.Form):
    pass

class NoteFrom(forms.Form):
    title = forms.CharField(label="笔记标题",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))

    category = forms.CharField(label="笔记类别",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))

    content = forms.CharField(label='笔记内容',
                              widget=CKEditorUploadingWidget(attrs={'class': 'container'}))
    meta_description = forms.CharField(label="笔记简述",
                                       widget=forms.Textarea(
                                           attrs={'class': 'form-control'}))
    is_published=forms.BooleanField(label='是否分享笔记',required=False )
    class Meta:
        model = Note
        fields = ['title', 'category', 'meta_description', 'content', 'is_published']


