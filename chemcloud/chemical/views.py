# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django_tables2   import RequestConfig

from chemical.models import Atom, Substance
from chemical.tables  import AtomTable, SubstanceTable

# Вещество

@login_required
def substance_all(request):
    substance_table = SubstanceTable(Substance.objects.all())
    RequestConfig(request, paginate={"per_page": 5}).configure(substance_table)
    return render(request, 'chemical/substance_all.html',  {"substance": substance_table})


@login_required
def substance_detail(request, id_substance):
    try:
        substance = Substance.objects.get(pk=id_substance)
    except Substance.DoesNotExist:
        raise Http404("Substance does not exist")
    return render(request, 'chemical/substance_detail.html', {"substance": substance})

@login_required
def substance_new(request):
    return render(request, 'chemical/substance_new.html', {})


# расчеты

@login_required
def calculation_all(request):
    return render(request, 'chemical/calculation_all.html', {})

# атом
@login_required
def atoms_all(request):
    atom_table = AtomTable(Atom.objects.all())
    RequestConfig(request, paginate={"per_page": 5}).configure(atom_table)
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
    return render(request, 'chemical/reaction_all.html', {})

@login_required
def reaction_detail(request, id_reaction):
    try:
        react = Reaction.objects.get(pk=id_reaction)
    except Reaction.DoesNotExist:
        raise Http404("Reaction does not exist")
    return render(request, 'chemical/reaction_detail.html', {"reaction": react})

@login_required
def reaction_new(request):
    return render(request, 'chemical/reaction_new.html', {})


#  Механизмы реакции
#import the Reaction_scheme model
from chemical.models import Reaction_scheme
from .forms import ReacSchemeForm

@login_required
def scheme_all(request, reaction_id):
#получаем список всех схем реакций, 
#сортируем по идентификатору схемы.
#извлекаем первые пять записей
#помещаем список в словарь контекста, который будет передан механизму шаблонов	
	scheme_list = Reaction_scheme.objects.filter(fid_reac=int(reaction_id)).order_by('fid_scheme')[:5]
	context_dict = {'schemes': scheme_list}

#формируем ответ для клиента по шаблону и отправляем обратно
	return render(request, 'chemical/scheme_all.html', context_dict )

@login_required
def scheme_detail(request, reaction_id, scheme_id):
	scheme_details = Reaction_scheme.objects.filter(fid_scheme=int(scheme_id))
	context = {'scheme_detail': scheme_detail}

	return render(request, 'chemical/scheme_detail.html', context )

@login_required
def scheme_edit(request, id_scheme):
    try:
        scheme = Reaction_scheme.objects.get(pk=id_scheme)
    except Reaction_scheme.DoesNotExist:
        raise Http404("Reaction_scheme does not exist")
    return render(request, 'chemical/scheme_edit.html', {"scheme": scheme})

#      c = RequestContext(request.POST, {})
@login_required
def scheme_new(request, reaction_id):
	if request.method == "POST":
 		form = ReacSchemeForm(request.POST)
		if form.is_valid():
			scheme = form.save(commit=False)
			scheme.fid_reac = reaction_id			
			scheme.fname = form.cleaned_data['fname']
			scheme.fdescription = form.cleaned_data['fdescription']
			scheme.fis_possible = form.cleaned_data['fis_possible']
		#   scheme.fcreated_date = timezone.now
		#	scheme.fupdated_date = timezone.now
			scheme.fupdated_by = request.user
			scheme.fcreated_by = request.user
			scheme.save()
			#return HttpResponseRedirect("/")	
			return redirect('chemical.views.scheme_detail', reaction_id, scheme.pk)
	else:
		form = ReacSchemeForm()
	return render(request, 'chemical/scheme_new.html', {'form': form })
	#return render_to_response('chemkinoptima/scheme_new.html', {'form': form }, context_instance = RequestContext(request ) ) #{'form': form }, context_instance =


# Эксперименты
@login_required
def experiment_all(request, id_reaction):
	return render(request, 'chemical/experiment_all.html', [] )

@login_required
def experiment_detail(request, id_experiment):
   # try:
    #    atom = Atom.objects.get(pk=atom_number)
   # except Atom.DoesNotExist:
    #    raise Http404("Atom does not exist")
    return render(request, 'chemical/experiment_detail.html', [])

@login_required
def experiment_new(request, id_reaction):
	return render(request, 'chemical/experiment_new.html', [])

@login_required
def experiment_edit(request, id_experiment):
   # try:
    #    atom = Atom.objects.get(pk=atom_number)
   # except Atom.DoesNotExist:
    #    raise Http404("Atom does not exist")
    return render(request, 'chemical/experiment_edit.html', [])


