"""chemcloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings 
from django.conf.urls.static import static 

import chemmain.views
import chemical.views
from django.conf.urls import include

from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self,request):
        return '/'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', chemmain.views.index, name='index'),
    url(r'^about/$', chemmain.views.about, name='about'),
    url(r'^help/$', chemmain.views.help, name='help'),
    url(r'^faq/$', chemmain.views.faq, name='faq'),
    url(r'^contact/$', chemmain.views.contact, name='contact'),
    url(r'^prices/$', chemmain.views.prices, name='prices'),
    url(r'^news/$', chemmain.views.news, name='news'),

    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^reaction/all/$', chemical.views.reactions_all, name='reactions_all'),
    url(r'^substance_dict/$', chemical.views.substance_dict, name='substance_dict'),
    url(r'^calculation/all/$', chemical.views.calculations_all, name='calculations_all'),
  
]
