# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, Http404


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django_tables2 import RequestConfig

from chemical.models import Atom, Substance, SubstanceConsist, Experiment
from chemical.tables import AtomTable, SubstanceTable, ReactionTable,ConsistTable, MechanizmTable,ExperimentTable
from chemical.tables import StepsTable

from django.shortcuts import redirect
from chemical.forms import SubstanceForm, ReactionForm
#import the Reaction_scheme model
from chemical.models import Reaction
from chemical.models import Reaction_scheme, Scheme_step
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
    reaction_table = ReactionTable(Reaction.objects.all())
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
            form.save()
            return redirect('reaction_detail', reaction.pk)
    return render(request,'chemical/reaction_new.html', {'form': form})



#  Механизмы реакции


@login_required
def scheme_all(request, id_reaction):
	try:
		#получаем объект реакции по id_reaction
		reac_temp = Reaction.objects.get(pk=id_reaction)
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
	
	#помещаем таблицу со списком механизмов, а также id_reaction в словарь контекста, который будет передан шаблону	
	context_dict = {'schemes': mech_table, 'id_reaction' : id_reaction}
	#формируем ответ для клиента по шаблону и отправляем обратно
	return render(request, 'chemical/scheme_all.html', context_dict )



@login_required
def scheme_detail(request, id_reaction, id_scheme):
	#try:
	#	#получаем объект реакции по id_reaction
	#	reac_temp = Reaction.objects.get(pk=id_reaction)
	#except Reaction.DoesNotExist:
	#	raise Http404("Reaction does not exist")		
	#получаем объект схемы по id_scheme	
	scheme_tmp = Reaction_scheme.objects.get(pk=id_scheme)
	reac_id = scheme_tmp.reaction.id_reaction
	context = {'scheme': scheme_tmp, 'id_reaction' : reac_id}
	return render(request, 'chemical/scheme_detail.html', context )

@login_required
def scheme_edit(request, id_reaction, id_scheme):
	try:
		#получаем объект реакции по id_reaction
		reac_temp = Reaction.objects.get(pk=id_reaction)
	except Reaction.DoesNotExist:
		raise Http404("Reaction does not exist")
	try:
		#получаем объект схемы по id_scheme		
		scheme = Reaction_scheme.objects.get(pk=id_scheme)
	except Reaction_scheme.DoesNotExist:
		raise Http404("Reaction scheme does not exist")
	reac_id = scheme.reaction.id_reaction	
	#получаем список стадий схемы	
	
	steps   = scheme.steps.all()
	#steps_table = StepsTable(steps)
	context = {'steps': steps, 'id_reaction': reac_id, 'scheme_name': scheme.name}	
	return render(request, 'chemical/scheme_edit.html', context)

@login_required
def step_detail(request, id_reaction, id_scheme, step_id):
	try:
		#получаем объект реакции по id_reaction
		reac_temp = Reaction.objects.get(pk=id_reaction)
	except Reaction.DoesNotExist:
		raise Http404("Reaction does not exist")		
	#получаем объект схемы по id_scheme	
	scheme_tmp = Reaction_scheme.objects.get(pk=id_scheme)
	context = {'scheme': scheme_tmp, 'id_reaction' : id_reaction}
	return render(request, 'chemical/step_detail.html', context )

#      c = RequestContext(request.POST, {})
@login_required
def scheme_new(request, id_reaction):
	if request.method == "POST":
 		form = ReacSchemeForm(request.POST)
		if form.is_valid():
			try:
				reaction = Reaction.objects.get(pk=id_reaction)
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
			return redirect('chemical.views.scheme_detail', id_reaction, scheme.pk)
	else:
		form = ReacSchemeForm()
	context_dict = {'form': form, 'id_reaction' : id_reaction}
	return render(request, 'chemical/scheme_new.html', context_dict)
	#return render_to_response('chemkinoptima/scheme_new.html', {'form': form }, context_instance = RequestContext(request ) ) #{'form': form }, context_instance =


