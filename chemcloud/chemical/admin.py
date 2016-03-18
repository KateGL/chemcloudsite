# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from chemical.models import Atom, Substance, Reaction, Reaction_scheme
from chemical.forms import BruttoFormulaField

class AtomAdmin(admin.ModelAdmin):
  fields = ['atom_number', 'symbol','atom_mass',  'name', 'name_latin']
  list_display = ('atom_number', 'symbol', 'atom_mass', 'name', 'name_latin')

admin.site.register(Atom, AtomAdmin)


class SubstanceAdmin(admin.ModelAdmin):
  formula_brutto = BruttoFormulaField( label="Брутто-формула")
  fields = ['name', 'charge', 'is_radical', 'formula_brutto','note']
  list_display = ('id_substance',  'name',  'charge', 'is_radical', 'formula_brutto','note')

admin.site.register(Substance, SubstanceAdmin)

class ReactionAdmin(admin.ModelAdmin):
  fields = ['name',  'is_favorite', #'is_notstationary',
 'is_isothermal','description' ]
  list_display = ('id_reaction',  'name', 'is_favorite', #'is_notstationary',
 'is_isothermal','description' )

admin.site.register(Reaction, ReactionAdmin)


#  механизмы реакции

class ReactionSchemeAdmin(admin.ModelAdmin):
  fields = ['name']
  list_display = ('id_scheme', 'name')

admin.site.register( Reaction_scheme, ReactionSchemeAdmin)

#  Эксперименты

