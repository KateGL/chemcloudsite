# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Атом
class Atom(models.Model): 
    atom_number = models.IntegerField(primary_key = True, verbose_name='Атомный номер')
    symbol = models.CharField(max_length=3, unique=True, verbose_name='Обозначение')
    atom_mass = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Атомная масса')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название (рус)')
    name_latin = models.CharField(max_length=100, unique=True, verbose_name='Название (лат)') 
    class Meta:
        verbose_name = ('Атом')
        verbose_name_plural = ('Атомов')
 
# Вещество
class Substance(models.Model): 
    id_substance = models.AutoField(primary_key = True, verbose_name='ИД')
    name = models.CharField(max_length=255, verbose_name='Название')
    charge = models.SmallIntegerField (default = 0, verbose_name='Заряд')
    is_radical = models.BooleanField(default = False, verbose_name='Радикал')
    formula_brutto = models.CharField(max_length=255, verbose_name='Брутто-формула')
    note = models.TextField( verbose_name='Примечание')
    #formula_mol = models.FileField()
    #formula_picture = models.ImageField()
    class Meta:
        verbose_name = ('Вещество')
        verbose_name_plural = ('Веществ')

# Состав вещества

# Реакция
class Reaction(models.Model):
    id_reaction = models.AutoField(primary_key = True, verbose_name='ИД')
    name = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField( verbose_name='Описание')
    is_favorite = models.BooleanField(default = False, verbose_name='Избранное')
    is_stationary = models.BooleanField(default = True, verbose_name='Стационарная')
    is_isothermal = models.BooleanField(default = True, verbose_name='Изотермическая')
    class Meta:
        verbose_name = ('Реакция')
        verbose_name_plural = ('Реакций')   

#

#






 
