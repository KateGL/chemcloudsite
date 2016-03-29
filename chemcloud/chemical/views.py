# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, Http404


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django_tables2 import RequestConfig


from chemical.models import Atom, Substance, Experiment, SubstanceConsist
from chemical.tables import AtomTable, SubstanceTable, ReactionTable
from chemical.tables import ConsistTable, MechanizmTable, ReactionSubstTable, ExperimentTable
from chemical.tables import StepsTable


from django.shortcuts import redirect
from chemical.forms import SubstanceForm, ReactionForm, ReactionSubstForm
#import the Reaction_scheme model
from chemical.models import Reaction
from chemical.models import Reaction_scheme
from .forms import ReacSchemeForm,ExperimentForm

from .utils import decorate_formula

# Вещество

@login_required
def substance_all(request):
    substance_table = SubstanceTable(Substance.objects.all())
    RequestConfig(request, paginate={"per_page": 25}).configure(substance_table)
    return render(request, 'chemical/substance_all.html', {"substance": substance_table})


@login_required
def substance_detail(request, id_substance):
    try:
      substance = Substance.objects.get(pk=id_substance)
      consist_table = ConsistTable(substance.consist.all())
    except Substance.DoesNotExist:
      raise Http404("Substance does not exist")
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
            return redirect('substance_detail', substance.pk)
    return render(request,'chemical/substance_new.html', {'form': form})

# расчеты

@login_required
def calculation_all(request):
    return render(request, 'chemical/calculation_all.html', {})

# атом
@login_required
def atoms_all(request):
    atom_table = AtomTable(Atom.objects.all())
    RequestConfig(request, paginate={"per_page": 30}).configure(atom_table)
    return render(request, 'chemical/atom_all.html',  {"atom": atom_table})

@login_required
def atom_detail(request, atom_number):
    try:
        atom = Atom.objects.get(pk=atom_number)
    except Atom.DoesNotExist:
      raise Http404("Atom does not exist")
    return render(request, 'chemical/atom_detail.html', {"atom": atom})

# Справочники
@login_required
def dictionaries(request):
    return render(request, 'chemical/dictionaries.html', {})


# Реакции

@login_required
def reaction_all(request):
    reaction_table = ReactionTable(request.user.reactions.all())
    RequestConfig(request, paginate={"per_page": 15}).configure(reaction_table)
    return render(request, 'chemical/reaction_all.html', {"reaction": reaction_table})

@login_required
def reaction_detail(request, id_reaction):
    try:
        react = Reaction.objects.get(pk=id_reaction)
    except Reaction.DoesNotExist:
        raise Http404("Reaction does not exist")
    return render(request, 'chemical/reaction_detail.html',
         {"reaction": react, "id_reaction": id_reaction})

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
def scheme_all(request, reaction_id):
	try:
		#получаем объект реакции по reaction_id
		reac_temp = Reaction.objects.get(pk=reaction_id)
	except Reaction.DoesNotExist:
		raise Http404("Reaction does not exist")	
	#получаем список всех схем реакции
	#сортируем по идентификатору схемы.
	#для извлечения первых пяти записей - [:5]
	#scheme_list = Reaction_scheme.objects.filter(reaction = reac_temp).order_by('id_scheme')
	#scheme_list = reac_temp.reaction_scheme_set.all()
	scheme_list = reac_temp.schemes.all()

	#формируем таблицу на основе полученного списка механизмов
	mech_table = MechanizmTable(scheme_list)
	
	#помещаем таблицу со списком механизмов, а также reaction_id в словарь контекста, который будет передан шаблону	
	context_dict = {'schemes': mech_table, 'id_reaction' : reaction_id}
	#формируем ответ для клиента по шаблону и отправляем обратно
	return render(request, 'chemical/scheme_all.html', context_dict)


