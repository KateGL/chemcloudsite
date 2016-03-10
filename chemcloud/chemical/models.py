# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Атом
class Atom(models.Model): 
    atom_number = models.IntegerField(primary_key = True)
    symbol = models.CharField(max_length=3, unique=True)
    atom_mass = models.DecimalField(max_digits=11, decimal_places=7)
    name = models.CharField(max_length=100, unique=True)
    name_latin = models.CharField(max_length=100, unique=True) 
 
# Вещество
class Substance(models.Model): 
    id_substance = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255)
    charge = models.SmallIntegerField (default = 0)
    is_radical = models.BooleanField(default = False)
    formula_brutto = models.CharField(max_length=255)
    note = models.TextField()
    #formula_mol = models.FileField()
    #formula_picture = models.ImageField()

# Состав вещества

# Реакция
class Reaction(models.Model):
    id_reaction = models.AutoField(primary_key = True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    is_favorite = models.BooleanField(default = False)
    is_stationary = models.BooleanField(default = True)
    is_isothermal = models.BooleanField(default = True)
    

#

#






 
