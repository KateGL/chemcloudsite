# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from chemical.chemical_models import Dict_atom, Substance, Reaction, Reaction_scheme, Experiment
from chemical.chemical_models import Scheme_step, Scheme_step_subst
from chemical.chemical_models import Reaction_subst,Substance_synonym,Reaction_tag,Dict_feature,Reaction_feature, Dict_model_function, Dict_model_argument, Dict_measure_unit
from chemical.chemical_models import User_reaction,Substance_consist,Exper_subst
from chemical.chemical_models import Dict_exper_param,Dict_exper_subst_param,Exper_extradata,Exper_subst_extradata
from chemical.chemical_models import Exper_serie
from chemical.chemical_models import Dict_problem_type, Problem
from chemical.chemical_models import Dict_calc_criteria_constraints, Dict_calc_functional
from chemical.chemical_models import Dict_calc_param, Dict_problem_class, Dict_calc_method, Calc_param, Calc_criteria_constraint
from chemical.chemical_models import Exper_func_point, Exper_arg_value
from chemical.models import Chemistry
#from chemical.chemical_models import Calc_log, Dict_calc_status


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

admin.site.register(Exper_func_point)
admin.site.register(Exper_arg_value)

#  механизмы реакции

#class ReactionSchemeAdmin(admin.ModelAdmin):
  #fields = ['name','reaction']
  #list_display = ('id_scheme', 'name','reaction')

class Reaction_schemeAdmin(admin.ModelAdmin):
  fields = ['reaction','name','description','is_possible']
  list_display = ('reaction','name','description','is_possible')

admin.site.register(Reaction_scheme,Reaction_schemeAdmin)

class Scheme_stepAdmin(admin.ModelAdmin):
  fields = ['scheme','name','order','is_revers','note','rate_equation']
  list_display = ('scheme','name','order','is_revers','note','rate_equation')

admin.site.register(Scheme_step,Scheme_stepAdmin)

class Scheme_step_substAdmin(admin.ModelAdmin):
  fields = ['step','reac_substance','position','stoich_koef']
  list_display = ('step','reac_substance','position','stoich_koef')

admin.site.register(Scheme_step_subst,Scheme_step_substAdmin)

#Вещества реакции
class Reaction_substAdmin(admin.ModelAdmin):
  fields = ['reaction','substance','alias','brutto_formula_short','note']
  list_display = ('reaction','substance','alias','brutto_formula_short','note')

#admin.site.register(Reaction_subst)
admin.site.register(Reaction_subst,Reaction_substAdmin)

#  Эксперименты
class ExperimentAdmin(admin.ModelAdmin):
  fields = ['name','reaction','arg','argument_measure','func','function_measure','init_function_measure','description', 'exper_serie', 'exper_date','is_favorite','created_date','created_by','updated_by','updated_date']
  list_display = ('name','reaction','arg','argument_measure','func','function_measure','init_function_measure','description', 'exper_serie','exper_date','is_favorite','created_date','created_by','updated_by','updated_date')

admin.site.register(Experiment,ExperimentAdmin)

#Состав вещества
class Substance_consistAdmin(admin.ModelAdmin):
  fields = [ 'atom','atom_count','substance']
  list_display = ('substance','atom', 'atom_count')

admin.site.register(Substance_consist,Substance_consistAdmin)

#Права пользователя
admin.site.register(User_reaction)

#Синонимы вещества
class Substance_synonymAdmin(admin.ModelAdmin):
  fields = ['substance','name']
  list_display = ('substance','name')

admin.site.register(Substance_synonym,Substance_synonymAdmin)

#Свойства (свойства реакции)
class Dict_featureAdmin(admin.ModelAdmin):
  fields = ['id_feature', 'name']
  list_display = ('id_feature', 'name')

admin.site.register(Dict_feature,Dict_featureAdmin)

#Свойства реакции
class Reaction_featureAdmin(admin.ModelAdmin):
  fields = ['reaction','feature']
  list_display = ('reaction','feature')

admin.site.register(Reaction_feature,Reaction_featureAdmin)

#Тэги реакции
class Reaction_tagAdmin(admin.ModelAdmin):
  fields = ['reaction','tag']
  list_display = ('reaction','tag')

admin.site.register(Reaction_tag,Reaction_tagAdmin)

#Функции модели
class Dict_model_functionAdmin(admin.ModelAdmin):
  fields = ['id_func', 'name','symbol']
  list_display = ('id_func', 'name','symbol')

admin.site.register(Dict_model_function,Dict_model_functionAdmin)

#Аргументы модели
class Dict_model_argumentAdmin(admin.ModelAdmin):
  fields = ['id_arg', 'name','symbol']
  list_display = ('id_arg', 'name','symbol')

