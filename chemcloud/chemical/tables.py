# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
#from django.utils.html import escape

from chemical.chemical_models import Dict_atom, Substance, Substance_consist, Reaction_scheme, Experiment
from chemical.chemical_models import Scheme_step, Scheme_step_subst
from chemical.chemical_models import Reaction_subst, User_reaction
from chemical.chemical_models import Problem

from .urls_utils import make_detail_link, make_name_link, make_isomer_link

class AtomTable(tables.Table):
    detail_link = tables.LinkColumn('atom_detail', orderable=False,  verbose_name='Ссылка', empty_values=())

    def render_detail_link(self,record):
        link = reverse('chemical.views.atom_detail', args=[record.pk])
        return make_detail_link(link)

    class Meta:
        model = Dict_atom
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("atom_number", "symbol", "name", "name_latin", "atom_mass")


class SubstanceTable(tables.Table):
    detail_link = tables.LinkColumn('substance_detail', orderable=False,  verbose_name='Ссылка', empty_values=())
    isomer_link = tables.LinkColumn('substance_isomer', orderable=False,  verbose_name='Изомеры', empty_values=())

    def render_formula_brutto_formatted(self, record):
        return mark_safe(record.formula_brutto_formatted)

    def render_detail_link(self, record):
        link = reverse('chemical.views.substance_detail', args=[record.pk])
        return make_detail_link(link)

    def render_isomer_link(self, record):
        if record.consist_as_string > '':
            link = reverse('chemical.views.substance_isomers', args=[record.consist_as_string])
            return make_isomer_link(link)
        return ''

    class Meta:
        model = Substance
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("name", "formula_brutto_formatted", "charge", "is_radical")
        sequence = ("name", "formula_brutto_formatted", "charge", "is_radical")


class ConsistTable(tables.Table):
    atom_symbol = tables.Column(accessor='atom.symbol')

    def render_atom_count(self, record):
        return str(record.atom_count.normalize())

    class Meta:
        model = Substance_consist
        attrs = {"class": "paleblue"}
        fields = ("atom_symbol", "atom_count")
        sequence = ("atom_symbol", "atom_count")


#Реакции
class ReactionTable(tables.Table):
    detail_link = tables.LinkColumn('reaction_detail', args=[A('pk')], orderable=False,  verbose_name='Ссылка', empty_values=())
    name = tables.Column(accessor='reaction.name')
    is_favorite = tables.Column(accessor='reaction.is_favorite')
    description = tables.Column(accessor='reaction.description')
    updated_date = tables.Column(accessor='reaction.updated_date')
    user_rule = tables.Column(verbose_name='Права', orderable=False, empty_values=())

    def render_detail_link(self, record):
        link = reverse('chemical.views.reaction_detail', args=[record.reaction.pk])
        return make_detail_link(link)

    def render_user_rule(self, record):
        if record.is_owner:
            return 'Чтение, Редактирование, Поделиться'
        else:
            return 'Чтение'

    class Meta:
        model = User_reaction
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("name", "is_favorite", "description", "updated_date", "user_rule", "detail_link")
        sequence = ("is_favorite", "name",  "description", "updated_date","detail_link", "user_rule")


#Права на Реакции
class UserOfReactionTable(tables.Table):
    user_name = tables.Column(verbose_name='Пользователь', accessor='user.username')
    user_email = tables.Column(verbose_name='E-mail', accessor='user.email')
    user_rule = tables.Column(verbose_name='Права', orderable=False, empty_values=())

    def render_user_rule(self, record):
        if record.is_owner:
            return 'Чтение, Редактирование, Поделиться'
        else:
            return 'Чтение'

    class Meta:
        model = User_reaction
        attrs = {"class": "paleblue"}
        fields = ("user_name", "user_rule", "user_email")
        sequence = ("user_name", "user_email", "user_rule")




