# -*- coding: utf-8 -*-
from django.conf.urls import url

#import chemical.views
from chem_ajax import views

urlpatterns = [
#Вещества
    url(r'^substance/search/(?P<searched>[\w\-]+)/$', views.substance_search, name='substance_search'),
    url(r'^substance/search_hint/(?P<searched>[\w\-]+)/$', views.substance_search_hint, name='substance_search_hint'),
    ]