# -*- coding: utf-8 -*-
import logging

import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db import models
import swapper
import time
from datetime import datetime
from decimal import Decimal

from chemical.models import owner_required, substance_owner_required, Chemistry
from chemical.urls_utils import make_name_link, make_detail_link
from chemical.urls_utils import get_subst_detail_link
from chemical.utils import decorate_formula
from chemical.models import substance_get_isomer, substance_get_isomer_count
from chemical.chemical_models import consist_to_string, Exper_subst, Exper_func_point
# Create your views here.


def set_field_value_to_model(field_name, value_tmp, my_model):
    data = '{"result":"True", "message":"ok"}'
    field_object = my_model._meta.get_field(field_name)
    #print(field_object)
    #если это ссылка на класс
    if isinstance(field_object, models.ForeignKey):
        try:
            rel_model = field_object.rel.to
            #print(rel_model)
            value = rel_model.objects.get(pk=value_tmp)
            #print(value)
        except:  # ахтунг! не очень клево, т.к. может скрыть ошибки
            #print(value)
            value = None
        #если это булево поле
    elif isinstance(field_object, models.BooleanField):
        value = (value_tmp.lower() == 'true')
    elif isinstance(field_object, models.DateTimeField):
        tmp_val = time.strptime(value_tmp, "%d.%m.%Y %H:%M")
        tmp_val = datetime.fromtimestamp(time.mktime(tmp_val))
        value = tmp_val
    elif isinstance(field_object, models.DecimalField):
        tmp_val = value_tmp.strip(' \t\n\r')
        #print(tmp_val)
        value = Decimal(tmp_val)
    else:
        value = value_tmp

    #print(my_model)
    #print(field_name)
    #print(value)
    setattr(my_model, field_name, value)
    return {"is_error": False, "err_msg": data, "field_name": field_name, "value": value}


def set_field_and_value_from_request(request, my_model):
    if request.is_ajax():
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            #print(body)
            field_name = body['field_name']
            value_tmp = body['value']
            #print(field_name)
            return set_field_value_to_model(field_name, value_tmp, my_model)

    data = '{"result":"False", "message":"Request not Ajax or not POST"}'
    return {"is_error": True, "err_msg": data}


@login_required
def substance_search_hint(request, searched='', top_count=0):
    subst = request.user.chemistry.substance_get_like(searched, top_count)
    tmp = ''
    for value in subst.values():
        if tmp > '':
            tmp = tmp + ', '
        lnk = get_subst_detail_link(value['id_substance'])
        tmp = tmp + make_name_link(lnk, value['name']) + ' (' + value['formula_brutto_formatted'] + ')'
    return HttpResponse(tmp)


@login_required
def substance_search_list(request):
    #print('Hi!')
    #print(request.method)
    if request.method != 'GET':
        return False
    top_count = 50  # request.GET['top_count']
    searched = request.GET['q']

    data = {}
    substance_list = []
    if searched != '':
        subst = request.user.chemistry.substance_get_like(searched, top_count)
        data['total_count'] = subst.count()
        data['incomplete_results'] = False
        for value in subst.values():
            dict_val = {}
            dict_val['id'] = value['id_substance']
            dict_val['name'] = value['name']
            dict_val['formula_brutto_formatted'] = value['formula_brutto_formatted']
            dict_val['formula_brutto'] = value['formula_brutto']
            lnk = get_subst_detail_link(value['id_substance'])
            dict_val['detail_link'] = make_detail_link(lnk)
            #print(dict_val)
            substance_list.append(dict_val)
    #print(substance_list)
    data['items'] = substance_list
    xml_bytes = json.dumps(data)
    return HttpResponse(xml_bytes, 'application/json')


@login_required
def substance_check_isomer(request):
    if request.method != 'GET':
        return False
    brutto_formula = request.GET['brutto_formula']
    #top_count = request.GET['top_count']
    consist_as_string = consist_to_string(brutto_formula)
    #subst_dict = substance_get_isomer(consist_as_string, top_count)
    isomers_cnt = substance_get_isomer_count(consist_as_string)

    isomer_dict = {}
    isomer_dict['isomer_count'] = isomers_cnt
    isomer_dict['consist_as_string'] = consist_as_string
    #print(isomer_dict)
    #isomer_dict['values'] = serializers.serialize('json', subst_dict)
    #isomer_dict['models'] = subst_dict
    xml_bytes = json.dumps(isomer_dict)
    #xml_bytes = serializers.serialize('json', subst_dict)
    return HttpResponse(xml_bytes, 'application/json')


@login_required
@substance_owner_required
def substance_detail_edit(request, id_substance):
    subst = request.user.chemistry.substance_get(id_substance)
    fv_dict = set_field_and_value_from_request(request, subst)

    if (fv_dict['is_error'] is False):
        if fv_dict['field_name'] == 'formula_brutto':
            subst.after_create()
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
    print(fv_dict)
    if (fv_dict['is_error'] is False):
        if fv_dict['field_name'] == 'brutto_formula_short':
            rsubst.after_create()
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