@login_required
def scheme_detail(request, scheme_id):
	#try:
	#	#получаем объект реакции по reaction_id
	#	reac_temp = Reaction.objects.get(pk=reaction_id)
	#except Reaction.DoesNotExist:
	#	raise Http404("Reaction does not exist")		
	#получаем объект схемы по scheme_id	
	scheme_tmp = Reaction_scheme.objects.get(pk=scheme_id)
	reac_id = scheme_tmp.reaction.id_reaction
	context = {'scheme': scheme_tmp, 'id_reaction' : reac_id}
	return render(request, 'chemical/scheme_detail.html', context )

@login_required
def scheme_edit(request, reaction_id, scheme_id):
	try:
		#получаем объект реакции по reaction_id
		reac_temp = Reaction.objects.get(pk=reaction_id)
	except Reaction.DoesNotExist:
		raise Http404("Reaction does not exist")
	try:
		#получаем объект схемы по scheme_id		
		scheme = Reaction_scheme.objects.get(pk=scheme_id)
	except Reaction_scheme.DoesNotExist:
		raise Http404("Reaction scheme does not exist")
	reac_id = scheme.reaction.id_reaction	
	#получаем список стадий схемы		
	steps   = scheme.steps.all()
	steps_table = StepsTable(steps)
	context = {'steps': steps_table, 'id_reaction': reac_id, 'scheme_name': scheme.name}	
	return render(request, 'chemical/scheme_edit.html', context)

@login_required
def step_detail(request, reaction_id, scheme_id, step_id):
	try:
		#получаем объект реакции по reaction_id
		reac_temp = Reaction.objects.get(pk=reaction_id)
	except Reaction.DoesNotExist:
		raise Http404("Reaction does not exist")		
	#получаем объект схемы по scheme_id	
	scheme_tmp = Reaction_scheme.objects.get(pk=scheme_id)
	context = {'scheme': scheme_tmp, 'id_reaction' : reaction_id}
	return render(request, 'chemical/step_detail.html', context )

#      c = RequestContext(request.POST, {})
@login_required
def scheme_new(request, reaction_id):
	if request.method == "POST":
 		form = ReacSchemeForm(request.POST)
		if form.is_valid():
			try:
				reaction = Reaction.objects.get(pk=reaction_id)
			except Reaction.DoesNotExist:
				raise Http404("Reaction does not exist")			
			scheme = form.save(commit=False)			
			scheme.reaction = reaction		
			scheme.name = form.cleaned_data['name']
			scheme.description = form.cleaned_data['description']
			scheme.is_possible = form.cleaned_data['is_possible']
		#  scheme.fcreated_date = timezone.now
		#	scheme.fupdated_date = timezone.now
			scheme.updated_by = request.user
			scheme.created_by = request.user
			scheme.save()
			#return HttpResponseRedirect("/")	
			return redirect('chemical.views.scheme_detail', reaction_id, scheme.pk)
	else:
		form = ReacSchemeForm()
	context_dict = {'form': form, 'id_reaction' : reaction_id}
	return render(request, 'chemical/scheme_new.html', context_dict)
	#return render_to_response('chemkinoptima/scheme_new.html', {'form': form }, context_instance = RequestContext(request ) ) #{'form': form }, context_instance =


#Вещества реакции
@login_required
def react_substance_all(request, id_reaction):
    try:
        react = Reaction.objects.get(pk=id_reaction)
    except Reaction.DoesNotExist:
        raise Http404("Reaction does not exist")

    reaction_subst_table = ReactionSubstTable(react.substances.all())
    RequestConfig(request, paginate={"per_page": 25}).configure(reaction_subst_table)
    context_dict = {'substance': reaction_subst_table, 'id_reaction': id_reaction}
    return render(request, 'chemical/react_substance_all.html', context_dict)


@login_required
def react_substance_new(request, id_reaction):
    try:
        react = Reaction.objects.get(pk=id_reaction)
    except Reaction.DoesNotExist:
        raise Http404("Reaction does not exist")

    form = ReactionSubstForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            react_substance = form.save(commit=False)
            react_substance.reaction = react
            form.save()
            return redirect('react_substance_detail', id_reaction, react_substance.pk)

    context = {'id_reaction': id_reaction, 'form': form}
    return render(request, 'chemical/react_substance_new.html', context)


