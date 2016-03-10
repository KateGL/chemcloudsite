from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django_tables2   import RequestConfig

from chemical.models import Atom
from chemical.tables  import AtomTable

@login_required
def reactions_all(request):
    return render(request, 'chemical/reactions_all.html', {})

@login_required
def substance_dict(request):
    return render(request, 'chemical/substance_dict.html', {})

@login_required
def calculations_all(request):
    return render(request, 'chemical/calculations_all.html', {})

@login_required
def atoms_all(request):
    atom_table = AtomTable(Atom.objects.all())
    RequestConfig(request, paginate={"per_page": 5}).configure(atom_table)
    return render(request, 'chemical/atoms_all.html',  {"atom": atom_table})

@login_required
def dictionaries(request):
    return render(request, 'chemical/dictionaries.html', {})
