# -*- coding: utf-8 -*-
import logging

import json

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from chemical.models import owner_required, substance_owner_required
from chemical.urls_utils import make_name_link
from chemical.urls_utils import get_subst_detail_link
from chemical.utils import decorate_formula
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

@login_required
@substance_owner_required
def substance_detail_edit(request, id_substance):
    subst = request.user.chemistry.substance_get(id_substance)

    data = '{"result":"ok", "message":"ok"}'
    xml_bytes = json.dumps(data)

    if request.is_ajax():
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            field_name = body['field_name']
            value = body['value']
            setattr(subst, field_name, value)

            if field_name == 'formula_brutto':
                subst.formula_brutto_formatted = decorate_formula(subst.formula_brutto)
                subst.consist_create()

            subst.save()

    return HttpResponse(xml_bytes, 'application/json')


@login_required
@owner_required
def reaction_detail_edit(request, id_reaction):
    #print('get react')
    ureact = request.user.chemistry.reaction_get(id_reaction)
    react = ureact.reaction

    data = '{"result":"ok", "message":"ok"}'
    xml_bytes = json.dumps(data)

    if request.is_ajax():
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            field_name = body['field_name']
            value = body['value']
            #print(field_name)
            #print(value)
            setattr(react, field_name, value)

            react.save()
            #print('after_save')
            #print(react.name)
    return HttpResponse(xml_bytes, 'application/json')


