# -*- coding: utf-8 -*-
from django.conf.urls import url

#import chemical.views
from chem_ajax import views

urlpatterns = [
#Вещества

    url(r'^substance/search_hint/(?P<searched>[\w\-\.\,\!\?\\\:\;\s]+)/(?P<top_count>[0-9]+)/$',
        views.substance_search_hint, name='substance_search_hint'),

    url(r'^substance/search_list/$', views.substance_search_list, name='substance_search_list'),

    url(r'^substance/(?P<id_substance>[0-9]+)/detail_edit/$', views.substance_detail_edit, name='substance_detail_edit'),
    url(r'^substance/check_isomer/$', views.substance_check_isomer, name='substance_check_isomer'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/detail_edit/$', views.reaction_detail_edit, name='reaction_detail_edit'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/substance/(?P<id_react_substance>[0-9]+)/detail_edit/$',
        views.react_substance_detail_edit, name='react_substance_detail_edit'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/scheme/(?P<id_scheme>[0-9]+)/detail_edit/$',
        views.scheme_detail_edit, name='scheme_detail_edit'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/step/(?P<id_scheme>[0-9]+)/(?P<id_step>[0-9]+)/detail_edit/$',
        views.step_detail_edit, name='step_detail_edit'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/detail_edit/$',
        views.experiment_detail_edit, name='experiment_detail_edit'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/edit_subst/$',
        views.experiment_edit_subst, name='experiment_edit_subst'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/experiment/(?P<id_experiment>[0-9]+)/edit_point/$',
        views.experiment_edit_point, name='experiment_edit_point'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/exper_serie/(?P<id_exper_serie>[0-9]+)/detail_edit/$',
        views.exper_serie_detail_edit, name='exper_serie_detail_edit'),

    url(r'^reaction/(?P<id_reaction>[0-9]+)/problem/(?P<id_problem>[0-9]+)/detail_edit/$',
        views.problem_detail_edit, name='problem_detail_edit'),

    url(r'^dictionary/get/$', views.dictionary_get, name='dictionary_get'),
    url(r'^exper_serie/get/(?P<id_reaction>[0-9]+)/$', views.exper_serie_get, name='exper_serie_get'),

    ]