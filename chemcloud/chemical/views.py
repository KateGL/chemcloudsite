# -*- coding: utf-8 -*-
import logging
import re
import json
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core import serializers
from django.core.urlresolvers import reverse

# Create your views here.
from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from chemical.tables import AtomTable, SubstanceTable, ReactionTable
from chemical.tables import ConsistTable, MechanizmTable, ReactionSubstTable, ExperimentTable, ProblemTable
from chemical.tables import StepsTable, UserOfReactionTable


from django.shortcuts import redirect
from chemical.forms import SubstanceForm, ReactionForm, ReactionSubstForm, ReactionShareForm, ProblemForm, ExperSerieForm
from .forms import ReacSchemeForm, ExperimentForm
from .models import substance_get_isomer_count, substance_get_isomer
from .models import owner_required, substance_owner_required
from .view_helpers import React_Substance_with_Exper, Series_and_Exper
from .urls_utils import make_detail_link

from chemcloud.celery import add
from celery.result import ResultBase
from celery.result import AsyncResult
import time
# Вещество


@login_required
def substance_all(request):
    substance_table = SubstanceTable(request.user.chemistry.substance_all())
    is_substance_owner = request.user.chemistry.is_substance_owner
    RequestConfig(request, paginate={"per_page": 25}).configure(substance_table)
    return render(request, 'chemical/substance_all.html', {"substance": substance_table, "is_owner": is_substance_owner})


@login_required
def substance_all_search(request, searched=''):
    substance_table = SubstanceTable(request.user.chemistry.substance_get_like(searched, 0))
    is_substance_owner = request.user.chemistry.is_substance_owner
    RequestConfig(request, paginate={"per_page": 25}).configure(substance_table)
    return render(request, 'chemical/substance_all.html',
    {"substance": substance_table, "searched": searched, "is_owner": is_substance_owner})


@login_required
def substance_isomers(request, consist_string=''):
    substance_table = SubstanceTable(substance_get_isomer(consist_string, 0))
    RequestConfig(request, paginate={"per_page": 25}).configure(substance_table)
    return render(request, 'chemical/substance_isomer.html',
    {"substance": substance_table, "id_substance": 0, "formula_brutto": consist_string})


@login_required
def substance_detail(request, id_substance):
    substance = request.user.chemistry.substance_get(id_substance)
    consist_table = ConsistTable(substance.consist.all())
    is_substance_owner = request.user.chemistry.is_substance_owner
    isomer_count = substance_get_isomer_count(substance.consist_as_string) - 1
    return render(request, 'chemical/substance_detail.html',
    {"substance": substance, "substance_consist": consist_table, "isomer_count": isomer_count,
        "is_owner": is_substance_owner})


@login_required
@substance_owner_required
def substance_new(request):
    form = SubstanceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            substance = form.save()
            substance.after_create()
            form.save()
            #print(request.POST)
            if 'save_and_new_btn' in request.POST:
                return redirect('substance_new')
            return redirect('substance_detail', substance.pk)
    return render(request, 'chemical/substance_new.html', {'form': form})



# расчеты
@login_required
def calculation_all(request):
    return render(request, 'chemical/calculation_all.html', {})


# атом
@login_required
def atoms_all(request):
    atom_table = AtomTable(request.user.chemistry.atom_all())
    RequestConfig(request, paginate={"per_page": 30}).configure(atom_table)
    return render(request, 'chemical/atom_all.html', {"atom": atom_table})


@login_required
def atom_detail(request, atom_number):
    atom = request.user.chemistry.atom_get(atom_number)
    return render(request, 'chemical/atom_detail.html', {"atom": atom})


# Справочники
@login_required
def dictionaries(request):
    return render(request, 'chemical/dictionaries.html', {})


# Реакции
@login_required
def reaction_all(request, searched=''):
    print(searched)
    if searched == '':
        reactions = request.user.chemistry.reaction_all()
    else:
        reactions = request.user.chemistry.reaction_search(searched)
    reaction_table = ReactionTable(reactions)
    RequestConfig(request, paginate={"per_page": 15}).configure(reaction_table)
    return render(request, 'chemical/reaction_all.html', {"reaction": reaction_table, "searched": searched})


