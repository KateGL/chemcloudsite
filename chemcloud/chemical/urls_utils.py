# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.safestring import mark_safe


def make_detail_link(link):
    return mark_safe(''' <a href="%s">Детали</a>''' % link)


def make_isomer_link(link):
    return mark_safe(''' <a href="%s">Изомеры</a>''' % link)


def make_name_link(link, name):
    return mark_safe(''' <a href="%s">%s</a>''' % (link, name))


def get_subst_detail_link(id_subst):
    return '/chemical/substance/' + str(id_subst) + '/detail/'