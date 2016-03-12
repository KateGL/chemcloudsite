from django.conf.urls import patterns, url
#import chemical.views
from chemical import views

urlpatterns = [
    
    url(r'^reaction/all/$', views.reactions_all, name='reactions_all'),
    
    url(r'^substance/all/$', views.substance_all, name='substance_all'),
    url(r'^substance/detail/(?P<id_substance>[0-9]+)/$', views.substance_detail, name='substance_detail'),

    url(r'^atom/all/$', views.atoms_all, name='atoms_all'),
    url(r'^atom/detail/(?P<atom_number>[0-9]+)/$', views.atom_detail, name='atom_detail'),

    url(r'^dictionaries/$', views.dictionaries, name='dictionaries'),
    url(r'^calculation/all/$', views.calculations_all, name='calculations_all'),


    url(r'^reactions/(?P<reaction_id>[0-9]+)/schemes/$', views.schemes, name='schemes'),
    url(r'^reactions/(?P<reaction_id>[0-9]+)/schemes/(?P<scheme_id>[0-9]+)/details/$', views.scheme_details, name='scheme_details'),
    url(r'^reactions/(?P<reaction_id>[0-9]+)/schemes/new/$', views.scheme_new, name='scheme_new'),
]
