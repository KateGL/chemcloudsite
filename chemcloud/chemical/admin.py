# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from chemical.chemical_models import Dict_atom, Substance, Reaction, Reaction_scheme, Experiment
from chemical.chemical_models import Scheme_step, Scheme_step_subst
from chemical.chemical_models import Reaction_subst,Substance_synonym,Reaction_tag,Dict_feature,Reaction_feature, Dict_model_function, Dict_model_argument, Dict_measure_unit
from chemical.chemical_models import User_reaction,Substance_consist,Exper_subst,Dict_subst_role
from chemical.chemical_models import Dict_exper_param,Dict_exper_subst_param,Exper_data,Exper_subst_data
from chemical.chemical_models import Exper_point
from chemical.chemical_models import Problem, Dict_problem_type
from chemical.models import Chemistry


class Dict_atomAdmin(admin.ModelAdmin):
  fields = ['atom_number', 'symbol','atom_mass',  'name', 'name_latin']
  list_display = ('atom_number', 'symbol', 'atom_mass', 'name', 'name_latin')

admin.site.register(Dict_atom, Dict_atomAdmin)


class SubstanceAdmin(admin.ModelAdmin):
  #formula_brutto = BruttoFormulaField( label="Брутто-формула") надо в админке тоже добавить это поле!!!
  fields = ['name', 'charge', 'is_radical', 'formula_brutto','note', 'consist_as_string']
  list_display = ('id_substance',  'name',  'charge', 'is_radical', 'formula_brutto', 'consist_as_string','note')

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

class Scheme_step_substAdmin(admin.ModelAdmin):
  fields = ['id_step', 'step','reac_substance','position','stoich_koef']
  list_display = ('id_step', 'step','reac_substance','position','stoich_koef')

admin.site.register(Scheme_step_subst,Scheme_step_substAdmin)

#Вещества реакции
class Reaction_substAdmin(admin.ModelAdmin):
  fields = ['id_react_subst', 'reaction','substance','alias','brutto_formula_short','note']
  list_display = ('id_react_subst', 'reaction','substance','alias','brutto_formula_short','note')

admin.site.register(Reaction_subst,Reaction_substAdmin)

#  Эксперименты
admin.site.register(Experiment)#, ReactionSchemeAdmin)

#Состав вещества
class Substance_consistAdmin(admin.ModelAdmin):
  fields = ['id_subst_consist', 'atom','atom_count','substance']
  list_display = ('id_subst_consist', 'substance','atom', 'atom_count')

admin.site.register(Substance_consist,Substance_consistAdmin)

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
class Dict_model_argumentAdmin(admin.ModelAdmin):
  fields = ['id_arg', 'name','symbol']
  list_display = ('id_arg', 'name','symbol')

admin.site.register(Dict_model_argument,Dict_model_argumentAdmin)

#Единицы
class Dict_measure_unitAdmin(admin.ModelAdmin):
  fields = ['id_unit', 'code','name','is_si','multiplier','id_unit_si']
  list_display = ('name','id_unit', 'code','is_si','multiplier','id_unit_si')

admin.site.register(Dict_measure_unit,Dict_measure_unitAdmin)

#Вещества реакции в эксперименте
class Exper_substAdmin(admin.ModelAdmin):
  fields = ['id_expersubst', 'experiment','reaction_subst','dict_subst_role','is_observed','init_func_val']
  list_display = ('id_expersubst', 'experiment','reaction_subst','dict_subst_role','is_observed','init_func_val')

admin.site.register(Exper_subst,Exper_substAdmin)

#Роли вещества в механизме
class Dict_subst_roleAdmin(admin.ModelAdmin):
  fields = ['id_role', 'name']
  list_display = ('id_role', 'name')

admin.site.register(Dict_subst_role,Dict_subst_roleAdmin)

#Дополнительные данные эксперимента
class Dict_exper_paramAdmin(admin.ModelAdmin):
  fields = ['id_experparam', 'name']
  list_display = ('id_experparam', 'name')

admin.site.register(Dict_exper_param,Dict_exper_paramAdmin)

#Дополнительная информация о веществе реакции
class Dict_exper_subst_paramAdmin(admin.ModelAdmin):
  fields = ['id_expersubstparam', 'name']
  list_display = ('id_expersubstparam', 'name')

admin.site.register(Dict_exper_subst_param,Dict_exper_subst_paramAdmin)

#Дополнительная информация эксперимента
class Exper_dataAdmin(admin.ModelAdmin):
  fields = ['id_exper_data', 'experiment','value','exper_param','dict_unit_id_unit']
  list_display = ('id_exper_data', 'experiment','value','exper_param','dict_unit_id_unit')

admin.site.register(Exper_data,Exper_dataAdmin)

#Дополнительные экспериментальные данные
class Exper_subst_dataAdmin(admin.ModelAdmin):
  fields = ['id_exper_subst_data', 'exper_subst','value','subst_param','unit']
  list_display = ('id_exper_subst_data', 'exper_subst','value','subst_param','unit')

admin.site.register(Exper_subst_data,Exper_subst_dataAdmin)

#Экспериментальные данные
admin.site.register(Exper_point)

#Задачи
admin.site.register(Problem)
admin.site.register(Dict_problem_type)