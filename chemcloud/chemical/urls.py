# -*- coding: utf-8 -*-
from django.conf.urls import url

#import chemical.views
from chemical import views

urlpatterns = [
#Вещества
    url(r'^substance/all/$', views.substance_all, name='substance_all'),
    url(r'^substance/isomers/$', views.substance_isomers, name='substance_isomers'),
    url(r'^substance/isomers/(?P<consist_string>[\w\-\.]+)/$', views.substance_isomers, name='substance_isomers'),
    url(r'^substance/search/$', views.substance_all_search, name='substance_all_search'),
    url(r'^substance/search/(?P<searched>[\w\-\.\,\!\?\\\:\;\s]+)/$', views.substance_all_search, name='substance_all_search'),
    url(r'^substance/(?P<id_substance>[0-9]+)/detail/$', views.substance_detail, name='substance_detail'),
    url(r'^substance/new/$', views.substance_new, name='substance_new'),

#Атомы
    url(r'^atom/all/$', views.atoms_all, name='atom_all'),
    url(r'^atom/(?P<atom_number>[0-9]+)/detail/$', views.atom_detail, name='atom_detail'),
#Справочники
    url(r'^dictionaries/$', views.dictionaries, name='dictionaries'),


#Реакции
    url(r'^reaction/all/$', views.reaction_all, name='reaction_all'),
    url(r'^reaction/all/(?P<searched>[\w\-\.\,\!\?\\\:\;\s]+)/$', views.reaction_all, name='reaction_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/detail/$', views.reaction_detail, name='reaction_detail'),
    url(r'^reaction/new/$', views.reaction_new, name='reaction_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/delete/$', views.reaction_delete, name='reaction_delete'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/copy/$', views.reaction_copy, name='reaction_copy'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/report/$', views.reaction_report, name='reaction_report'),

#Механизмы реакции
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/all/$', views.scheme_all, name='scheme_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/detail/$', views.scheme_detail, name='scheme_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/new/$', views.scheme_new, name='scheme_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/edit/$', views.scheme_edit, name='scheme_edit'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/delete/$', views.scheme_delete, name='scheme_delete'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/copy/$', views.scheme_copy, name='scheme_copy'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/report/$', views.scheme_report, name='scheme_report'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/step/(?P<id_step>[0-9]+)/detail/$', views.step_detail, name='step_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/change_order/$', views.change_step_order, name='change_step_order'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/check_balance/$', views.scheme_check_balance, name='scheme_check_balance'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/step_delete/$', views.step_delete, name='step_delete'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/step/new/$', views.step_new, name='step_new'),


#Урл для обновления данных при редактировании ячейки какой-либо таблицы. Универсальныйй
    url(r'^cell_update/$', views.cell_update, name='cell_update'),

#Вещества реакции
    url(r'^reaction/(?P<id_reaction>[0-9]+)/substance/all/$', views.react_substance_all, name='react_substance_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/substance/new/$', views.react_substance_new, name='react_substance_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/substance/(?P<id_react_substance>[0-9]+)/detail/$',
        views.react_substance_detail, name='react_substance_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/substance/(?P<id_react_substance>[0-9]+)/delete/$',
        views.react_substance_delete, name='react_substance_delete'),


#Серии для Экспериментов
    url(r'^reaction/(?P<id_reaction>[0-9]+)/exper_serie/new/$', views.exper_serie_new, name='exper_serie_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/exper_serie/(?P<id_exper_serie>[0-9]+)/detail/$',
        views.exper_serie_detail, name='exper_serie_detail'),

#Эксперименты
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/all/$', views.experiment_all, name='experiment_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/search/$', views.experiment_all_search, name='experiment_all_search'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/search/(?P<searched>[\w\-\.\,\!\?\\\:\;\s]+)/$',
        views.experiment_all_search, name='experiment_all_search'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/detail/$',
        views.experiment_detail, name='experiment_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/new/$', views.experiment_new, name='experiment_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/new/(?P<id_exper_serie>[0-9]+)/$', views.experiment_new, name='experiment_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/edit/$',
        views.experiment_edit, name='experiment_edit'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/copy/$',
        views.experiment_copy, name='experiment_copy'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/delete/$',
        views.experiment_delete, name='experiment_delete'),

#Задачи
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/all/$', views.problem_all, name='problem_all'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/new/(?P<id_problem_type>[0-9]+)/$', views.problem_new, name='problem_new'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/(?P<id_problem>[0-9]+)/detail/$', views.problem_detail, name='problem_detail'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/(?P<id_problem>[0-9]+)/edit/$', views.problem_edit, name='problem_edit'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/(?P<id_problem>[0-9]+)/init/$', views.problem_init, name='problem_init'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/(?P<id_problem>[0-9]+)/calc_options/$', views.problem_calc_options, name='problem_calc_options'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/(?P<id_problem>[0-9]+)/calc_state/$', views.problem_calc_state, name='problem_calc_state'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/(?P<id_problem>[0-9]+)/results/$', views.problem_results, name='problem_results'),
    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/(?P<id_problem>[0-9]+)/delete/$', views.problem_delete, name='problem_delete'),

#Решения
   url(r'^calculation/all/$', views.calculation_all, name='calculation_all'),
   url(r'^reaction/(?P<id_reaction>[0-9]+)/calc/all/$', views.calc_all, name='calc_all'),

#Статистика
   url(r'^reaction/(?P<id_reaction>[0-9]+)/statistic/$', views.statistic, name='statistic'),

#Журнал изменений
   url(r'^reaction/(?P<id_reaction>[0-9]+)/log/$', views.log, name='log'),
]
