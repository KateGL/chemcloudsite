# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from chemical.chemical_models import Atom, Substance, Reaction, Reaction_scheme, Experiment
from chemical.chemical_models import Scheme_step, Step_subst
from chemical.chemical_models import ReactionSubst
from chemical.chemical_models import UserReaction


class AtomAdmin(admin.ModelAdmin):
  fields = ['atom_number', 'symbol','atom_mass',  'name', 'name_latin']
  list_display = ('atom_number', 'symbol', 'atom_mass', 'name', 'name_latin')

admin.site.register(Atom, AtomAdmin)


class SubstanceAdmin(admin.ModelAdmin):
  #formula_brutto = BruttoFormulaField( label="Брутто-формула") надо в админке тоже добавить это поле!!!
  fields = ['name', 'charge', 'is_radical', 'formula_brutto','note']
  list_display = ('id_substance',  'name',  'charge', 'is_radical', 'formula_brutto','note')

admin.site.register(Substance, SubstanceAdmin)

class ReactionAdmin(admin.ModelAdmin):
  fields = ['name',  'is_favorite', 'is_notstationary',
 'is_isothermal','description', 'created_by' ]
  list_display = ('id_reaction',  'name', 'is_favorite', 'is_notstationary',
 'is_isothermal','description', 'created_by' )

admin.site.register(Reaction, ReactionAdmin)


#  механизмы реакции

#class ReactionSchemeAdmin(admin.ModelAdmin):
  #fields = ['name','reaction']
  #list_display = ('id_scheme', 'name','reaction')

admin.site.register( Reaction_scheme)

admin.site.register( Scheme_step)

admin.site.register( Step_subst)

#Вещества реакции
admin.site.register( ReactionSubst)

#  Эксперименты
admin.site.register(Experiment)#, ReactionSchemeAdmin)


#Права пользователя
admin.site.register(UserReaction)
