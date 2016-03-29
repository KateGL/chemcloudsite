# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from django.utils.safestring import mark_safe
#from django.utils.html import escape
from table import Table
from table.columns import Column, LinkColumn

from chemical.models import Atom, Substance, Reaction, SubstanceConsist, Reaction_scheme,Experiment
from chemical.models import Scheme_step, Step_subst

class AtomTable(tables.Table):
    detail_link = tables.LinkColumn('atom_detail', args=[A('pk')], orderable=False,  verbose_name='Ссылка', empty_values=())

    def render_detail_link(self,record):
        return mark_safe( ''' <a href="/chemical/atom/%d/detail">Детали</a>'''%record.pk)

    class Meta:
        model = Atom
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("atom_number", "symbol", "name", "name_latin", "atom_mass")

class SubstanceTable(tables.Table):
    detail_link = tables.LinkColumn('substance_detail', args=[A('pk')], orderable=False,  verbose_name='Ссылка', empty_values=())

    def render_formula_brutto_formatted(self,record):
        return mark_safe(record.formula_brutto_formatted)

    def render_detail_link(self,record):
        return mark_safe( ''' <a href="/chemical/substance/%d/detail">Детали</a>'''%record.pk)

    class Meta:
        model = Substance
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields =("name", "formula_brutto_formatted", "charge", "is_radical")
        sequence = ("name", "formula_brutto_formatted", "charge", "is_radical")

class ConsistTable(tables.Table):
    atom_symbol = tables.Column(accessor='atom.symbol')
    class Meta:
        model = SubstanceConsist
        attrs = {"class": "paleblue"}
        fields =("atom_symbol", "atom_count")
        sequence = ("atom_symbol", "atom_count")


#Реакции
class ReactionTable(tables.Table):
    detail_link = tables.LinkColumn('reaction_detail', args=[A('pk')], orderable=False,  verbose_name='Ссылка', empty_values=())

    def render_detail_link(self,record):
        return mark_safe( ''' <a href="/chemical/reaction/%d/detail">Детали</a>'''%record.pk)

    class Meta:
        model = Reaction
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields =("name", "is_favorite", "description", "updated_date")
        sequence = ("is_favorite", "name",  "description", "updated_date")

#Механизмы
class MechanizmTable(tables.Table):
	#args=[A('pk')], и без этого работает	
	detail_link = tables.LinkColumn('scheme_detail', orderable=False,  verbose_name='', empty_values=())
	name = tables.LinkColumn('scheme_edit', orderable=True)
	#для колонки с пустым значением render вызывается, если стоит empty_values=()) 	
	steps_count = tables.Column(verbose_name='Число стадий', orderable=False, empty_values=())

	def render_detail_link(self,record):
		#return mark_safe( ''' <a href="/chemical/reaction/%d/scheme/%d/detail">Детали</a>'''% (record.reaction.id_reaction, record.pk))
		return mark_safe( ''' <a href="/chemical/reaction/%d/scheme/%d/detail">Детали</a>'''% (record.reaction.id_reaction, record.pk))

	def render_name(self,record):
		return mark_safe( ''' <a href="/chemical/reaction/%d/scheme/%d/edit">%s</a>'''% (record.reaction.id_reaction, record.pk, record.name))

	def render_steps_count(self,record):
		#TODO число стадий подсчитать и вывести
		#получаем число стадий схемы по scheme
		steps_count = Scheme_step.objects.filter(scheme = record).count()
		return mark_safe('%d' %steps_count)

	class Meta:
		model = Reaction_scheme
		# add class="paleblue" to <table> tag
		attrs = {"class": "paleblue"}
		fields =("name", "description", "updated_date", "is_possible")
		sequence = ("name", "description", "steps_count", "is_possible", "updated_date")

#Стадии механизма
#tables.Table
class StepsTable(tables.Table):
	detail_link = tables.LinkColumn('step_detail', orderable=False,  verbose_name='', empty_values=())
	step = tables.Column(verbose_name='Стадия', orderable=False, empty_values=())
	order_arrows = tables.LinkColumn('change_step_order', orderable=False,  verbose_name='Переместить', empty_values=())

# &#9660 &#9650
	def render_detail_link(self,record):
		return mark_safe( ''' <a href="/chemical/step/%d/detail">Детали</a> '''% (record.pk))

	def render_order_arrows(self,record):
		return mark_safe( ''' <button id="change_order" data-stepid="%d" data-curorder="%d" data-direction="up" class="btn btn-defualt" type="button">&#9650</button></br><button id="change_order" data-stepid="%d" data-curorder="%d" data-direction="down" class="btn btn-defualt" type="button">&#9660</button>'''% (record.pk, record.order, record.pk, record.order))

	def render_step(self,record):
		#TODO число стадий подсчитать и вывести
		#получаем число стадий схемы по scheme
		if record.is_revers:
			return mark_safe('left &harr right')
		else:
			return mark_safe('left &rarr right')			

	class Meta:
		model = Scheme_step
		ajax  = True
		# add class="paleblue" to <table> tag
		attrs = {"class": "paleblue"}
		fields =("name", "order", "step", "order_arrows", "detail_link")
		sequence = ("order_arrows", "order","name", "step", "detail_link")


#Эксперименты
class ExperimentTable(tables.Table):
	detail_link = tables.LinkColumn('experiment_detail', orderable=False,  verbose_name='', empty_values=())
	name = tables.LinkColumn('experiment_edit', orderable=True)
	#для колонки с пустым значением render вызывается, если стоит empty_values=()) 	
	#steps_count = tables.Column(verbose_name='Число стадий', orderable=False, empty_values=())

	def render_detail_link(self,record):
		return mark_safe( ''' <a href="/chemical/experiment/%d/detail">Детали</a>'''% (record.pk))

	def render_name(self,record):
		return mark_safe( ''' <a href="/chemical/reaction/%d/experiment/%d/edit">%s</a>'''% (record.reaction.id_reaction, record.pk, record.name))

	#def render_steps_count(self,record):
	#	#TODO число стадий подсчитать и вывести
	#	#получаем число стадий схемы по scheme
	#	steps_count = Scheme_step.objects.filter(scheme = record).count()
	#	return mark_safe('%d' %steps_count)

	class Meta:
		model = Experiment
		attrs = {"class": "paleblue"}
		fields =("name", "description", "updated_date", "is_favorite")
		sequence = ("name", "description",  "is_favorite", "updated_date")
