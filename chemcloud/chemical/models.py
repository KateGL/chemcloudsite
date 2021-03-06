# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied


from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User

from chemical.chemical_models import Dict_atom, Substance, Reaction, User_reaction
from chemical.chemical_models import Reaction_subst, Experiment, Exper_serie, Reaction_scheme
from chemical.chemical_models import Scheme_step, Substance_synonym, Dict_feature
from chemical.chemical_models import Reaction_feature,Exper_subst,Dict_model_function, Exper_arg_value
from chemical.chemical_models import Problem, Dict_problem_type,Dict_model_argument,Dict_measure_unit
from chemical.chemical_models import Dict_calc_criteria_constraints, Dict_calc_functional, Dict_calc_param


def owner_required(f):
    def decorator(request, *args, **kwargs):
        id_reaction = kwargs['id_reaction']
        is_owner = request.user.chemistry.is_owner(id_reaction)
        if not is_owner:
            raise PermissionDenied
        return f(request, *args, **kwargs)

    return decorator


def substance_owner_required(f):
    def decorator(request, *args, **kwargs):
        is_owner = request.user.chemistry.is_substance_owner
        #print(is_owner)
        if not is_owner:
            raise PermissionDenied
        return f(request, *args, **kwargs)

    return decorator


def substance_get_isomer(consist_as_string, top_count):
    filter_search = Q(consist_as_string__exact=consist_as_string) #& ~Q(pk=id_substance)
    if top_count > 0:
        return Substance.objects.filter(filter_search)[:top_count]
    else:
        return Substance.objects.filter(filter_search)


def substance_get_isomer_count(consist_as_string):
    filter_search = Q(consist_as_string__exact=consist_as_string) #& ~Q(pk=id_substance)
    return Substance.objects.filter(filter_search).count()



#Объект для доступа к химии
class Chemistry(models.Model):
    user = AutoOneToOneField(User, primary_key=True, null=False, on_delete=models.CASCADE)
    is_substance_owner = models.BooleanField(default=False, null=False, verbose_name='Редактирует Вещества')

    def __unicode__(self):
        return self.user.username

    def substance_all(self):
        return Substance.objects.all()

    def substance_get(self, id_substance):
        try:
            subst = Substance.objects.get(pk=id_substance)
        except Substance.DoesNotExist:
            raise Http404("Substance does not exist")
        return subst

    def substance_get_like(self, searched, top_count):
        filter_search = Q(name__icontains=searched) | Q(formula_brutto__icontains=searched)
        if top_count > 0:
            return Substance.objects.filter(filter_search)[:top_count]
        else:
            return Substance.objects.filter(filter_search)

    def atom_all(self):
        return Dict_atom.objects.all()

    def atom_get(self, atom_number):
        try:
            atom = Dict_atom.objects.get(pk=atom_number)
        except Dict_atom.DoesNotExist:
            raise Http404("Atom does not exist")
        return atom

    def reaction_all(self):
        return self.user.reactions.all()

    def reaction_search(self, searched):
        if searched == '':
            return self.reaction_all()
        else:
            filter_search = Q(reaction__name__icontains=searched) | Q(reaction__description__icontains=searched)
            return self.user.reactions.filter(filter_search)

    def is_owner(self, id_reaction):
        try:
            react = User_reaction.objects.get(reaction__pk=id_reaction, user__pk=self.user.pk)
        except User_reaction.DoesNotExist:
            raise Http404("Reaction does not exist or access denied")
        return react.is_owner

