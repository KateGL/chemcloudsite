# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone

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
        verbose_name_plural = ('Атомы')

# Вещество
class Substance(models.Model):
    id_substance = models.AutoField(primary_key = True, verbose_name='ИД')
    name = models.CharField(max_length=255, verbose_name='Название', unique=True)
    charge = models.SmallIntegerField (default = 0, verbose_name='Заряд')
    is_radical = models.BooleanField(default = False, verbose_name='Радикал')
    formula_brutto = models.CharField(max_length=255, default = '',verbose_name='Брутто-формула')
    formula_brutto_formatted = models.CharField(max_length=255, default = '', verbose_name='Брутто-формула')
    note = models.TextField( verbose_name='Примечание')
    #formula_mol = models.FileField()
    #formula_picture = models.ImageField()

    def consist_create(self):#создает состав вещества на основе брутто-формулы
        self.consist.all().delete()#clear consist
        atoms_dict = self.get_atom_dict()# ахтунг! говнокод
        #atoms_dict = {'H':2, 'Oh':3}
        for key, val in atoms_dict.items():
            try:
              atom = Atom.objects.get(symbol=key)
              if atom:
                co = SubstanceConsist.objects.get_or_create(atom =atom, substance = self, atom_count = val)[0]
                co.save()
                self.consist.add(co)
            except:
                return -1
            #


    def get_atom_dict(self,):# получение словаря с типа атомами
        formula_s = self.formula_brutto+' '
        atom_name =''
        atom_count = ''
        atoms_dict = {}
        for s in formula_s:
            if('A'<=s<='Z') or (s==' '):#начало названия элемента
               if atom_name !='':
                   atoms_dict.setdefault(atom_name,0)
                   if atom_count !='':
                     atoms_dict[atom_name]+= int(atom_count)
                   else:
                     atoms_dict[atom_name]+=1
               atom_name = s
               atom_count = ''
            if('a'<=s<='z'):# продолжение имени
               atom_name +=s
               atom_count = ''
            #кол-во
            if(s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                atom_count += s
        return atoms_dict

    class Meta:
        verbose_name = ('Вещество')
        verbose_name_plural = ('Вещества')

# Состав вещества
class SubstanceConsist(models.Model):
    substance = models.ForeignKey(Substance, null = False, on_delete=models.CASCADE, related_name='consist')
    atom = models.ForeignKey(Atom, null = False, on_delete=models.CASCADE, related_name='+')
    atom_count = models.DecimalField(max_digits=11, decimal_places=7,default = 0, verbose_name = 'Количество атомов')
    class Meta:
        verbose_name = ('Состав Вещества')
        verbose_name_plural = ('Составы Вещества')

# Реакция
class Reaction(models.Model):
    id_reaction      = models.AutoField(primary_key=True, verbose_name='ИД')
    name             = models.CharField(max_length=300, verbose_name='Название')
    description      = models.TextField(null = True,  verbose_name='Описание')
    is_favorite      = models.BooleanField(default = False, verbose_name='Избранное')
    is_notstationary = models.BooleanField(default = True, verbose_name='Нестационарная')
    is_isothermal    = models.BooleanField(default = True, verbose_name='Изотермическая')
    created_by       = models.TextField (verbose_name='Создал(ла)')#todo data type
    created_date     = models.DateTimeField (default=timezone.now, verbose_name='Дата создания')
    updated_by       = models.TextField (verbose_name='Обновил(а)')#todo data type
    updated_date     = models.DateTimeField (default=timezone.now, verbose_name='Дата последних изменений')
    class Meta:
      verbose_name        = ('Реакция')
      verbose_name_plural = ('Реакции')

#Схема механизма/маршрута реакции
class Reaction_scheme (models.Model):
	id_scheme    = models.AutoField (primary_key = True, verbose_name='ИД')
	reaction     = models.ForeignKey(Reaction, null = False, on_delete=models.CASCADE, related_name='+' )
	name         = models.CharField (max_length = 250, verbose_name='Название')
	description  = models.TextField (null = True, verbose_name='Описание')
	is_possible  = models.BooleanField (verbose_name='Вероятный')
	created_by   = models.TextField (verbose_name='Создал(ла)')#todo data type
	created_date = models.DateTimeField (default=timezone.now, verbose_name='Дата создания')
	updated_by   = models.TextField (verbose_name='Обновил(а)')#todo data type
	updated_date = models.DateTimeField (default=timezone.now, verbose_name='Дата обновления')
	class Meta:
		verbose_name        = ('Механизм')
		verbose_name_plural = ('Механизмы')

#Стадия схемы реакции
class Scheme_step(models.Model):
	id_step       = models.AutoField (primary_key = True, verbose_name='ИД')
	scheme        = models.ForeignKey(Reaction_scheme, null = False, on_delete=models.CASCADE, related_name='+')
	name          = models.CharField (max_length = 250, verbose_name='Обозначение')
	order         = models.IntegerField (verbose_name='№ п/п')
	is_revers     = models.BooleanField (verbose_name='Обратимая')
	note	        = models.CharField (max_length = 250, null = True, verbose_name='Примечание')
	rate_equation = models.TextField (null = True, verbose_name='Выражение для скорости')#todo data type
	class Meta:
		verbose_name        = ('Стадия схемы')
		verbose_name_plural = ('Стадии схемы')

#Вещество в стадии схемы реакции
class Step_subst(models.Model):
	#первичный ключ, только для возможности django создать ключ
	id_stepsubst = models.AutoField (primary_key = True, verbose_name='ИД')
	step         = models.ForeignKey(Scheme_step, null = False, on_delete=models.CASCADE, related_name='+')
	#subst       = models.ForeignKey(Reaction_subst, null = False, on_delete=models.CASCADE, related_name='+')
	substance    = models.IntegerField()
	position     =	models.IntegerField(verbose_name='Позиция вещества в стадии')
	stoich_koef  =	models.DecimalField(max_digits=6, decimal_places=3,default = 0, verbose_name='Стехиометрический коэффициент')
	class Meta:
		unique_together     = ('step', 'substance')		
		verbose_name        = ('Вещество стадии')
		verbose_name_plural = ('Вещества стадии')

#Эксперименты
class Experiment (models.Model):
    id_experiment    = models.AutoField (primary_key = True, verbose_name='ИД')
    reaction      = models.ForeignKey(Reaction)
    name         = models.CharField (max_length = 250, verbose_name='Название')
    description  = models.TextField (null = True, verbose_name='Описание')
    exper_date = models.DateTimeField (default=timezone.now, verbose_name='Дата проведения')
    is_favorite  = models.BooleanField(default = False, verbose_name='Избранное')
    created_by   = models.TextField (verbose_name='Создал(ла)')#todo data type
    created_date = models.DateTimeField (default=timezone.now, verbose_name='Дата создания')
	#updated_by   = models.TextField (verbose_name='Обновил(а)')#todo data type
	#updated_date = models.DateTimeField (default=timezone.now, verbose_name='Дата обновления')
    class Meta:
      verbose_name = ('Эксперимент')
      verbose_name_plural = ('Эксперименты')