@login_required
def reaction_detail(request, id_reaction):
    react = request.user.chemistry.reaction_get(id_reaction)
    user_reacts = UserOfReactionTable(react.reaction.users.all())
    react_features = request.user.chemistry.react_feature_all(id_reaction)
    form = ReactionShareForm(request.POST or None)
    rights = 'cc'
    if request.method == 'POST':
        if form.is_valid() & react.is_owner:
            user = request.user.chemistry.get_user_by_email(form.cleaned_data['user_email'])
            rights = form.cleaned_data['rights']
            if rights == '1':
                react.reaction.share_to_user(user, True)
            else:
                react.reaction.share_to_user(user, False)
            #form.cleaned_data['message'])  , 'text': str(form.cleaned_data['rights']
    return render(request, 'chemical/reaction_detail.html',
         {"reaction": react.reaction, "id_reaction": id_reaction, "is_owner": react.is_owner,
              'form': form, 'user_reacts': user_reacts, 'react_features': react_features})


@login_required
def reaction_copy(request, id_reaction):
    #empty now TODO
    return redirect('reaction_detail', id_reaction)


@login_required
def reaction_report(request, id_reaction):
    #empty now TODO
    return redirect('reaction_detail', id_reaction)


@login_required
@owner_required
def reaction_delete(request, id_reaction):
    #тут нужно добавить обработчик ошибок... Для случаев, когда удаление реакции запрещено
    #например, если по реакции есть расчеты
    react = request.user.chemistry.reaction_get(id_reaction)
    react.reaction.delete()
    return redirect('reaction_all')  # или лушче на сообщение - "Реакция удалена?"


@login_required
def reaction_new(request):
    form = ReactionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            reaction = form.save()
            reaction.add_owner(request.user)
            form.save()
            return redirect('reaction_detail', reaction.pk)
    return render(request, 'chemical/reaction_new.html', {'form': form})


#  Механизмы реакции
@login_required
def scheme_all(request, id_reaction):
    mech_table = MechanizmTable(request.user.chemistry.react_scheme_all(id_reaction))
    context_dict = {'schemes': mech_table, 'id_reaction': id_reaction}
    return render(request, 'chemical/scheme_all.html', context_dict)


