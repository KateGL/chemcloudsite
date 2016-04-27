# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from chemical.chemical_models import Dict_atom, Substance, Reaction, Reaction_scheme, Experiment
from chemical.chemical_models import Scheme_step, Scheme_step_subst
from chemical.chemical_models import Reaction_subst,Substance_synonym,Reaction_tag,Dict_feature,Reaction_feature, Dict_model_function, Dict_model_argument, Dict_measure_unit
from chemical.chemical_models import User_reaction,Substance_consist,Exper_subst,Dict_subst_role
from chemical.chemical_models import Dict_exper_param,Dict_exper_subst_param,Exper_data,Exper_subst_data
from chemical.chemical_models import Exper_point
from chemical.models import Chemistry


class Dict_atomAdmin(admin.ModelAdmin):
  fields = ['atom_number', 'symbol','atom_mass',  'name', 'name_latin']
  list_display = ('atom_number', 'symbol', 'atom_mass', 'name', 'name_latin')

admin.site.register(Dict_atom, Dict_atomAdmin)


class SubstanceAdmin(admin.ModelAdmin):
  #formula_brutto = BruttoFormulaField( label="Брутто-формула") надо в админке тоже добавить это поле!!!
  fields = ['name', 'charge', 'is_radical', 'formula_brutto','note']
  list_display = ('id_substance',  'name',  'charge', 'is_radical', 'formula_brutto','note')

admin.site.register(Substance, SubstanceAdmin)

class ReactionAdmin(admin.ModelAdmin):
  #fields = ['name',  'is_favorite', 'is_notstationary',
 #'is_isothermal','description', 'created_by' ]
 # list_display = ('id_reaction',  'name', 'is_favorite', 'is_notstationary',
 #'is_isothermal','description', 'created_by' )
  fields = ['name',  'is_favorite','description', 'created_by' ]
  list_display = ('id_reaction',  'name', 'is_favorite', 'description', 'created_by' )

admin.site.register(Reaction, ReactionAdmin)

admin.site.register(Chemistry)

#  механизмы реакции

#class ReactionSchemeAdmin(admin.ModelAdmin):
  #fields = ['name','reaction']
  #list_display = ('id_scheme', 'name','reaction')

admin.site.register( Reaction_scheme)

admin.site.register( Scheme_step)

admin.site.register( Scheme_step_subst)

#Вещества реакции
admin.site.register( Reaction_subst)

#  Эксперименты
admin.site.register(Experiment)#, ReactionSchemeAdmin)

#Состав вещества
admin.site.register(Substance_consist)

#Права пользователя
admin.site.register(User_reaction)

#Синонимы вещества
admin.site.register(Substance_synonym)

#Свойства (свойства реакции)
admin.site.register(Dict_feature)

#Свойства реакции
admin.site.register(Reaction_feature)

#Тэги реакции
admin.site.register(Reaction_tag)

#Функции модели
admin.site.register(Dict_model_function)

#Аргументы модели
admin.site.register(Dict_model_argument)

#Единицы
admin.site.register(Dict_measure_unit)

#Вещества реакции в эксперименте
admin.site.register(Exper_subst)

#Роли вещества в механизме
admin.site.register(Dict_subst_role)

#Дополнительные данные эксперимента
admin.site.register(Dict_exper_param)

#Дополнительная информация о веществе реакции
admin.site.register(Dict_exper_subst_param)

#Дополнительная информация эксперимента
admin.site.register(Exper_data)

#Дополнительные экспериментальные данные
admin.site.register(Exper_subst_data)

#Экспериментальные данные
admin.site.register(Exper_point)