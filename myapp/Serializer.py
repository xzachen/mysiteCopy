#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : SundayCoder-俊勇
# @File    : Serializer.py
from rest_framework.serializers import ModelSerializer
from myapp.models import APPUser
class UserSerializer(ModelSerializer):
    # 设置序列化
    class Meta:
        model = APPUser
        fields = "__all__"


