# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from django.utils.safestring import mark_safe
from django.utils.html import escape

from chemical.models import Atom, Substance, Reaction

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

    def render_detail_link(self,record):
        return mark_safe( ''' <a href="/chemical/substance/%d/detail">Детали</a>'''%record.pk)

    class Meta:
        model = Substance
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("name", "formula_brutto", "charge", "is_radical")

#Реакции
class ReactionTable(tables.Table):
    detail_link = tables.LinkColumn('reaction_detail', args=[A('pk')], orderable=False,  verbose_name='Ссылка', empty_values=())

    def render_detail_link(self,record):
        return mark_safe( ''' <a href="/chemical/reaction/%d/detail">Детали</a>'''%record.pk)

    class Meta:
        model = Reaction
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("id_reaction", "name", "is_favorite", "description")

#Эксперименты