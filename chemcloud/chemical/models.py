# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User

from chemical.chemical_models import Atom, Substance, Reaction, UserReaction
from chemical.chemical_models import ReactionSubst, Experiment, Reaction_scheme
from chemical.chemical_models import Scheme_step


def owner_required(f):
    def decorator(request, *args, **kwargs):
        id_reaction = kwargs['id_reaction']
        is_owner = request.user.chemistry.is_owner(id_reaction)
        if not is_owner:
            raise PermissionDenied
        return f(request, *args, **kwargs)

    return decorator


#Объект для доступа к химии
class Chemistry(models.Model):
    user = AutoOneToOneField(User, primary_key=True, null = False,on_delete=models.CASCADE)

    def substance_all(self):
        return Substance.objects.all()

    def substance_get(self, id_substance):
        try:
            subst = Substance.objects.get(pk=id_substance)
        except Substance.DoesNotExist:
            raise Http404("Substance does not exist")
        return subst

    def atom_all(self):
        return Atom.objects.all()


    def atom_get(self, atom_number):
        try:
            atom = Atom.objects.get(pk=atom_number)
        except Atom.DoesNotExist:
            raise Http404("Atom does not exist")
        return atom

    def reaction_all(self):
        return self.user.reactions.all()

    def is_owner(self, id_reaction):
        try:
            react = UserReaction.objects.get(reaction__pk=id_reaction, user__pk = self.user.pk)
        except UserReaction.DoesNotExist:
            raise Http404("Reaction does not exist or access denied")
        return react.is_owner

#на самом деле возвращает объект UserReaction
    def reaction_get(self, id_reaction):
        try:
            react = UserReaction.objects.get(reaction__pk=id_reaction, user__pk = self.user.pk)
        except UserReaction.DoesNotExist:
            raise Http404("Reaction does not exist or access denied")
        return react


    def react_subst_all(self, id_reaction):
        react = self.reaction_get(id_reaction)
        return react.reaction.substances.all()

    def react_subst_get(self, id_reaction, id_react_subst):
        react = self.reaction_get(id_reaction)
        try:
            subst = react.reaction.substances.get(pk=id_react_subst)
        except ReactionSubst.DoesNotExist:
            raise Http404("Substance does not exist")
        subst_dict = {}
        subst_dict['substance'] = subst
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


    class Meta:
      verbose_name = ('Доступ к Химии')
      verbose_name_plural = ('Доступ к Химии')