admin.site.register(Dict_model_argument,Dict_model_argumentAdmin)

#Единицы
class Dict_measure_unitAdmin(admin.ModelAdmin):
  fields = ['id_unit', 'code','name','is_si','multiplier','unit_si']
  list_display = ('id_unit','name', 'code','is_si','multiplier','unit_si')

admin.site.register(Dict_measure_unit,Dict_measure_unitAdmin)


#Вещества реакции в эксперименте
class Exper_substAdmin(admin.ModelAdmin):
  fields = ['experiment', 'reaction_subst', 'is_observed', 'init_func_val', 'standard_error']
  list_display = ('experiment', 'reaction_subst', 'is_observed', 'init_func_val', 'standard_error')

admin.site.register(Exper_subst, Exper_substAdmin)


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
class Exper_extradataAdmin(admin.ModelAdmin):
  fields = ['experiment','value','exper_param','dict_unit_id_unit']
  list_display = ('experiment','value','exper_param','dict_unit_id_unit')

admin.site.register(Exper_extradata,Exper_extradataAdmin)


#Дополнительные экспериментальные данные
class Exper_subst_extradataAdmin(admin.ModelAdmin):
    fields = ['exper_subst', 'value', 'subst_param', 'unit']
    list_display = ('exper_subst', 'value', 'subst_param', 'unit')

admin.site.register(Exper_subst_extradata, Exper_subst_extradataAdmin)


#Серии экспериентов
class Exper_serieAdmin(admin.ModelAdmin):
  fields = ['name','description']
  list_display = ('name','description')

admin.site.register(Exper_serie,Exper_serieAdmin)

#Эксперименты в серии экспериментов
class Experserie_experimentAdmin(admin.ModelAdmin):
  fields = ['experiment','exper_serie']
  list_display = ('experiment','exper_serie')


#Справочник параметров расчета
class Dict_calc_paramAdmin(admin.ModelAdmin):
  fields = ['id_dict_param','name', 'mask']
  list_display = ('id_dict_param','name', 'mask')

admin.site.register(Dict_calc_param,Dict_calc_paramAdmin)


#Справочник статусов решения задачи
#class Dict_calc_statusAdmin(admin.ModelAdmin):
#  fields = ['id_status','name']
#  list_display = ('id_status','name')

#admin.site.register(Dict_calc_status,Dict_calc_statusAdmin)

class Calc_criteria_constraintAdmin(admin.ModelAdmin):
  fields = ['id_ccc', 'is_constraint', 'problem', 'criteria', 'functional' ]
  list_display = ('id_ccc', 'is_constraint', 'problem', 'criteria', 'functional'  )

admin.site.register(Calc_criteria_constraint,Calc_criteria_constraintAdmin)

class Calc_paramAdmin(admin.ModelAdmin):
  fields = ['id_calc_param', 'is_input', 'value', 'problem', 'dict_param', 'step', 'substance' ]
  list_display = ('id_calc_param', 'is_input', 'value', 'problem', 'dict_param', 'step', 'substance'  )

admin.site.register(Calc_param,Calc_paramAdmin)

#class Calc_logAdmin(admin.ModelAdmin):
#  fields = ['id_calc_log', 'calc', '_log' ]
#  list_display = ('id_calc_log', 'calc', '_log'  )
#
#admin.site.register(Calc_log,Calc_logAdmin)

class Dict_calc_functionalAdmin(admin.ModelAdmin):
  fields = ['id_func', 'name' ]
  list_display = ('id_func', 'name'  )

admin.site.register(Dict_calc_functional,Dict_calc_functionalAdmin)

class ProblemAdmin(admin.ModelAdmin):
  fields = ['id_problem', 'reaction', 'problem_type', 'description', 'created_date', 'schemes', 'expers', 'exper_points', 'is_approved' ]
  list_display = ('id_problem', 'reaction', 'problem_type', 'description', 'created_date', 'is_approved' )

admin.site.register(Problem,ProblemAdmin)

class Dict_calc_methodAdmin(admin.ModelAdmin):
  fields = ['id_method', 'name', 'description', 'problem_classes' ]
  list_display = ('id_method', 'name', 'description')

admin.site.register(Dict_calc_method,Dict_calc_methodAdmin)

class Dict_problem_typeAdmin(admin.ModelAdmin):
  fields = ['id_problem_type', 'name', 'problem_classes' ]
  list_display = ('id_problem_type', 'name' )

admin.site.register(Dict_problem_type,Dict_problem_typeAdmin)

class Dict_problem_classAdmin(admin.ModelAdmin):
  fields = ['id_problem_class', 'name' ]
  list_display = ('id_problem_class', 'name')

admin.site.register(Dict_problem_class,Dict_problem_classAdmin)