#Механизмы
class MechanizmTable(tables.Table):
    #args=[A('pk')], и без этого работает
    detail_link = tables.LinkColumn('scheme_detail', orderable=False,  verbose_name='', empty_values=())
    name = tables.LinkColumn('scheme_edit', orderable=True)
    #для колонки с пустым значением render вызывается, если стоит empty_values=())
    steps_count = tables.Column(verbose_name='Число стадий', orderable=False, empty_values=())

    def render_detail_link(self, record):
        link = reverse('chemical.views.scheme_detail', args=[record.reaction.id_reaction, record.pk])
        return make_detail_link(link)

    def render_name(self, record):
        link = reverse('chemical.views.scheme_edit', args=[record.reaction.id_reaction, record.pk])
        return make_name_link(link, record.name)


    def render_steps_count(self, record):
        ##TODO число стадий подсчитать и вывести
        ##получаем число стадий схемы по scheme
        steps_count = Scheme_step.objects.filter(scheme = record).count()
        return mark_safe('%d' %steps_count)

    class Meta:
        model = Reaction_scheme
        # add class="paleblue" to <table> tag
        attrs = {"classteps_counts": "paleblue"}
        fields =("name", "description", "updated_date", "is_possible")
        sequence = ("name", "description", "steps_count", "is_possible", "updated_date")


#Вещества реакции

class ReactionSubstTable(tables.Table):
    detail_link = tables.LinkColumn('reaction_subst_detail', orderable=False, verbose_name='Ссылка', empty_values=())
    name = tables.Column(accessor='substance.name')

    def render_brutto_formula_short_formatted(self, record):
        return mark_safe(record.brutto_formula_short_formatted)

    def render_detail_link(self, record):
        link = reverse('chemical.views.react_substance_detail', args=[record.reaction.id_reaction, record.pk])
        return make_detail_link(link)

    class Meta:
        model = Reaction_subst
        attrs = {"class": "paleblue"}
        fields = ("alias", "brutto_formula_short_formatted", "name", "detail_link")
        sequence = ("alias", "brutto_formula_short_formatted", "name", "detail_link")

#Стадии механизма
class StepsTable(tables.Table):
    detail_link = tables.LinkColumn('step_detail', orderable=False,  verbose_name='', empty_values=())
    step = tables.Column(verbose_name='Стадия', orderable=False, empty_values=())
    order_arrows = tables.LinkColumn('change_step_order', orderable=False,  verbose_name='Переместить', empty_values=())

    def render_detail_link(self,record):
        link = reverse('chemical.views.step_detail', args=[record.scheme.reaction.pk, record.scheme.pk ,record.pk])
        return make_detail_link(link)

    def render_step(self,record):
        ##TODO число стадий подсчитать и вывести
        #получаем число стадий схемы по scheme
        if record.is_revers:
            return mark_safe('left &harr right')
        else:
            return mark_safe('left &rarr right')

    def render_order_arrows(self,record):
        return mark_safe( ''' <button id="change_order" data-stepid="%d" data-curorder="%d" data-direction="up" class="btn btn-defualt" type="button">&#9650</button></br><button id="change_order" data-stepid="%d" data-curorder="%d" data-direction="down" class="btn btn-defualt" type="button">&#9660</button>'''% (record.pk, record.order, record.pk, record.order))

    class Meta:
        model = Scheme_step
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields =("name", "order", "step", "order_arrows", "detail_link")
        sequence = ("order_arrows", "order","name", "step", "detail_link")

#Эксперименты
class ExperimentTable(tables.Table):
    detail_link = tables.LinkColumn('experiment_detail', orderable=False,  verbose_name='', empty_values=())
    name = tables.LinkColumn('experiment_edit', orderable=True)

    def render_detail_link(self, record):
        link = reverse('chemical.views.experiment_detail', args=[record.reaction.id_reaction,record.pk])
        return make_detail_link(link)

    def render_name(self, record):
        link = reverse('chemical.views.experiment_edit', args=[record.reaction.id_reaction, record.pk])
        return make_name_link(link, record.name)

    class Meta:
        model = Experiment
        attrs = {"class": "paleblue"}
        fields = ("exper_date", "name", "description", "updated_date", "is_favorite")
        sequence = ("exper_date","name", "description", "is_favorite", "updated_date")


#Задачи
class ProblemTable(tables.Table):
    detail_link = tables.LinkColumn('problem_detail', orderable=False,  verbose_name='', empty_values=())
    problem_type = tables.LinkColumn('problem_edit', orderable=True)

    def render_detail_link(self, record):
        link = reverse('chemical.views.problem_detail', args=[record.reaction.id_reaction,record.pk])
        return make_detail_link(link)

    def render_problem_type(self, record):
        link = reverse('chemical.views.problem_edit', args=[record.reaction.id_reaction, record.pk])
        return make_name_link(link, record.problem_type.name)

    class Meta:
        model = Problem
        attrs = {"class": "paleblue"}
        fields = ("problem_type", "description", "created_date")
        sequence = ("problem_type", "description", "created_date")