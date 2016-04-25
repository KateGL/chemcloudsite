# -*- coding: utf-8 -*-
import logging

import json

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.db import models

from chemical.models import owner_required, substance_owner_required
from chemical.urls_utils import make_name_link
from chemical.urls_utils import get_subst_detail_link
from chemical.utils import decorate_formula
# Create your views here.

def set_field_and_value_from_request(request, my_model):
    data = '{"result":"True", "message":"ok"}'
    if request.is_ajax():
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            field_name = body['field_name']
            value = body['value']

            if isinstance(my_model._meta.get_field(field_name), models.BooleanField):
                value = (value.lower() == 'true')
            #print(my_model._meta.get_field(field_name).get_internal_type())
            setattr(my_model, field_name, value)
            return {"is_error": False, "err_msg": data, "field_name": field_name, "value": value}

    data = '{"result":"False", "message":"Request not Ajax or not POST"}'
    return {"is_error": True,"err_msg": data}


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
    fv_dict = set_field_and_value_from_request(request, subst)

    if (fv_dict['is_error'] is False):
        if fv_dict['field_name'] == 'formula_brutto':
            subst.formula_brutto_formatted = decorate_formula(subst.formula_brutto)
            subst.consist_create()
        subst.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


@login_required
@owner_required
def reaction_detail_edit(request, id_reaction):
    ureact = request.user.chemistry.reaction_get(id_reaction)
    react = ureact.reaction
    fv_dict = set_field_and_value_from_request(request, react)

    if (fv_dict['is_error'] is False):
        react.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


@login_required
@owner_required
def react_substance_detail_edit(request, id_reaction, id_react_substance):
    subst_dict = request.user.chemistry.react_subst_get(id_reaction, id_react_substance)
    rsubst = subst_dict['substance']
    fv_dict = set_field_and_value_from_request(request, rsubst)

    if (fv_dict['is_error'] is False):
        rsubst.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


@login_required
@owner_required
def scheme_detail_edit(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    scheme = scheme_dict['scheme']
    fv_dict = set_field_and_value_from_request(request, scheme)

    if (fv_dict['is_error'] is False):
        scheme.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')