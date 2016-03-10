# -*- coding: utf-8 -*-
import django_tables2 as tables
from chemical.models import Atom

class AtomTable(tables.Table):
    class Meta:
        model = Atom
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("atom_number", "symbol", "name", "name_latin", "atom_mass")
