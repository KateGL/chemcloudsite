# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, Http404


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django_tables2 import RequestConfig

from chemical.models import Atom, Substance, SubstanceConsist
from chemical.tables import AtomTable, SubstanceTable, ReactionTable

from django.shortcuts import redirect
from chemical.forms import SubstanceForm, ReactionForm
#import the Reaction_scheme model
from chemical.models import Reaction
from chemical.models import Reaction_scheme
from .forms import ReacSchemeForm


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
      #a = SubstanceConsist.objects.get_or_create(atom =Atom.objects.get(pk=1), substance = substance, atom_count = 3)[0]
      #a.save()
      #substance.consist.add(a)
      #cnt = substance.consist.count;
    except Substance.DoesNotExist:
      raise Http404("Substance does not exist")
    return render(request, 'chemical/substance_detail.html', {"substance": substance})

@login_required
def substance_new(request):
    form = SubstanceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            substance = form.save()
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
def scheme_all(request, reaction_id):
	#получаем список всех схем реакций,
	#сортируем по идентификатору схемы.
	#для извлечения первых пяти записей - [:5]
	#помещаем список в словарь контекста, который будет передан механизму шаблонов	
	try:
		reac_temp = Reaction.objects.get(pk=reaction_id)
	except Reaction.DoesNotExist:
		raise Http404("Reaction does not exist")	
	scheme_list = Reaction_scheme.objects.filter(reaction = reac_temp).order_by('id_scheme')
	context_dict = {'schemes': scheme_list, 'id_reaction' : reaction_id}
	#формируем ответ для клиента по шаблону и отправляем обратно
	return render(request, 'chemical/scheme_all.html', context_dict )

@login_required
def scheme_detail(request, scheme_id):
	scheme_detail = Reaction_scheme.objects.get(pk=scheme_id)
	context = {'scheme': scheme_detail}
	return render(request, 'chemical/scheme_detail.html', context )

@login_required
def scheme_edit(request, scheme_id):
    try:
        scheme = Reaction_scheme.objects.get(pk=scheme_id)
    except Reaction_scheme.DoesNotExist:
        raise Http404("Reaction_scheme does not exist")
    return render(request, 'chemical/scheme_edit.html', {"scheme": scheme})

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
			return redirect('chemical.views.scheme_detail', scheme.pk)
	else:
		form = ReacSchemeForm()
	return render(request, 'chemical/scheme_new.html', {'form': form })
	#return render_to_response('chemkinoptima/scheme_new.html', {'form': form }, context_instance = RequestContext(request ) ) #{'form': form }, context_instance =


#Вещества реакции
@login_required
def react_substance_all(request, id_reaction):
    return render(request, 'chemical/react_substance_all.html', {"id_reaction": id_reaction})



# Эксперименты
@login_required
def experiment_all(request, id_reaction):
	return render(request, 'chemical/experiment_all.html', {"id_reaction": id_reaction} )

@login_required
def experiment_detail(request, id_experiment):
   # try:
    #    atom = Atom.objects.get(pk=atom_number)
   # except Atom.DoesNotExist:
    #    raise Http404("Atom does not exist")
    return render(request, 'chemical/experiment_detail.html', {"id_reaction": id_reaction})

@login_required
def experiment_new(request, id_reaction):
    return render(request, 'chemical/experiment_new.html', {"id_reaction": id_reaction})

@login_required
def experiment_edit(request, id_experiment):
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



