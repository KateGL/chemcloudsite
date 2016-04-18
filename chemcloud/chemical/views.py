# -*- coding: utf-8 -*-
import logging

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from chemical.tables import AtomTable, SubstanceTable, ReactionTable
from chemical.tables import ConsistTable, MechanizmTable, ReactionSubstTable, ExperimentTable
from chemical.tables import StepsTable, UserOfReactionTable


from django.shortcuts import redirect
from chemical.forms import SubstanceForm, ReactionForm, ReactionSubstForm, ReactionShareForm
from .forms import ReacSchemeForm, ExperimentForm

from .utils import decorate_formula

from .models import owner_required

# Вещество

@login_required
def substance_all(request):
    substance_table = SubstanceTable(request.user.chemistry.substance_all())
    RequestConfig(request, paginate={"per_page": 25}).configure(substance_table)
    return render(request, 'chemical/substance_all.html', {"substance": substance_table})

@login_required
def substance_search(request, searched):
    tmp = searched+ ' Hello, World!'
    return HttpResponse(tmp)


@login_required
def substance_search_hint(request, searched):
    subst = request.user.chemistry.substance_get_like(searched, 3)
    tmp = ''
    for value in subst.values():
        if tmp > '':
            tmp = tmp + ', '
        tmp = tmp + value['name']


    #tmp = searched + ' ' + str(subst)
    return HttpResponse(tmp)


@login_required
def substance_detail(request, id_substance):
    substance = request.user.chemistry.substance_get(id_substance)
    consist_table = ConsistTable(substance.consist.all())
    return render(request, 'chemical/substance_detail.html',
    {"substance": substance,"substance_consist":consist_table})

@login_required
def substance_new(request):
    form = SubstanceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            substance = form.save()
            substance.formula_brutto_formatted = decorate_formula(substance.formula_brutto)
            substance.consist_create()
            form.save()
            if 'save_and_new_btn' in request.POST:
                return redirect('substance_new')
            return redirect('substance_detail', substance.pk)
    return render(request,'chemical/substance_new.html', {'form': form})



# расчеты

@login_required
def calculation_all(request):
    return render(request, 'chemical/calculation_all.html', {})

# атом
@login_required
def atoms_all(request):
    atom_table = AtomTable(request.user.chemistry.atom_all())
    RequestConfig(request, paginate={"per_page": 30}).configure(atom_table)
    return render(request, 'chemical/atom_all.html',  {"atom": atom_table})

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
def reaction_all(request):
    reaction_table = ReactionTable(request.user.chemistry.reaction_all())
    RequestConfig(request, paginate={"per_page": 15}).configure(reaction_table)
    return render(request, 'chemical/reaction_all.html', {"reaction": reaction_table})

@login_required
def reaction_detail(request, id_reaction):
    react = request.user.chemistry.reaction_get(id_reaction)
    user_reacts = UserOfReactionTable(react.reaction.users.all())
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
              'form': form, 'user_reacts': user_reacts})


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
    return redirect('reaction_all')#или лушче на сообщение - "Реакция удалена?"


@login_required
def reaction_new(request):
    form = ReactionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            reaction = form.save()
            reaction.add_owner(request.user)
            form.save()
            return redirect('reaction_detail', reaction.pk)
    return render(request,'chemical/reaction_new.html', {'form': form})


#  Механизмы реакции
@login_required
def scheme_all(request, id_reaction):
    mech_table = MechanizmTable(request.user.chemistry.react_scheme_all(id_reaction))
    context_dict = {'schemes': mech_table, 'id_reaction' : id_reaction}
    return render(request, 'chemical/scheme_all.html', context_dict)