#на самом деле возвращает объект UserReaction
    def reaction_get(self, id_reaction):
        try:
            react = User_reaction.objects.get(reaction__pk=id_reaction, user__pk=self.user.pk)
        except User_reaction.DoesNotExist:
            raise Http404("Reaction does not exist or access denied")
        return react

    def get_user_by_email(self, user_email):
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise Http404("User with email %s does not exist" % user_email)
        return user

    def react_subst_all(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.substances.all().order_by('alias')

    def react_subst_get(self, id_reaction, id_react_subst):
        react = self.reaction_get(id_reaction)
        try:
            subst = react.reaction.substances.get(pk=id_react_subst)
        except Reaction_subst.DoesNotExist:
            raise Http404("Substance does not exist")
        subst_dict = {}
        subst_dict['substance'] = subst
        subst_dict['is_owner'] = react.is_owner
        return subst_dict

    def react_subst_filterbyAlias(self, id_reaction, alias_str):
        react = self.reaction_get(id_reaction)
        try:
            subst_list = react.reaction.substances.filter(alias=alias_str)
            if subst_list.count() > 1:
                raise Http404("More than substance with alias: '"+ alias_str + "'")
            if subst_list.count() == 0:
                raise Http404("There are no any reaction substance with alias: '"+ alias_str + "'")
        except:
            return {}
#        except Reaction_subst.DoesNotExist:
#            raise Http404("There are no any reaction substance with alias: '"+ alias_str + "'")
        subst_dict = {}
        subst_dict['substance'] = subst_list[0]
        subst_dict['is_owner'] = react.is_owner
        return subst_dict

    def react_scheme_all(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.schemes.all()

    def react_scheme_get(self, id_reaction, id_scheme):
        react = self.reaction_get(id_reaction)
        try:
            scheme = react.reaction.schemes.get(pk=id_scheme)
        except Reaction_scheme.DoesNotExist:
            raise Http404("Reaction_scheme does not exist")
        scheme_dict = {}
        scheme_dict['scheme'] = scheme
        scheme_dict['is_owner'] = react.is_owner
        return scheme_dict

    def rscheme_step_all(self, id_reaction, id_scheme):
        scheme_dict = self.react_scheme_get(id_reaction, id_scheme)
        steps_dict = {}
        steps_dict['steps'] = scheme_dict['scheme'].steps.all()
        steps_dict['is_owner'] = scheme_dict['is_owner']
        return steps_dict

    def rscheme_step_get(self, id_reaction, id_scheme, id_step):
        scheme_dict = self.react_scheme_get(id_reaction, id_scheme)
        try:
            sch_step = scheme_dict['scheme'].steps.get(pk=id_step)
        except Scheme_step.DoesNotExist:
            raise Http404("Step does not exist")
        step_dict = {}
        step_dict['step'] = sch_step
        step_dict['is_owner'] = scheme_dict['is_owner']
        return step_dict

    def rscheme_step_get_byorder(self, id_reaction, id_scheme, _order):
        scheme_dict = self.react_scheme_get(id_reaction, id_scheme)
        try:
            sch_step = scheme_dict['scheme'].steps.get(order=_order)
        except Scheme_step.DoesNotExist:
            raise Http404("Step does not exist")
        step_dict = {}
        step_dict['step'] = sch_step
        step_dict['is_owner'] = scheme_dict['is_owner']
        return step_dict

    def experiment_all(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.experiments.all()

    def experiment_search(self, id_reaction, searched):
        react = self.reaction_get(id_reaction)
        filter_search = Q(name__icontains=searched) | Q(description__icontains=searched) | Q(exper_serie__name__icontains=searched) | Q(exper_serie__description__icontains=searched)
        return react.reaction.experiments.filter(filter_search)

    def experiment_all_no_serie(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.experiments.filter(exper_serie=None)

    def experiment_get(self, id_reaction, id_experiment):
        react = self.reaction_get(id_reaction)
        try:
            exp = self.experiment_all(id_reaction).get(pk=id_experiment)
        except Experiment.DoesNotExist:
            raise Http404("Experiment does not exist")
        exp_dict = {}
        exp_dict['experiment'] = exp
        exp_dict['is_owner'] = react.is_owner
        return exp_dict

    def exper_serie_all(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.exper_series.all().order_by('name')

    def exper_serie_get(self, id_reaction, id_experserie):
        react = self.reaction_get(id_reaction)
        try:
            exp = react.reaction.exper_series.all().get(pk=id_experserie)
        except Exper_serie.DoesNotExist:
            raise Http404("Exper_serie does not exist")
        exp_dict = {}
        exp_dict['exper_serie'] = exp
        exp_dict['is_owner'] = react.is_owner
        return exp_dict

    # получить вещества эксперимента
    def exper_subst_all(self, id_reaction, id_experiment):
        exper_dict = self.experiment_get(id_reaction, id_experiment)
        return exper_dict['experiment'].exper_substs.all().order_by('reaction_subst__alias')

    #по id вещества эксперимента получить вещество эксперимента
    def exper_subst_get(self, id_expersubst):
        try:
            exper_subst = Exper_subst.objects.get(pk=id_expersubst)
        except Exper_subst.DoesNotExist:
            raise Http404("Experiment substance does not exist or access denied")
        return exper_subst

    def exper_arg_get(self, id_argument):
        try:
            exper_arg = Exper_arg_value.objects.get(pk=id_argument)
        except Exper_arg_value.DoesNotExist:
            raise Http404("Experiment argument does not exist or access denied")
        return exper_arg

    #по id вещества эксперимента получить экспериментальные точки
    def exper_points(self, id_expersubst):
        exp_subst = self.exper_subst_get(id_expersubst)
        return exp_subst.exper_func_points.all()

    def exper_point_get(self, id_expersubst, id_argument):
        exper_subst = self.exper_subst_get(id_expersubst)
        point_list = exper_subst.exper_func_points.all().filter(argument__pk=id_argument)
        if len(point_list) > 0:
            return point_list[0]
        else:
            return None

    def dict_model_funct_all(self):
        return Dict_model_function.objects.all()

    # по id функции модели
    def dict_model_funct_get(self, id_func):
        try:
            dict_model_funct = Dict_model_function.objects.get(pk=id_func)
        except Dict_model_function.DoesNotExist:
            raise Http404("Dict_model_function does not exist or access denied")
        return dict_model_funct

    # по id реакции вернуть все характеристики реакции
    def react_feature_all(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.reac_features.all()

    # по id реакции вернуть все тэги реакции
    def react_tag_all(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.reac_tags.all()

    # по id вещества
    def subst_synonym_all(self, id_substance):
        try:
            subst = Substance_synonym.objects.get(pk=id_substance)
        except Substance_synonym.DoesNotExist:
            raise Http404("Substance does not exist")
        return subst

    # по id синонима вернуть синоним вещества
    def subst_synonym_get(self, id_subst_synonym):
        try:
            subst_synonym = Substance_synonym.objects.get(pk=id_subst_synonym)
        except Substance_synonym.DoesNotExist:
            raise Http404("Substance_synonym does not exist")
        return subst_synonym

    #вернуть весь справочник характеристик
    def dict_feature_all(self):
        return Dict_feature.objects.all()

    # вернуть характеристику по id характеристики
    def dict_feature_get(self, id_feat):
        try:
            dict_feature = Dict_feature.objects.get(pk=id_feat)
        except Dict_feature.DoesNotExist:
            raise Http404("Dict_feature does not exist")
        return dict_feature

    # все аргументы модели
    def dict_model_arg_all(self):
        return Dict_model_argument.objects.all()

    # вернуть аргумент по id аргумента
    def dict_model_arg_get(self, id_arg):
        try:
            dict_model_arg = Dict_model_argument.objects.get(pk=id_arg)
        except Dict_model_argument.DoesNotExist:
            raise Http404("Dict_model_argument does not exist")
        return dict_model_arg

    # вернуть все единицы измерения
    def dict_unit_all(self):
        return Dict_measure_unit.objects.all()

    # вернуть ед.изм. по id ед.изм.
    def dict_unit_get(self, id_unit):
        try:
            dict_unit = Dict_measure_unit.objects.get(pk=id_unit)
        except Dict_measure_unit.DoesNotExist:
            raise Http404("Dict_measure_unit does not exist")
        return dict_unit

    def problem_all(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.problems.all()

    def problem_get(self, id_reaction, id_problem):
        react = self.reaction_get(id_reaction)
        try:
            problem = react.reaction.problems.get(pk=id_problem)
        except Problem.DoesNotExist:
            raise Http404("Problem does not exist")
        problem_dict = {}
        problem_dict['problem'] = problem
        problem_dict['is_owner'] = react.is_owner
        return problem_dict

    def dict_problem_type_get(self, id):
        try:
            problem_type = Dict_problem_type.objects.get(pk=id)
        except Dict_problem_type.DoesNotExist:
            raise Http404("Dict_problem_type does not exist")
        return problem_type

    # вернуть критерии, отфильтрованные по типу задачи
    def dict_criteria_filter(self, id_problem_type):
        try:
            _list=[]
            if id_problem_type == 2: #обратная задача
                _list.append(Dict_calc_criteria_constraints.objects.get(pk=1))
                _list.append(Dict_calc_criteria_constraints.objects.get(pk=2))
        except:
            raise Http404("Error in getting criteria list")
        return _list

    # вернуть ограничения, отфильтрованные по типу задачи
    def dict_constraints_filter(self, id_problem_type):
        try:
            _list=[]
            if id_problem_type == 2: #обратная задача
                _list.append(Dict_calc_criteria_constraints.objects.get(pk=2))
                _list.append(Dict_calc_criteria_constraints.objects.get(pk=3))
        except:
            raise Http404("Error in getting constraints list")
        return _list

    # вернуть все виды функционалов невязки
    def dict_calc_functional_all(self):
        return Dict_calc_functional.objects.all()

    # вернуть функционалов невязки по id
    def dict_calc_functional_get(self, _id):
        try:
            dict_calc_functional = Dict_calc_functional.objects.get(pk=_id)
        except Dict_calc_functional.DoesNotExist:
            raise Http404("Dict_calc_functional does not exist")
        return dict_calc_functional

    # вернуть контекст для каждой задачи: параметры задачи, а также всевозможные выпадающие списки и т.д.
    def get_problem_context(self, problem, page_num):
        try:
            id_problem_type = problem.problem_type.id_problem_type
            if id_problem_type==2:#обратная задача
                problem_context = self.get_inverse_problem_context(problem, page_num)
        except:
            raise Http404("Error in getting problem context")
        return problem_context

    def get_inverse_problem_context(self, problem, page_num):
        try:
            problem_context = {}
            if page_num == 1: #init - постановка задачи
                functional_value = None # бд позволяет. Но пока так не умеем считать. Пока что один вид функционала на все ограничения и критерии
                criteria_value  = None #значение выбранного критерия. Пока что однокритериальные задачи
                constraints_value_list = [] #значения выбранных ограничений.
                scheme = None #выбранный механизм реакции
                schemes_list_combo = []#список всех механизмов реакции
                expers_value_list = [] #список всех экспериментов реакции с пометкой, выбран эксперимент в задаче или нет
                left_bound_value_list = []
                rigth_bound_value_list = []

                id_problem_type = problem.problem_type.id_problem_type
                criteria_value   = problem.constraints.filter(is_constraint = False)[0] #обязательно должно существовать
                constraints_value_list = problem.constraints.filter(is_constraint = True)
                functional_value = criteria_value.functional

                schemes_list_combo = problem.reaction.schemes.all()
                scheme = problem.scheme
                exper_list = problem.reaction.experiments.all()
                problem_exper_list = problem.expers.all()
                problem_exper_list = list(problem_exper_list)
                for exper in exper_list:
                    pos_exper = problem_exper_list.index(exper)
                    temp_list = [exper]
                    if  pos_exper < 0:
                        temp_list.append(False)
                    else:
                        temp_list.append(True)
                    expers_value_list.append(temp_list)
                #границы
                if scheme is not None:
                    temp_param_dir_down = Dict_calc_param.objects.get(pk = 5)#min k->
                    temp_param_inv_down = Dict_calc_param.objects.get(pk = 6)#min k<-
                    temp_param_dir_up   = Dict_calc_param.objects.get(pk = 11)#max k->
                    temp_param_inv_up   = Dict_calc_param.objects.get(pk = 12)#max k<-
                    left_bound_value_list.append(problem.params.filter(dict_param = temp_param_dir_down).order_by('step__order') )
                    temp_list = problem.params.filter(dict_param = temp_param_inv_down).order_by('step__order')
                    if temp_list.count()>0:
                        left_bound_value_list.append(temp_list)
                    rigth_bound_value_list.append(problem.params.filter(dict_param = temp_param_dir_up).order_by('step__order'))
                    temp_list = problem.params.filter(dict_param = temp_param_inv_up).order_by('step__order')
                    if temp_list.count()>0:
                        rigth_bound_value_list.append(temp_list)
                problem_context = { 'criteria_value': criteria_value,  'constraints_value_list': constraints_value_list,  'functional_value':functional_value, 'schemes_list_combo':schemes_list_combo, 'scheme':scheme, 'expers_value_list':expers_value_list, 'left_bound_value_list':left_bound_value_list, 'rigth_bound_value_list':rigth_bound_value_list}
        except:
            raise Http404("Error in getting inverse problem context")
        return problem_context

    class Meta:
        verbose_name = ('Доступ к Химии')
        verbose_name_plural = ('Доступ к Химии')
