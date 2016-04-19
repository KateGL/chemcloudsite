# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from chemical.models import owner_required
from chemical.urls_utils import make_name_link
from chemical.urls_utils import get_subst_detail_link
# Create your views here.

@login_required
def substance_search(request, searched):
    tmp = searched + ' Hello, World!'
    return HttpResponse(tmp)


@login_required
def substance_search_hint(request, searched):
    subst = request.user.chemistry.substance_get_like(searched, 3)
    tmp = ''
    for value in subst.values():
        if tmp > '':
            tmp = tmp + ', '
        lnk = get_subst_detail_link(value['id_substance'])
        tmp = tmp + make_name_link(lnk, value['name']) + ' (' + value['formula_brutto_formatted'] + ')'
    return HttpResponse(tmp)
