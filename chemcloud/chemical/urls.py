from django.conf.urls import patterns, url
import chemical.views


urlpatterns = [
    
    url(r'^reaction/all/$', chemical.views.reactions_all, name='reactions_all'),
    
    url(r'^substance/all/$', chemical.views.substance_all, name='substance_all'),
    url(r'^substance/detail/(?P<id_substance>[0-9]+)/$', chemical.views.substance_detail, name='substance_detail'),

    url(r'^atom/all/$', chemical.views.atoms_all, name='atoms_all'),
    url(r'^atom/detail/(?P<atom_number>[0-9]+)/$', chemical.views.atom_detail, name='atom_detail'),

    url(r'^dictionaries/$', chemical.views.dictionaries, name='dictionaries'),
    url(r'^calculation/all/$', chemical.views.calculations_all, name='calculations_all'),

]
