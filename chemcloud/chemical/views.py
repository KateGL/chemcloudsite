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

@login_required
def reactions_all(request):
    return render(request, 'chemical/reactions_all.html', {})

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
def calculations_all(request):
    return render(request, 'chemical/calculations_all.html', {})

@login_required
def atoms_all(request):
    atom_table = AtomTable(Atom.objects.all())
    RequestConfig(request, paginate={"per_page": 5}).configure(atom_table)
    return render(request, 'chemical/atoms_all.html',  {"atom": atom_table})

@login_required
def atom_detail(request, atom_number):
    try:
        atom = Atom.objects.get(pk=atom_number)
    except Atom.DoesNotExist:
        raise Http404("Atom does not exist")
    return render(request, 'chemical/atom_detail.html', {"atom": atom})


@login_required
def dictionaries(request):
    return render(request, 'chemical/dictionaries.html', {})