@login_required
def scheme_detail(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    context = {'scheme': scheme_dict['scheme'], 'id_reaction' : id_reaction, 'is_owner': scheme_dict['is_owner']}
    return render(request, 'chemical/scheme_detail.html', context )

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
    reac_substs = request.user.chemistry.react_subst_all(id_reaction)
    context = {'steps': steps, 'id_reaction': id_reaction, 'scheme_name': scheme_dict['scheme'].name, 'is_owner': scheme_dict['is_owner'], 'reac_substs': reac_substs, 'id_scheme': id_scheme }
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
def get_cell_value(request): #взятие старого значения ячейки
    if not request.is_ajax():
        return HttpResponse(status=400)
    table_str = ''
    id_str = ''
    field_str = ''
    if request.method != 'POST':
        return HttpResponse(status=400)
    table_str = request.POST['table']
    id_str    = request.POST['id']
    field_str = request.POST['field']
    #взятие значения ячейки из базы
    arr = table_str.split('_');
    #таблица стадий механизма
    pos = arr[0].find('all-steps');
    if pos != -1:
        id_reaction = int(arr[1])
        id_scheme   = int(arr[2])
        step_id = int(id_str)
        step_dict = request.user.chemistry.rscheme_step_get(id_reaction, id_scheme, int(step_id))
        step = step_dict['step']
        value = ''
        if field_str == 'name':
            value = step.name
        if field_str == 'step':
            value = 'kuku'
        data = '{"value": "' +value + '"}'
        xml_bytes = json.dumps(data)
        return HttpResponse(xml_bytes,'application/json')

    #сюда для других таблиц вставлять свои проверки названия таблицы и соответствующие обработчики
    return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def _create_step_part(step, is_left, part ):
    log = logging.getLogger('django') 
    log.info('а это будет')
    return 1   

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
    table_str = request.POST['table']
    id_str    = request.POST['id']
    field_str = request.POST['field']
    value_str = request.POST['value']

    #обработка редактирования стадий
    arr = table_str.split('_');
    #таблица стадий механизма
    pos = arr[0].find('all-steps');
    if pos != -1:
        id_reaction = int(arr[1])
        id_scheme   = int(arr[2])
        step_id = int(id_str)
        step_dict = request.user.chemistry.rscheme_step_get(id_reaction, id_scheme, int(step_id))
        step = step_dict['step']
        result = 'success'
        errorText = ''
        if field_str == 'name':
            step.name = value_str
        if field_str == 'step':
            step_str = value_str
            left_str = ''
            right_str = ''
            pos=step_str.find('->');
            if pos != -1:
                step.is_revers = False
                arr2 = table_str.split('->');
            else:
                pos = step_str.find('<->');
                if pos != -1:
                    step.is_revers = True
                    arr2 = table_str.split('<->');
                else:     
                    result = 'error'           
                    errorText = 'Неправильно введен флаг обратимости стадии'
            if pos != -1:
                left_str = arr2[0]
                right_str = arr2[1]
                _create_step_part(step, True, left_str)
        if result == 'success':
            step.save()
        data = '{"result":"' + result  +'", "errorText": "' + errorText + '"}'
        xml_bytes = json.dumps(data)
        return HttpResponse(xml_bytes,'application/json')

    #сюда для других таблиц вставлять свои проверки названия таблицы и соответствующие обработчики
    return HttpResponse(
            json.dumps('{"result": "error", "errorText": "unknown error"}'),
            content_type="application/json"
        )



@login_required
def step_delete(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    step_id = ''
    if request.method == 'GET':
        step_id = request.GET['step_id']
    if step_id:
        step_dict = request.user.chemistry.rscheme_step_get(id_reaction, id_scheme, int(step_id))
        step = step_dict['step']
        step.delete()
        #todo спросить
        data = '{"result":"success"}'
        xml_bytes = json.dumps(data)
        return HttpResponse(xml_bytes,'application/json')



@login_required
def step_new(request, id_reaction, id_scheme):
    scheme_dict = request.user.chemistry.react_scheme_get(id_reaction, id_scheme)
    scheme = scheme_dict['scheme'];
    new_step = scheme.create_new_emptystep();
    if new_step == -1:
        return HttpResponse(status=400)
    data = '{"id_step":"' + str(new_step.id_step) +'", "order":"'+str(new_step.order) + '", "name": "'+new_step.name+'"}'
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
    if request.method == 'GET':
        step_id = request.GET['step_id']
    direction = None
    if request.method == 'GET':
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
    return redirect('react_substance_all', id_reaction)#или лушче на сообщение - "?"

# Эксперименты
@login_required
def experiment_all(request, id_reaction):
    exp_table = ExperimentTable(request.user.chemistry.experiment_all(id_reaction))
    RequestConfig(request, paginate={"per_page": 25}).configure(exp_table)
    context_dict = {'experiments': exp_table, 'id_reaction' : id_reaction}
    return render(request, 'chemical/experiment_all.html', context_dict )


@login_required
def experiment_detail(request, id_reaction, id_experiment):
    exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    context = {'experiment': exper_dict['experiment'], 'id_reaction': id_reaction, "is_owner": exper_dict['is_owner']}
    return render(request, 'chemical/experiment_detail.html', context )

@login_required
def experiment_edit(request, id_reaction, id_experiment):
    exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    context = {'id_reaction': id_reaction, 'experiment': exper_dict['experiment'], "is_owner": exper_dict['is_owner']}
    return render(request, 'chemical/experiment_edit.html', context)


@login_required
@owner_required
def experiment_delete(request, id_reaction, id_experiment):
    #тут нужно добавить обработчик ошибок...
    exper_dict = request.user.chemistry.experiment_get(id_reaction, id_experiment)
    exper_dict['experiment'].delete()
    return redirect('experiment_all', id_reaction)#или лушче на сообщение - "?"


@login_required
@owner_required
def experiment_copy(request, id_reaction, id_experiment):
    #empty now TODO
    return redirect('experiment_detail', id_reaction, id_experiment)



@login_required
@owner_required
def experiment_new(request, id_reaction):
    react = request.user.chemistry.reaction_get(id_reaction)

    form = ExperimentForm(request.POST or None)
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
    return render(request, 'chemical/problem_all.html', {"id_reaction": id_reaction})

#Решения
@login_required
def calc_all(request, id_reaction):
    return render(request, 'chemical/calc_all.html', {"id_reaction": id_reaction})


#Статистика
@login_required
def statistic(request, id_reaction):
    return render(request, 'chemical/statistic.html', {"id_reaction": id_reaction})



#Журнал изменений
@login_required
def log(request, id_reaction):
    return render(request, 'chemical/log.html', {"id_reaction": id_reaction})



