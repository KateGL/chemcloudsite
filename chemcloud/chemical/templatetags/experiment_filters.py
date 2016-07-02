# -*- coding: utf-8 -*-
from django import template

register = template.Library()


# value Exper_arg_value, arg id_expersubst
#only one point by expersubst
@register.filter
def get_points_from_arg_by_expersubst(value, arg):
    point = value.exper_func_points.filter(exper_subst__pk=arg)
    if len(point)>0:
        return point[0].func_val
    else:
        return ''

#register.filter('get_points_from_arg_by_expersubst', get_points_from_arg_by_expersubst)