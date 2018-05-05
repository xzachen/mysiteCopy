#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : SundayCoder-俊勇
# @File    : urls.py
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login, name='login'),
    path('loginbyapp', views.loginbyapp, name='loginbyapp'),
    path('home', views.index, name='home'),
    path('addnote', views.addnote, name='addnote'),
    path('notedetailed/<int:nid>', views.notedetailed, name='notedetailed'),
    path('mynote', views.mynote, name='mynote'),
    path('seachnote', views.seachnote, name='seachnote'),
    path('sharenote', views.sharenote, name='sharenote'),
    path('collection', views.collection, name='collection'),
    # 一下是APPUser的路由。
    path('register', views.register, name='register'),
    # 查询课程信息路由。方法GET
    path('querycourseinfo/<int:uid>', views.querycourseinfo, name='querycourseinfo'),
    # 更新课程的路由。方法POST
    path('updatecourseinfo', views.updatecourseInfo, name='updatecourseinfo'),
    # 创建课程的路由,方法POST
    path('createcourse', views.createCourse, name='createcourse'),
    # 删除课程信息，方法GET
    path('deletecourse/<int:cid>', views.deleteCourse, name='deletecourse'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