@login_required
def react_substance_detail(request, id_reaction, id_react_substance):
    try:
        react = Reaction.objects.get(pk=id_reaction)
    except Reaction.DoesNotExist:
        raise Http404("Reaction does not exist")

    try:
        substance = react.substances.get(pk=id_react_substance)
    except Substance.DoesNotExist:
        raise Http404("Substance does not exist")

    context = {'id_reaction': id_reaction, "substance": substance}
    return render(request, 'chemical/react_substance_detail.html', context)

# Эксперименты
@login_required
def experiment_all(request, reaction_id):
   #получаем список всех экспериментов,
	#сортируем по идентификатору схемы.
	#для извлечения первых пяти записей - [:5]
	#помещаем список в словарь контекста, который будет передан механизму шаблонов	
   try:
      reac_temp = Reaction.objects.get(pk=reaction_id)
   except Reaction.DoesNotExist:
      raise Http404("Reaction does not exist")
   experiment_list = reac_temp.experiments.all()
   #формируем таблицу на основе полученного списка механизмов
   exp_table = ExperimentTable(experiment_list)
   #помещаем таблицу со списком механизмов, а также reaction_id в словарь контекста, который будет передан шаблону
   context_dict = {'experiments': exp_table, 'id_reaction' : reaction_id}

   #формируем ответ для клиента по шаблону и отправляем обратно
   return render(request, 'chemical/experiment_all.html', context_dict )



@login_required
def experiment_detail(request, experiment_id):
    experiment_tmp = Experiment.objects.get(pk=experiment_id)
    reac_id = experiment_tmp.reaction.id_reaction
    context = {'experiment': experiment_tmp, 'id_reaction' : reac_id}
    return render(request, 'chemical/experiment_detail.html', context )

@login_required
def experiment_edit(request, reaction_id, scheme_id):
	try:
		#получаем объект реакции по reaction_id
		reac_temp = Reaction.objects.get(pk=reaction_id)
	except Reaction.DoesNotExist:
		raise Http404("Reaction does not exist")
	try:
		#получаем объект схемы по scheme_id		
		experiment = Experiment.objects.get(pk=experiment_id)
	except Experiment.DoesNotExist:
		raise Http404("Reaction scheme does not exist")
	reac_id = experiment.reaction.id_reaction	
	context = {'id_reaction': reac_id, 'experiment_name': experiment.name}	
	return render(request, 'chemical/experiment_all.html', context)


@login_required
def experiment_new(request, reaction_id):
	if request.method == "POST":
 		form = ExperimentForm(request.POST)
		if form.is_valid():
			try:
				reaction = Reaction.objects.get(pk=reaction_id)
			except Reaction.DoesNotExist:
				raise Http404("Reaction does not exist")			
			experiment = form.save(commit=False)			
			experiment.reaction = reaction		
			experiment.name = form.cleaned_data['name']
			experiment.description = form.cleaned_data['description']
			experiment.is_favorite = form.cleaned_data['is_favorite']		
			experiment.updated_by = request.user
			experiment.created_by = request.user
			experiment.save()
			
			return redirect('experiment_detail', reaction_id, experiment.pk)
		context_dict = {'form': form, 'id_reaction' : reaction_id}
		return render(request,'chemical/experiment_new.html', context_dict)

			#return redirect('chemical/experiment_all.html', reaction_id, experiment.pk)
	else:
		form = ExperimentForm()
	context_dict = {'form': form, 'id_reaction' : reaction_id}
	return render(request, 'chemical/experiment_new.html', context_dict)


@login_required
def experiment_edit(request, reaction_id, id_experiment):
   # try:
    #    atom = Atom.objects.get(pk=atom_number)
   # except Atom.DoesNotExist:
    #    raise Http404("Atom does not exist")
    return render(request, 'chemical/experiment_edit.html', {"id_reaction": reaction_id})


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