@login_required
def scheme_detail(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    context = {'scheme': scheme_dict['scheme'], 'id_reaction': id_reaction, 'is_owner': scheme_dict['is_owner']}
    return render(request, 'chemical/scheme_detail.html', context)


#@login_required
#test for dataTable
def scheme_edit_json(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    #получаем список стадий схемы
    steps = scheme_dict['scheme'].steps.all()
#    json = serializers.serialize('json', steps)
    data = '{"pk": 1, "fields": {"name": "1"}}'
    xml_bytes = json.dumps(data)
    return HttpResponse(xml_bytes, content_type='application/json')

@login_required
def scheme_edit(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    #получаем список стадий схемы
    steps = scheme_dict['scheme'].steps.all()
    rst = ReactionSubstTable(request.user.chemistry.react_subst_all(id_reaction))
    RequestConfig(request, paginate={"per_page": 25}).configure(rst)
    context = {'steps': steps, 'id_reaction': id_reaction, 'scheme_name': scheme_dict['scheme'].name,
        'is_owner': scheme_dict['is_owner'], 'reac_substs': rst, 'id_scheme': id_scheme }
    return render(request, 'chemical/scheme_edit.html', context)


@login_required
@owner_required
def scheme_delete(request, id_reaction, id_scheme):
    #тут нужно добавить обработчик ошибок...
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    scheme_dict['scheme'].delete()
    return redirect('scheme_all', id_reaction)#или лушче на сообщение - "?"


@login_required
@owner_required
def scheme_copy(request, id_reaction, id_scheme):
    #empty now TODO
    return redirect('scheme_detail', id_reaction, id_scheme)


@login_required
def scheme_report(request, id_reaction, id_scheme):
    #empty now TODO
    return redirect('scheme_detail', id_reaction, id_scheme)

@login_required
def scheme_check_balance(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    scheme = scheme_dict['scheme'];
    balance_mess = []
    bad_steps = []
    result = 'True'
    balance_bool = scheme.check_scheme_balance(balance_mess)
    mess = ''
    tr_class=''
    if not balance_bool:
        mess = balance_mess[0]
        result = 'False'
        tr_class = 'danger'
    data = '{"result":"' + result  +'", "messageText": "' + mess + '", "tr_class":"'+ tr_class +'"}'
    xml_bytes = json.dumps(data)
    return HttpResponse(xml_bytes,'application/json')

@login_required
def step_detail(request, id_reaction, id_scheme, id_step):
    step_dict = request.user.chemistry.rscheme_step_get(id_reaction, id_scheme, id_step)
    context = {'step': step_dict['step'], 'id_reaction' : id_reaction, 'is_owner': step_dict['is_owner']}
    return render(request, 'chemical/step_detail.html', context)

@login_required
@owner_required
def scheme_new(request, id_reaction):
    react = request.user.chemistry.reaction_get(id_reaction)

    form = ReacSchemeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            scheme = form.save(commit=False)
            scheme.reaction = react.reaction
#            scheme.name = form.cleaned_data['name']
#            scheme.description = form.cleaned_data['description']
#            scheme.is_possible = form.cleaned_data['is_possible']
        #  scheme.fcreated_date = timezone.now
        #    scheme.fupdated_date = timezone.now
#            scheme.updated_by = request.user
#            scheme.created_by = request.user
#            scheme.save()
            form.save()
            return redirect('scheme_detail', id_reaction, scheme.pk)

    context = {'id_reaction': id_reaction, 'form': form}
    return render(request, 'chemical/scheme_new.html', context)

@login_required
def cell_update(request):
    if not request.is_ajax():
        return HttpResponse(status=400)
    table_str = ''
    id_str = ''
    field_str = ''
    value_str = ''
    if request.method != 'POST':
        return HttpResponse(status=400)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    table_str = body['table']
    id_str    = body['id']
    field_str = body['field']
    value_str = body['value']

    data = '';
    #таблица стадий механизма
    pos = table_str.find('all-steps');
    if pos != -1:
        #обработка редактирования стадий
        data = scheme_cell_update(request, table_str, id_str, field_str, value_str )

    if data != '':
        xml_bytes = json.dumps(data)
        return HttpResponse(xml_bytes,'application/json')

    #сюда для других таблиц вставлять свои проверки названия таблицы и соответствующие обработчики
    return HttpResponse(
            json.dumps('{"result": "error", "errorText": "unknown error"}'),
            content_type="application/json"
        )


def _create_step_part(request, id_reaction, step, is_left, part_str, start_i ):
    arr2 = part_str.split('+')
    i = start_i
    list_temp = []
    for str_i in arr2:
        #убрать пробелы. Отделить псевдоним от стехиометрического коэффициента
        #поиск соответствующего вещества реакции, если нет - ошибка
        #subst_list = request.user.chemistry.react_subst_all(id_reaction)
        str_temp = str_i.strip()
        #ищем любую латинскую букву или букву кириллицы - это значит начало псевдонима. Все , что до - это стех.коэффициент а-яА-ЯёЁa-zA-Z0-9
        req_res = re.search(u'([A-Za-zа-яА-ЯёЁ]+\d*)', str_temp) #r перед строкой - включение сырого режима. Отключение экранирования
        if req_res == None:
            return []
        start_pos = req_res.start()
        alias = str_temp[start_pos:]
        steh_koef = 1.000;
        if start_pos > 0:
            steh_koef_str = str_temp[0:req_res.start()]
            try:
                steh_koef = float(steh_koef_str)
            except:
                return []
                #raise Http404("Ошибка ввода стехиометрического коэффициента: " + steh_koef_str)
        if steh_koef <= 0:
            return []
        if is_left:
            steh_koef = -1.0*steh_koef
        subst_dict = request.user.chemistry.react_subst_filterbyAlias(id_reaction, alias)
        if subst_dict=={}:
            return []
        reac_subst = subst_dict['substance']
        element = [i, steh_koef, reac_subst]
        i=i+1
        list_temp = list_temp + [element]
    return list_temp

def scheme_cell_update(request, table_str, id_str, field_str, value_str ):
    arr = table_str.split('_');
    id_reaction = int(arr[1])
    id_scheme   = int(arr[2])
    step_id = int(id_str)

    step_dict = request.user.chemistry.rscheme_step_get(id_reaction, id_scheme, int(step_id))
    step = step_dict['step']
    result = 'success'
    errorText = ''
    if field_str == 'name':
        step.name = value_str.strip(' ')
    if field_str == 'step':
        step_str = value_str.strip(' ')
        left_str = ''
        right_str = ''
        pos=step_str.find('<->')
        arr2 = []
        if pos != -1:
            step.is_revers = True
            arr2 = value_str.split('<->')
        else:
            pos = step_str.find('->')
            if pos != -1:
                step.is_revers = False
                arr2 = value_str.split('->')
            else:
                result = 'error'
                errorText = 'Неправильно введен флаг обратимости стадии'
        if pos != -1:
            if len(arr2) != 2:
                result = 'error'
                errorText = 'Введено несколько флагов обратимости'
            else:
                left_str = arr2[0]
                right_str = arr2[1]
                data_list=[]
                data_list_left = _create_step_part(request, id_reaction, step, True, left_str, 0)
                data_list_rigth = []
                if len(data_list_left) > 0:
                    data_list_rigth = _create_step_part(request, id_reaction, step, False, right_str, len(data_list_left))
                    data_list = data_list_left+data_list_rigth
                if len(data_list_left) == 0 or len(data_list_rigth) == 0 or not step.generate_step_from_str(data_list):
                    result = 'error'
                    errorText = 'Ошибка распознавания и сохранения стадии'
                    if len(data_list) == 0:
                        errorText = errorText + '. Некорректно введены левая и правая части'
                    elif len(data_list_left) == 0:
                        errorText = errorText + '. Некорректно введена левая часть'
                    elif len(data_list_rigth) == 0:
                        errorText = errorText + '. Некорректно введена правая часть'
                    else:
                        errorText = errorText + '. Убедитесь, что одно и то же вещество не содержится одновременно в левой и правой частях стадии '
                    errorText = errorText + '. Проверьте соответствие введенных псевдонимов веществам и корректность введенных стехиометрических коэффициентов.'
    mess = ''
    tr_class = ''
    info_iconName = ''
    info_iconText=''
    if result == 'success':
        step.save()
        balance_mess = []
        balance_bool = True

        info_iconName = 'glyphicon glyphicon-ok glyphicon-good_balance'
        info_iconText = 'Закон сохранения массы выполняется'
        if field_str == 'step':
            balance_bool = step.check_step_balance(balance_mess)
        if not balance_bool:
            #mess = balance_mess[0]
            #tr_class = 'danger'
            info_iconName = 'glyphicon glyphicon-exclamation-sign glyphicon-bad_balance'
            info_iconText = balance_mess[0]
    data = '{"result":"' + result  +'", "errorText": "' + errorText + '", "messageText": "' + mess + '", "tr_class":"'+ tr_class +'", "info_iconText": "' + info_iconText + '", "info_iconName":"'+ info_iconName +'" }'
    return data


@login_required
def step_delete(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    steps = scheme_dict['scheme'].steps.all()
    #удалить текущую стадию, у всех следующих после текущей стадии понизить на 1 порядок
    step_id = ''
    if request.method == 'GET':
        step_id = request.GET['step_id']
    if step_id:
        step_dict = request.user.chemistry.rscheme_step_get(id_reaction, id_scheme, int(step_id))
        step = step_dict['step']
        cur_step_order = step.order
        for temp_step in steps:
            if temp_step.order > cur_step_order:
                temp_step.order = temp_step.order - 1
                temp_step.save()
        step.delete()
        #todo спросить
        data = '{"result":"success", "deleted_step_order": "'+ str(cur_step_order) + '"}'
        xml_bytes = json.dumps(data)
        return HttpResponse(xml_bytes,'application/json')
    return HttpResponse(status=400)


@login_required
def step_new(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    scheme = scheme_dict['scheme'];
    new_step = scheme.create_new_emptystep();
    if new_step == -1:
        return HttpResponse(status=400)
    link_detail = reverse('step_detail', args=[id_reaction, id_scheme, new_step.id_step ])
    link_changeorder = reverse('change_step_order', args=[id_reaction, id_scheme ])
    link_delete = reverse('step_delete', args=[id_reaction, id_scheme ])

    data = '{"id_step":"' + str(new_step.id_step) +'", "order":"'+str(new_step.order) + '", "name": "'+new_step.name+'", "url_detail": "'+ link_detail+'", "url_changeorder": "' + link_changeorder+'", "url_delete": "' + link_delete +'"}'
    #fv_dict = {"id_step": new_step.id_step, "order":new_step.order, "name": new_step.name, "url_detail": link_detail, "url_changeorder": link_changeorder}
    xml_bytes = json.dumps(data)
    return HttpResponse(xml_bytes,'application/json')


#изменение порядка стадии
@login_required
def change_step_order(request, id_reaction, id_scheme):
#    if not request.is_ajax():
#        return HttpResponse(status=400)
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    #получаем список стадий схемы
    steps_count = scheme_dict['scheme'].steps.count()

    step_id = None
    direction = None
    if request.method == 'GET':
        step_id = request.GET['step_id']
        direction = request.GET['direction']
    #todo проверки на соответствие шага схемы схеме и реакции
    new_order = -1
    cur_order = -1
    cur_id = -1
    neighbor_id = -1
    if step_id:
        step_dict = request.user.chemistry.rscheme_step_get(id_reaction, id_scheme, int(step_id))
        step = step_dict['step']
        cur_order = step.order
        cur_id = step.id_step
        if step:
            if direction == 'up' and cur_order>1:
                new_order = cur_order - 1
                step_neighbor_dict = request.user.chemistry.rscheme_step_get_byorder(id_reaction, id_scheme, new_order)
                step_neighbor = step_neighbor_dict['step']
                neighbor_id = step_neighbor.id_step
                step.order = new_order
                step_neighbor.order = cur_order
                step.save()
                step_neighbor.save()
            if direction == 'down' and cur_order<steps_count:
                new_order = cur_order + 1
                step_neighbor_dict = request.user.chemistry.rscheme_step_get_byorder(id_reaction, id_scheme, new_order)
                step_neighbor = step_neighbor_dict['step']
                step.order = new_order
                step_neighbor.order = cur_order
                neighbor_id = step_neighbor.id_step
                step.save()
                step_neighbor.save()
    if cur_id != -1 and neighbor_id != -1:
      #  format_str = 'json'
        mimetype = 'application/json'
        data = '{"cur_step_order": ' + str(new_order) +', "neighbor_step_order":'+str( cur_order) + ', "cur_step_id": '+str(cur_id)+', "neighbor_step_id": '+str(neighbor_id)+', "steps_count": '+str(steps_count)+' }'
        xml_bytes = json.dumps(data)
       # data = serializers.serialize(format_str, data)
        return HttpResponse(xml_bytes,mimetype)
    return HttpResponse(status=400)


#Вещества реакции
@login_required
def react_substance_all(request, id_reaction):
    rst = ReactionSubstTable(request.user.chemistry.react_subst_all(id_reaction))
    RequestConfig(request, paginate={"per_page": 25}).configure(rst)
    context_dict = {}
    context_dict['substance'] = rst
    context_dict['id_reaction'] = id_reaction
    return render(request, 'chemical/react_substance_all.html', context_dict)


@login_required
@owner_required
def react_substance_new(request, id_reaction):
    react = request.user.chemistry.reaction_get(id_reaction)

    form = ReactionSubstForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            react_substance = form.save(commit=False)
            react_substance.reaction = react.reaction
            react_substance.after_create()
            form.save()
            if 'save_and_new_btn' in request.POST:
                return redirect('react_substance_new', id_reaction)
            return redirect('react_substance_detail', id_reaction, react_substance.pk)

    rst = ReactionSubstTable(request.user.chemistry.react_subst_all(id_reaction))
    RequestConfig(request, paginate={"per_page": 25}).configure(rst)
    context = {'id_reaction': id_reaction, 'form': form, 'substance': rst}
    return render(request, 'chemical/react_substance_new.html', context)


@login_required
def react_substance_detail(request, id_reaction, id_react_substance):
    subst_dict = request.user.chemistry.react_subst_get(id_reaction, id_react_substance)
    context = {'id_reaction': id_reaction, "substance": subst_dict['substance'], "is_owner": subst_dict['is_owner']}
    return render(request, 'chemical/react_substance_detail.html', context)


@login_required
@owner_required
def react_substance_delete(request, id_reaction, id_react_substance):
    #тут нужно добавить обработчик ошибок...
    subst_dict = request.user.chemistry.react_subst_get(id_reaction, id_react_substance)
    subst_dict['substance'].delete()
    return redirect('react_substance_all', id_reaction)  # или лушче на сообщение - "?"


#Серии для Экспериментов
@login_required
@owner_required
def exper_serie_new(request, id_reaction):
    react = request.user.chemistry.reaction_get(id_reaction)

    form = ExperSerieForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            exper_serie = form.save(commit=False)
            exper_serie.reaction = react.reaction
            form.save()
            return redirect('exper_serie_detail', id_reaction, exper_serie.pk)

    context = {'id_reaction': id_reaction, 'form': form}
    return render(request, 'chemical/exper_serie_new.html', context)


@login_required
def exper_serie_detail(request, id_reaction, id_exper_serie):
    exper_serie_dict = request.user.chemistry.exper_serie_get(id_reaction, id_exper_serie)
    context = {'exper_serie': exper_serie_dict['exper_serie'],
        'id_reaction': id_reaction, "is_owner": exper_serie_dict['is_owner']}
    return render(request, 'chemical/exper_serie_detail.html', context)


# Эксперименты
@login_required
def experiment_all(request, id_reaction):
    exper_by_ser = []
    #сначала без серий
    sae = Series_and_Exper()
    exp_table = None
    expers = None

    series = request.user.chemistry.exper_serie_all(id_reaction)
    for s in series:
        expers = s.experiments.all()
        sae = Series_and_Exper()
        sae.serie = s
        link = reverse('chemical.views.exper_serie_detail', args=[id_reaction, s.pk])
        sae.serie_detail_link = make_detail_link(link)
        exp_table = ExperimentTable(expers)
        sae.exper_table = exp_table
        sae.exper_count = len(expers)
        exper_by_ser.append(sae)

    sae = Series_and_Exper()
    exp_table = None
    expers = request.user.chemistry.experiment_all_no_serie(id_reaction)
    if len(expers) > 0:
        exp_table = ExperimentTable(expers)
        sae.exper_table = exp_table
        sae.exper_count = len(expers)

    exper_by_ser.append(sae)

    context_dict = {'exper_by_series': exper_by_ser, 'id_reaction': id_reaction}
    return render(request, 'chemical/experiment_all.html', context_dict)


@login_required
def experiment_all_search(request, id_reaction, searched=""):
    if searched.strip() == '':
        return experiment_all(request, id_reaction)

    exp_table = ExperimentTable(request.user.chemistry.experiment_search(id_reaction, searched))
    RequestConfig(request, paginate={"per_page": 25}).configure(exp_table)
    context_dict = {'exper_table': exp_table, 'id_reaction': id_reaction, 'searched': searched}
    return render(request, 'chemical/experiment_search.html', context_dict)


@login_required
def experiment_detail(request, id_reaction, id_experiment):
    exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    context = {'experiment': exper_dict['experiment'], 'id_reaction': id_reaction, "is_owner": exper_dict['is_owner']}
    return render(request, 'chemical/experiment_detail.html', context)


@login_required
def experiment_edit(request, id_reaction, id_experiment):
    exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    # получаем список веществ реакции
    # reac_substs = request.user.chemistry.react_subst_all(id_reaction)
    # получаем список веществ эксперимента
    react_subst = request.user.chemistry.react_subst_all(id_reaction)
    exp_substs = request.user.chemistry.exper_subst_all(id_reaction, id_experiment)
    #print(type(exp_substs))

    # добавим сюда ссылку на точку эксперимента
    react_with_exper = []
    for react_s in react_subst:
        rswe = React_Substance_with_Exper()
        rswe.react_subst = react_s
        rswe.exper_subst = exp_substs.filter(reaction_subst=react_s)[0]
        react_with_exper.append(rswe)
        #print(rswe.react_subst)

    #for exp_s in exp_substs:  # все экспериментальные вещества
    #    react_with_exper[exp_s.reaction_subst.pk].exper_subst = exp_s

    #print(exper_dict['experiment'])
    #print(exper_dict['experiment'].arg_values.all())
    context = {'id_reaction': id_reaction, 'experiment': exper_dict['experiment'],
        "is_owner": exper_dict['is_owner'], 'react_with_exper': react_with_exper,
        'arg_vals': exper_dict['experiment'].arg_values.all()}
    return render(request, 'chemical/experiment_edit.html', context)


@login_required
@owner_required
def experiment_delete(request, id_reaction, id_experiment):
    #тут нужно добавить обработчик ошибок...
    exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    exper_dict['experiment'].delete()
    return redirect('experiment_all', id_reaction)  # или лушче на сообщение - "?"


@login_required
@owner_required
def experiment_copy(request, id_reaction, id_experiment):
    #empty now TODO
    return redirect('experiment_detail', id_reaction, id_experiment)


@login_required
@owner_required
def experiment_new(request, id_reaction, id_exper_serie=''):
    react = request.user.chemistry.reaction_get(id_reaction)
    if id_exper_serie == '':
        exper_serie = None
    else:
        exper_serie_dict = request.user.chemistry.exper_serie_get(id_reaction, id_exper_serie)
        exper_serie = exper_serie_dict['exper_serie']

    #print(exper_serie['exper_serie'])

    form = ExperimentForm(request.POST or None, initial={'exper_serie': exper_serie, 'name': 'Эксперимент №<введите номер>'})
    if request.method == 'POST':
        if form.is_valid():
            experiment = form.save(commit=False)
            experiment.reaction = react.reaction
            form.save()
            return redirect('experiment_detail', id_reaction, experiment.pk)

    context = {'id_reaction': id_reaction, 'form': form}
    return render(request, 'chemical/experiment_new.html', context)


#Задачи
@login_required
def problem_all(request, id_reaction):
    problem_table = ProblemTable(request.user.chemistry.problem_all(id_reaction))
    RequestConfig(request, paginate={"per_page": 25}).configure(problem_table)
    context = {'problems': problem_table, 'id_reaction': id_reaction}
    return render(request, 'chemical/problem_all.html', context)


@login_required
def problem_detail(request, id_reaction, id_problem):
    problem_dict = request.user.chemistry.problem_get(id_reaction, id_problem)
    context = {'problem': problem_dict['problem'], 'id_reaction': id_reaction, "is_owner": problem_dict['is_owner']}
    return render(request, 'chemical/problem_detail.html', context)


@login_required
@owner_required
def problem_new(request, id_reaction, id_problem_type):
    react = request.user.chemistry.reaction_get(id_reaction)
    problem_type = request.user.chemistry.dict_problem_type_get(id_problem_type)
    form = ProblemForm(request.POST or None, initial={'problem_type': problem_type})
    if request.method == 'POST':
        if form.is_valid():
            problem = form.save(commit=False)
            problem.reaction = react.reaction
            form.save()
            if problem.set_default_problem_props() != 1:
                raise Http404("Ошибка формирования параметров задачи по умолчанию")
            return redirect('problem_init', id_reaction, problem.pk)
    context = {'id_reaction': id_reaction, 'id_problem_type':id_problem_type, 'form': form}
    return render(request, 'chemical/problem_new.html', context)
    #context = {'id_reaction': id_reaction, 'id_problem_type': id_problem_type}
    #return render(request, 'chemical/problem_new.html', context)


@login_required
def problem_edit(request, id_reaction, id_problem):
    #пока без учета типа задачи переадресовывает на  init
    #но если понадобиться, то можно будет для разных типов задач редиректить на разные страницы
    return redirect('problem_init', id_reaction, id_problem)


@login_required
def problem_init(request, id_reaction, id_problem):
    problem_dict = request.user.chemistry.problem_get(id_reaction, id_problem)
    context = {}
    problem = problem_dict['problem']
    context['problem'] = problem
    context['id_reaction'] = id_reaction
    context["is_owner"] = problem_dict['is_owner']
    context['step_name'] = 'problem_init'
    problem_context = request.user.chemistry.get_problem_context(problem, 1)
    context['problem_context'] = problem_context
    return render(request, 'chemical/problem_init.html', context)


@login_required
def problem_calc_options(request, id_reaction, id_problem):
    problem_dict = request.user.chemistry.problem_get(id_reaction, id_problem)
    context = {}
    context['problem'] = problem_dict['problem']
    context['id_reaction'] = id_reaction
    context["is_owner"] = problem_dict['is_owner']
    context['step_name'] = 'problem_calc_options'
    return render(request, 'chemical/problem_calc_options.html', context)


@login_required
def problem_calc_state(request, id_reaction, id_problem):
    problem_dict = request.user.chemistry.problem_get(id_reaction, id_problem)
    context = {}
    context['problem'] = problem_dict['problem']
    context['id_reaction'] = id_reaction
    context["is_owner"] = problem_dict['is_owner']
    context['step_name'] = 'problem_calc_state'
    return render(request, 'chemical/problem_calc_state.html', context)


@login_required
def problem_results(request, id_reaction, id_problem):
    problem_dict = request.user.chemistry.problem_get(id_reaction, id_problem)
    context = {}
    context['problem'] = problem_dict['problem']
    context['id_reaction'] = id_reaction
    context["is_owner"] = problem_dict['is_owner']
    context['step_name'] = 'problem_results'
    return render(request, 'chemical/problem_results.html', context)


@login_required
@owner_required
def problem_delete(request, id_reaction, id_problem):
    #тут нужно добавить обработчик ошибок...
    problem_dict = request.user.chemistry.problem_get(id_reaction, id_problem)
    problem_dict['problem'].delete()
    return redirect('problem_all', id_reaction)  # или лушче на сообщение - "?"




#Решения
@login_required
def calc_all(request, id_reaction):
    #print('start add')
    #result = add.delay(4, 4)
    #print(result.ready())
    #print('add ready')
    #print(result.backend)
    #print('add ready')
    #print(result.ready())
    #print(result.backend)
    #print(result.as_tuple())

    #result = celery.AsyncResult(task_id)
    #print(add.name)
    #print('start add')
    #result = add.apply_async((2, 2))  #add.delay(7, 8)
    #print(result.id)
    #print(result.ready())

    print('tmp 2 2')
    a = add.delay(2,2)
    tmp = add.AsyncResult(a.task_id).get()
    print(a)
    print(tmp)
   # result = add.delay(4, 7)
   # [v for v in result.collect()
  #      if not isinstance(v, (ResultBase, tuple))]
    return render(request, 'chemical/calc_all.html', {"id_reaction": id_reaction})


#Статистика
@login_required
def statistic(request, id_reaction):
    return render(request, 'chemical/statistic.html', {"id_reaction": id_reaction})


#Журнал изменений
@login_required
def log(request, id_reaction):
    return render(request, 'chemical/log.html', {"id_reaction": id_reaction})



