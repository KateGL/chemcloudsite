from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    return render(request, 'chemmain/index.html', {})

def about(request):
    return render(request, 'chemmain/about.html', {})

def help(request):
    return render(request, 'chemmain/help.html', {})

def faq(request):
    return render(request, 'chemmain/faq.html', {})

def contact(request):
    return render(request, 'chemmain/contact.html', {})

def prices(request):
    return render(request, 'chemmain/prices.html', {})

def news(request):
    return render(request, 'chemmain/news.html', {})

