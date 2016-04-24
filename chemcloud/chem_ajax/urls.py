# -*- coding: utf-8 -*-
from django.conf.urls import url

#import chemical.views
from chem_ajax import views

urlpatterns = [
#Вещества
    url(r'^substance/search/(?P<searched>[\w\-]+)/$', views.substance_search, name='substance_search'),
    url(r'^substance/search_hint/(?P<searched>[\w\-]+)/$', views.substance_search_hint, name='substance_search_hint'),
    url(r'^substance/(?P<id_substance>[0-9]+)/detail_edit/$', views.substance_detail_edit, name='substance_detail_edit'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/detail_edit/$', views.reaction_detail_edit, name='reaction_detail_edit'),
    ]