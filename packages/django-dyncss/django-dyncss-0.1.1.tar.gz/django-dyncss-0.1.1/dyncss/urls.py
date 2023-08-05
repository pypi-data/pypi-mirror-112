# -*- coding: utf-8 -*-
from django.urls import path

from .views import dyncss

appname = 'dyncss'

urlpatterns = [
    path('<str:filename>', dyncss, name='dyncss'),
]
