# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
#import chemical.views
from chemical import views

urlpatterns = [   
        
    url(r'^substance/all/$', views.substance_all, name='substance_all'),
    url(r'^substance/(?P<id_substance>[0-9]+)/detail/$', views.substance_detail, name='substance_detail'),
    url(r'^substance/new/$', views.substance_new, name='substance_new'),

    url(r'^atom/all/$', views.atoms_all, name='atom_all'),
    url(r'^atom/(?P<atom_number>[0-9]+)/detail/$', views.atom_detail, name='atom_detail'),

    url(r'^dictionaries/$', views.dictionaries, name='dictionaries'),
    url(r'^calculation/all/$', views.calculation_all, name='calculation_all'),

#Реакции
    url(r'^reaction/all/$', views.reaction_all, name='reaction_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/detail/$', views.reaction_detail, name='reaction_detail'),
    url(r'^reaction/new/$', views.reaction_new, name='reaction_new'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/all/$', views.scheme_all, name='scheme_all'),
    url(r'^scheme/(?P<id_scheme>[0-9]+)/detail/$', views.scheme_detail, name='scheme_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/new/$', views.scheme_new, name='scheme_new'),
    url(r'^scheme/(?P<id_scheme>[0-9]+)/edit/$', views.scheme_edit, name='scheme_edit'),

#Эксперименты
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/all/$', views.experiment_all, name='experiment_all'),
    url(r'^experiment/(?P<id_experiment>[0-9]+)/detail/$', views.experiment_detail, name='experiment_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/new/$', views.experiment_new, name='experiment_new'),
    url(r'^experiment/(?P<id_experiment>[0-9]+)/edit/$', views.experiment_edit, name='experiment_edit'),
]
