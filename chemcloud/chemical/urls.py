# -*- coding: utf-8 -*-
from django.conf.urls import url

#import chemical.views
from chemical import views

urlpatterns = [
#Вещества
    url(r'^substance/all/$', views.substance_all, name='substance_all'),
    url(r'^substance/(?P<id_substance>[0-9]+)/detail/$', views.substance_detail, name='substance_detail'),
    url(r'^substance/new/$', views.substance_new, name='substance_new'),

#Атомы
    url(r'^atom/all/$', views.atoms_all, name='atom_all'),
    url(r'^atom/(?P<atom_number>[0-9]+)/detail/$', views.atom_detail, name='atom_detail'),
#Справочники
    url(r'^dictionaries/$', views.dictionaries, name='dictionaries'),


#Реакции
    url(r'^reaction/all/$', views.reaction_all, name='reaction_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/detail/$', views.reaction_detail, name='reaction_detail'),
    url(r'^reaction/new/$', views.reaction_new, name='reaction_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/delete/$', views.reaction_delete, name='reaction_delete'),

#Механизмы реакции
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/all/$', views.scheme_all, name='scheme_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/detail/$', views.scheme_detail, name='scheme_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/new/$', views.scheme_new, name='scheme_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/edit/$', views.scheme_edit, name='scheme_edit'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/step/(?P<id_step>[0-9]+)/detail/$', views.step_detail, name='step_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/change_order/$', views.change_step_order, name='change_step_order'),

#Вещества реакции
    url(r'^reaction/(?P<id_reaction>[0-9]+)/substance/all/$', views.react_substance_all, name='react_substance_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/substance/new/$', views.react_substance_new, name='react_substance_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/substance/(?P<id_react_substance>[0-9]+)/detail/$', views.react_substance_detail, name='react_substance_detail'),

#Эксперименты
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/all/$', views.experiment_all, name='experiment_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/detail/$', views.experiment_detail, name='experiment_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/new/$', views.experiment_new, name='experiment_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/edit/$', views.experiment_edit, name='experiment_edit'),

#Задачи
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/all/$', views.problem_all, name='problem_all'),

#Решения
   url(r'^calculation/all/$', views.calculation_all, name='calculation_all'),
   url(r'^reaction/(?P<id_reaction>[0-9]+)/calc/all/$', views.calc_all, name='calc_all'),

#Статистика
   url(r'^reaction/(?P<id_reaction>[0-9]+)/statistic/$', views.statistic, name='statistic'),

#Журнал изменений
   url(r'^reaction/(?P<id_reaction>[0-9]+)/log/$', views.log, name='log'),
]
