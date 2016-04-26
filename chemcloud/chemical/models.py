# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User

from chemical.chemical_models import Dict_atom, Substance, Reaction, User_reaction
from chemical.chemical_models import Reaction_subst, Experiment, Reaction_scheme
from chemical.chemical_models import Scheme_step, Substance_synonym, Dict_feature
from chemical.chemical_models import Reaction_feature


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
        if top_count > 0:
            return Substance.objects.filter(Q(name__icontains=searched) | Q(formula_brutto__icontains=searched))[:top_count]
        else:
            return Substance.objects.filter(Q(name__icontains=searched) | Q(formula_brutto__icontains=searched))

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
        return react.reaction.substances.all()

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
        except Reaction_subst.DoesNotExist:
            raise Http404("Substance does not exist")
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

    def experiment_get(self, id_reaction, id_experiment):
        react = self.reaction_get(id_reaction)
        try:
            exp = react.reaction.experiments.get(pk=id_experiment)
        except Experiment.DoesNotExist:
            raise Http404("Experiment does not exist")
        exp_dict = {}
        exp_dict['experiment'] = exp
        exp_dict['is_owner'] = react.is_owner
        return exp_dict

    # по id вещества
    def subst_synonym_all(self, id_substance):
        try:
            subst = Substance_synonym.objects.get(pk=id_substance)
        except Substance_synonym.DoesNotExist:
            raise Http404("Substance does not exist")
        return subst

    # по id синонима (возможно не нужен)
    # def subst_synonym_get(self,):

    #вернуть весь справочник характеристик
    def dic_feature_all(self):
        return Dict_feature.objects.all()

    # вернуть характеристику по id характеристики
    def dic_feature_get(self, id_feat):
        try:
            dict_feature = Dict_feature.objects.get(pk=id_feat)
        except Dict_feature.DoesNotExist:
            raise Http404("Dict_feature does not exist")
        return dict_feature

    # TODO

    # по id реакции вернуть все характеристики реакции
    #def react_feature_all(self, id_reac):

    # по id реакции
    #def react_tag_all

    # по id реакции и id тэга
    #def react_tag_get

    #* exper_subst_all(..), exper_subst_get(по id вещества эксперимента)
    #* dict_model_funct_all(..), //
    #dict_model_funct_get(по id фукнции)
    #* dict_model_arg_all(..),
    #dict_model_arg_get(по id аргумента)
    #* dict_unit_all(..),
    #dict_unit_get(.по id ед.изм.)

    class Meta:
        verbose_name = ('Доступ к Химии')
        verbose_name_plural = ('Доступ к Химии')