#изменение порядка стадии
@login_required
def change_step_order(request, id_reaction, id_scheme):
	try:
		#получаем объект схемы по id_scheme		
		scheme = Reaction_scheme.objects.get(pk=id_scheme)
	except Reaction_scheme.DoesNotExist:
		raise Http404("Reaction scheme does not exist")
	steps_count = scheme.steps.count()

	step_id = None
	if request.method == 'GET':
		step_id = request.GET['step_id']
	current_order = None
	if request.method == 'GET':
		current_order = request.GET['cur_order']
	direction = None
	if request.method == 'GET':
		direction = request.GET['direction']

	#todo проверки на соответствие шага схемы схеме и реакции
	new_order = -1
	cur_order = int(current_order)
	if step_id:
		step = Scheme_step.objects.get(pk=int(step_id))
		if step:
			if direction == 'up' and cur_order>1:            
				new_order = cur_order - 1
				step_up = Scheme_step.objects.get(order=new_order)				
				step.order = new_order
				step_up.order = cur_order
				step.save()
				step_up.save()
			if direction == 'down' and cur_order<steps_count:            
				new_order = cur_order + 1
				step_down = Scheme_step.objects.get(order=new_order)				
				step.order = new_order
				step_down.order = cur_order
				step.order = new_order
				step.save()	
				step_down.save()
	#получаем список стадий схемы		
	steps   = scheme.steps.all()
	#steps_table = StepsTable(steps)
	context = {'steps': steps, 'id_reaction': id_reaction, 'scheme_name': scheme.name}	
	return render(request, 'chemical/scheme_edit.html', context)



#Вещества реакции
@login_required
def react_substance_all(request, id_reaction):
    return render(request, 'chemical/react_substance_all.html', {"id_reaction": id_reaction})

# Эксперименты
@login_required
def experiment_all(request, id_reaction):
   #получаем список всех экспериментов,
	#сортируем по идентификатору схемы.
	#для извлечения первых пяти записей - [:5]
	#помещаем список в словарь контекста, который будет передан механизму шаблонов	
   try:
      reac_temp = Reaction.objects.get(pk=id_reaction)
   except Reaction.DoesNotExist:
      raise Http404("Reaction does not exist")
   experiment_list = reac_temp.experiments.all()
   #формируем таблицу на основе полученного списка механизмов
   exp_table = ExperimentTable(experiment_list)
   #помещаем таблицу со списком механизмов, а также id_reaction в словарь контекста, который будет передан шаблону
   context_dict = {'experiments': exp_table, 'id_reaction' : id_reaction}

   #формируем ответ для клиента по шаблону и отправляем обратно
   return render(request, 'chemical/experiment_all.html', context_dict )



@login_required
#def experiment_detail(request, id_reaction, id_experiment):
def experiment_detail(request, id_reaction, experiment_id):
    experiment_detail = Experiment.objects.get(pk=experiment_id)
    context = {'experiment': experiment_detail, 'id_reaction' : id_reaction}
    return render(request, 'chemical/experiment_detail.html', context)

@login_required
def experiment_new(request, id_reaction):
    if request.method == "POST":
        form = ExperimentForm(request.POST)
        if form.is_valid():
            try:
                reaction = Reaction.objects.get(pk=id_reaction)
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

        return redirect('chemical.views.experiment_detail', id_reaction, experiment.pk)
    else:
        form = ExperimentForm()
        context_dict = {'form': form, 'id_reaction' : id_reaction}
        return render(request, 'chemical/experiment_new.html', context_dict)

@login_required
def experiment_edit(request, id_reaction, id_experiment):
   # try:
    #    atom = Atom.objects.get(pk=atom_number)
   # except Atom.DoesNotExist:
    #    raise Http404("Atom does not exist")
    return render(request, 'chemical/experiment_edit.html', {"id_reaction": id_reaction})


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