@login_required
@owner_required
def step_detail_edit(request, id_reaction, id_scheme, id_step):
    step_dict = request.user.chemistry.rscheme_step_get(id_reaction, id_scheme, id_step)
    step = step_dict['step']
    fv_dict = set_field_and_value_from_request(request, step)

    if (fv_dict['is_error'] is False):
        step.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


@login_required
@owner_required
def exper_serie_detail_edit(request, id_reaction, id_exper_serie):
    exper_serie_dict = request.user.chemistry.exper_serie_get(id_reaction, id_exper_serie)
    exper_serie = exper_serie_dict['exper_serie']
    fv_dict = set_field_and_value_from_request(request, exper_serie)

    if (fv_dict['is_error'] is False):
        exper_serie.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


@login_required
@owner_required
def experiment_detail_edit(request, id_reaction, id_experiment):
    exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    exper = exper_dict['experiment']

    fv_dict = set_field_and_value_from_request(request, exper)

    if (fv_dict['is_error'] is False):
        exper.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


def get_fvr_dict(request):
    if request.is_ajax():
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            #print(body)
            field_name = body['field_name']
            value_tmp = body['value']
            record_id = body['record_id']
            #print(field_name)
            data = '{"result":"True", "message":"ok"}'
            return {"is_error": False, "err_msg": data, "field_name": field_name, "value": value_tmp, "record_id": record_id}

    data = '{"result":"False", "message":"Request not Ajax or not POST"}'
    return {"is_error": True, "err_msg": data}


def get_point_fvr_dict(request):
    if request.is_ajax():
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            #print(body)
            field_name = body['field_name']
            value_tmp = body['value']
            arg_id = body['argument_id']
            subst_id = body['substance_id']
            #print(field_name)
            data = '{"result":"True", "message":"ok"}'
            return {"is_error": False, "err_msg": data, "field_name": field_name, "value": value_tmp, "argument_id": arg_id,
                "substance_id": subst_id}

    data = '{"result":"False", "message":"Request not Ajax or not POST"}'
    return {"is_error": True, "err_msg": data}


@login_required
@owner_required
def experiment_edit_subst(request, id_reaction, id_experiment):
    exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    exper = exper_dict['experiment']
    #value = None
    fvr_dict = get_fvr_dict(request)
    rec_id = fvr_dict['record_id']

    react_subst_dict = request.user.chemistry.react_subst_get(id_reaction, rec_id)
    react_subst = react_subst_dict['substance']
    exper_subst_list = exper.exper_substs.filter(reaction_subst=react_subst)

    exper_subst = None
    if exper_subst_list.count() > 0:
        exper_subst = exper_subst_list[0]
    else:
        exper_subst = Exper_subst(experiment=exper, reaction_subst=react_subst)
    #get or create exper_subst

    fv_dict = set_field_value_to_model(fvr_dict['field_name'], fvr_dict['value'], exper_subst)
    #print(fv_dict)
    if (fv_dict['is_error'] is False):
        exper_subst.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


@login_required
@owner_required
def experiment_edit_point(request, id_reaction, id_experiment):
    #exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    #exper = exper_dict['experiment']
    #value = None
    fvr_dict = get_point_fvr_dict(request)
    point = request.user.chemistry.exper_point_get(fvr_dict['substance_id'], fvr_dict['argument_id'])
    print(point)

    if point is None:
        #print('make new point')
        esubst = request.user.chemistry.exper_subst_get(fvr_dict['substance_id'])
        arg = request.user.chemistry.exper_arg_get(fvr_dict['argument_id'])
        new_point = Exper_func_point(exper_subst=esubst, argument=arg, func_val=fvr_dict['value'])
        new_point.save()
        #esubst.exper_func_points.add(new_point, bulk=False)
    else:
        print('edit point')#тупо редактируем аргумент
        point.func_val = fvr_dict['value']
        point.save()

    xml_bytes = json.dumps(fvr_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


@login_required
@owner_required
def problem_detail_edit(request, id_reaction, id_problem):
    problem_dict = request.user.chemistry.problem_get(id_reaction, id_problem)
    problem = problem_dict['problem']
    fv_dict = set_field_and_value_from_request(request, problem)

    if (fv_dict['is_error'] is False):
        problem.save()

    xml_bytes = json.dumps(fv_dict['err_msg'])
    return HttpResponse(xml_bytes, 'application/json')


@login_required
def dictionary_get(request):
    if request.method != 'GET':
        return False
    #print('start view')
    model_name = request.GET['model_name']
    #print(model_name)
    my_model = swapper.load_model('chemical', model_name)
    model_dict = {}

    for mdl in my_model.objects.all():
        model_dict[mdl.pk] = mdl.name

    xml_bytes = json.dumps(model_dict)
    #print(xml_bytes)
    #print('end eiw')
    return HttpResponse(xml_bytes, 'application/json')


@login_required
def exper_serie_get(request, id_reaction):
    if request.method != 'GET':
        return False
    series_all = request.user.chemistry.exper_serie_all(id_reaction)

    model_dict = {}
    model_dict[0] = '--------'

    for mdl in series_all:
        model_dict[mdl.pk] = mdl.name

    xml_bytes = json.dumps(model_dict)
    #print(xml_bytes)
    #print('end eiw')
    return HttpResponse(xml_bytes, 'application/json')
