# -*- coding: utf-8 -*-
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import numpy as np

# Create your models here.

from .utils import decorate_formula


# Атом
class Dict_atom(models.Model):
    atom_number = models.IntegerField(primary_key=True, verbose_name='Атомный номер')
    symbol = models.CharField(max_length=3, unique=True, verbose_name='Обозначение')
    atom_mass = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Атомная масса')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название (рус)')
    name_latin = models.CharField(max_length=100, unique=True, verbose_name='Название (лат)')

    class Meta:
        verbose_name = ('Атом')
        verbose_name_plural = ('Атомы')
        ordering = ["atom_number"]

    def __unicode__(self):
        return self.symbol


# Вещество
class Substance(models.Model):
    id_substance = models.AutoField(primary_key=True, verbose_name='ИД')
    name = models.CharField(max_length=255, verbose_name='Название', unique=True)
    charge = models.SmallIntegerField(default=0, verbose_name='Заряд')
    is_radical = models.BooleanField(default=False, verbose_name='Радикал')
    formula_brutto = models.CharField(max_length=255, default='', verbose_name='Брутто-формула')
    formula_brutto_formatted = models.CharField(max_length=255, default='', verbose_name='Брутто-формула')
    note = models.TextField(verbose_name='Примечание')
    #Вспомогательное поле для поиска изомеров
    consist_as_string = models.CharField(max_length=255, default='', verbose_name='Состав вещества строкой')
    #formula_mol = models.FileField()
    #formula_picture = models.ImageField()

    class Meta:
        verbose_name = ('Вещество')
        verbose_name_plural = ('Вещества')

    def __unicode__(self):
        return self.name

    def after_create(self):
        self.formula_brutto_formatted = decorate_formula(self.formula_brutto)
        self.consist_create()

    def consist_create(self):  # создает состав вещества на основе брутто-формулы
        self.consist.all().delete()  # clear consist
        atoms_dict = get_atom_dict(self.formula_brutto)  # ахтунг! говнокод
        self.consist_as_string = consist_dict_to_string(atoms_dict)

        #atoms_dict = {'H':2, 'Oh':3}
        for key, val in atoms_dict.items():
            try:
                atom = Dict_atom.objects.get(symbol=key)
                if atom:
                    co = Substance_consist.objects.get_or_create(atom=atom, substance=self, atom_count=val)[0]
                    co.save()
                    self.consist.add(co)
            except:
                return -1


# Состав вещества
def get_atom_dict(formula_brutto):  # получение словаря с типа атомами
    formula_s = formula_brutto.strip(' \t\n\r') + ' '
    atom_name = ''
    atom_count = ''
    atoms_dict = {}
    for s in formula_s:
        if('A' <= s <= 'Z') or (s == ' '):  # начало названия элемента
            if atom_name != '':
                atoms_dict.setdefault(atom_name, 0)
                if atom_count != '':
                    atoms_dict[atom_name] += Decimal(atom_count)
                else:
                    atoms_dict[atom_name] += Decimal(1)
            atom_name = s
            atom_count = ''
        if('a' <= s <= 'z'):  # продолжение имени
            atom_name += s
            atom_count = ''
        #кол-во
        if(s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']):
            atom_count += s
        if(s == ','):
            atom_count += '.'
    return atoms_dict


def consist_dict_to_string(mydict):
    as_str = ''
    for key in sorted(mydict):
        key_as_str = ''
        if mydict[key] != 1:  #не пишем в состав 1
            key_as_str = str(mydict[key].normalize())
        as_str += key + key_as_str
    return as_str


def consist_to_string(formula_brutto):
    atoms_dict = get_atom_dict(formula_brutto)
    return consist_dict_to_string(atoms_dict)


class Substance_consist(models.Model):
    id_subst_consist = models.AutoField(primary_key=True, verbose_name='ИД')
    substance = models.ForeignKey(Substance, null=False, on_delete=models.CASCADE, related_name='consist')
    atom = models.ForeignKey(Dict_atom, null=False, on_delete=models.CASCADE, related_name='+',default=0)
    atom_count = models.DecimalField(max_digits=11, decimal_places=7, default=0, verbose_name='Кол-во атомов')

    class Meta:
        verbose_name = ('Состав Вещества')
        verbose_name_plural = ('Составы Вещества')
        unique_together = (('substance', 'atom'), )

    def __unicode__(self):
        return self.substance.name


# Реакция
class Reaction(models.Model):
    id_reaction      = models.AutoField(primary_key=True, verbose_name='ИД')
    name             = models.CharField(max_length=300, verbose_name='Название')
    description      = models.TextField(blank = True,  verbose_name='Описание')
    is_favorite      = models.BooleanField(default = False, verbose_name='Избранное')
    #is_notstationary = models.BooleanField(default = True, verbose_name='Нестационарная')
    #is_isothermal    = models.BooleanField(default = True, verbose_name='Изотермическая')
    created_by       = models.TextField (verbose_name='Создал(ла)')#todo data type
    created_date     = models.DateTimeField (default=timezone.now, verbose_name='Дата создания')
    updated_by       = models.TextField (verbose_name='Обновил(а)')#todo data type
    updated_date     = models.DateTimeField (default=timezone.now, verbose_name='Дата последних изменений')

    def __unicode__ (self):
        return self.name

    def add_owner(self, user_owner):
        user_reaction = User_reaction.objects.get_or_create(user =user_owner, reaction = self, is_owner = True)[0]
        user_reaction.save()
        self.users.add(user_reaction)

    def share_to_user(self, user_new, is_owner_new):
        user_reaction = User_reaction.objects.get_or_create(user=user_new, reaction=self, is_owner=is_owner_new)[0]
        user_reaction.save()
        self.users.add(user_reaction)

    class Meta:
        verbose_name        = ('Реакция')
        verbose_name_plural = ('Реакции')

#Схема механизма/маршрута реакции
class Reaction_scheme (models.Model):
    id_scheme    = models.AutoField (primary_key = True, verbose_name='ИД')
    reaction     = models.ForeignKey(Reaction, null = False, on_delete=models.CASCADE, related_name='schemes' )
    name         = models.CharField (max_length = 250, verbose_name='Название')
    description  = models.TextField (blank = True, verbose_name='Описание')
    is_possible  = models.BooleanField (verbose_name='Вероятный')
    created_by   = models.TextField (verbose_name='Создал(ла)')#todo data type
    created_date = models.DateTimeField (default=timezone.now, verbose_name='Дата создания')
    updated_by   = models.TextField (verbose_name='Обновил(а)')#todo data type
    updated_date = models.DateTimeField (default=timezone.now, verbose_name='Дата обновления')

    def __unicode__ (self):
        return self.name

    def create_new_emptystep(self):
        try:
            steps = self.steps
            new_order = steps.count() + 1
            empty_step = Scheme_step.objects.get_or_create( scheme = self, order = new_order, is_revers = False, is_good_balance = False )[0]
            empty_step.save()
            self.steps.add(empty_step)
        except:
            return -1
        return empty_step

    def check_scheme_balance(self, error_list):
        try:
            error_str=''
            G_mtrx = self.get_scheme_G_mtrx()
            if G_mtrx == []:
                error_str = 'Ошибка в получении матрицы G'
                error_list.append(error_str)
                return False
            A_mtrx_dict = self.get_scheme_A_mtrx()
            if A_mtrx_dict == []:
                error_str = 'Ошибка в получении матрицы A. Возможно, ни одному псевдониму вещества реакции не сопоставлено вещество из справочника'
                error_list.append(error_str)
                return False
            A_mtrx = A_mtrx_dict[0]
            atoms_list = A_mtrx_dict[1]
            elem_count = len(atoms_list)
            stage_count = len(G_mtrx)
            GA = np.dot(G_mtrx, A_mtrx)
            GA_zero = np.zeros((stage_count, elem_count))
            b = np.array_equal(GA, GA_zero)
            #b = not b
            if not b:
                i = 0
                steps = self.steps.all()
                error_str = '';
                while i < stage_count:
                    error_str_temp = 'Стадия ' + str(steps[i])
                    k = 0
                    bool_temp = True
                    j = 0
                    error_str_temp = error_str_temp + '. Не соблюдается баланс по элементу(-ам): '
                    while j < elem_count:
                        elem = GA[i][j]
                        if elem!=0.0:
                            if k != 0:
                                error_str_temp = error_str_temp + ', '
                            error_str_temp = error_str_temp + str(atoms_list[j])
                            k = 1
                        j = j+1
                    i = i+1
                    if k!=0:
                        error_str = error_str+error_str_temp + '. '
                        bool_temp = False
                    #steps[i].is_good_balance = bool_temp по идее перезапись состояния баланса осуществляется при сохранении стадии
                    #steps_list[i].save()
                error_list.append(error_str)
            return b
        except:
            error_str = 'Неизвестная ошибка по исключению'
            error_list.append(error_str)
            return False

    def get_scheme_subst_all(self):
        try:
            steps = self.steps.all()
            substs_list = []
            for step_i in steps:
                substs = step_i.scheme_step_substs.all()
                for subst_j in substs:
                    substs_list = substs_list + [subst_j.reac_substance]
            #удаляем дубликаты в списке атомов
            substs_list = list(set(substs_list))
            return substs_list
        except:
            return []

    def get_scheme_G_mtrx(self):
        try:
            steps = self.steps.all()
            substs_list = self.get_scheme_subst_all()
            subst_count = len(substs_list)
            stage_count = steps.count()
            if subst_count == 0 or stage_count == 0:
                return []
            G_mtrx = np.zeros((stage_count,subst_count))
            i = -1
            for step_i in steps:
                i = i+1
                j = -1
                substs = step_i.scheme_step_substs.all()
                for subst_j in substs:
                    j = j+1
                    pos_subst = substs_list.index(subst_j.reac_substance)
                    if pos_subst < 0:
                        error_str = 'Этого не может быть, потому что этого быть не может'
                        return -1
                    G_mtrx[i][pos_subst] =  subst_j.stoich_koef
            return G_mtrx
        except:
            return []

    def get_scheme_A_mtrx(self):
        try:
            substs_list = self.get_scheme_subst_all()
            subst_count = len(substs_list)
            if subst_count == 0:
                return []
            atoms_list = []
            atoms_count_list = []
            i = 0
            for subst_i in substs_list:
                if subst_i.substance is not None:                
                    subst_consist_list = subst_i.substance.consist.all()
                    list_temp = []
                    for subst_consist in subst_consist_list:
                        atom_j = subst_consist.atom
                        atoms_list = atoms_list + [atom_j.symbol]
                        list_temp2 = [atom_j.symbol, subst_consist.atom_count]
                        list_temp = list_temp + [list_temp2]
                    atoms_count_list = atoms_count_list + [list_temp]
                i = i+1
            #удаляем дубликаты в списке атомов
            atoms_list = list(set(atoms_list))
            elem_count = len(atoms_list)
            if subst_count == 0 or elem_count == 0:
                return []
            #строки - число атомов хим элемента в веществе, стоблцы - хим.элементы
            A_mtrx = np.zeros((subst_count, elem_count))
            i = 0
            for elem_i in atoms_count_list : #бежим по веществам
                for elem_j in elem_i: #бежим по атомам
                    symbol = elem_j[0]
                    atom_cnt = elem_j[1]
                    pos_symbol = atoms_list.index(symbol)
                    if pos_symbol < 0:
                        error_str = 'Этого не может быть, потому что этого быть не может'
                        return []
                    A_mtrx[i][pos_symbol] = A_mtrx[i][pos_symbol] + float(atom_cnt)
                i = i+1
            result_dict = [A_mtrx, atoms_list]
            return result_dict
        except:
            return []

    class Meta:
        ordering            = ["updated_date"]
        verbose_name        = ('Механизм')
        verbose_name_plural = ('Механизмы')

#Стадия схемы реакции
class Scheme_step(models.Model):
    id_step       = models.AutoField (primary_key = True, verbose_name='ИД')
    scheme        = models.ForeignKey(Reaction_scheme, null = False, on_delete=models.CASCADE, related_name='steps')
    name          = models.CharField (max_length = 250, blank = True, verbose_name='Обозначение')
    order         = models.IntegerField (verbose_name='№ п/п')
    is_revers     = models.BooleanField (verbose_name='Обратимая')
    is_good_balance   = models.BooleanField (verbose_name='Баланс', null = False, default = False)
    note            = models.CharField (max_length = 250, blank = True, verbose_name='Примечание')
    rate_equation = models.TextField (blank= True, verbose_name='Выражение для скорости')#todo data type
    def __unicode__ (self):
        title = str(self.order)
        if self.name:
            str_name = self.name.strip(' ')
            title = title + '{'+str_name+'}'
        return title

    def get_leftPart_of_step(self):
        s_substs_arr = self.scheme_step_substs.all()
        left = ''
        i = 1
        cnt = s_substs_arr.count()
        for s_subst in s_substs_arr:
            if s_subst.stoich_koef < 0:
                if i != 1:
                    left = left + '+'
                alias = s_subst.reac_substance.alias
                positiv_koef = -1*s_subst.stoich_koef
                str_koef = ''
                if positiv_koef != 1.0:
                    str_koef = '{0:.3g}'.format(positiv_koef)#str(positiv_koef)
                left = left + str_koef+alias

            i = i+1
        return left

    def get_rightPart_of_step(self):
        s_substs_arr = self.scheme_step_substs.all()
        i = 1
        cnt = s_substs_arr.count()
        right = ''
        for s_subst in s_substs_arr:
            if s_subst.stoich_koef > 0:
                alias = s_subst.reac_substance.alias
                positiv_koef = s_subst.stoich_koef
                str_koef = ''
                if positiv_koef != 1.0:
                    str_koef = '{0:.3g}'.format(positiv_koef)#str(positiv_koef)
                right = right + str_koef+alias
                if i < cnt:
                    right = right + '+'
            i = i+1
        return right

    def generate_step_from_str(self, data_list):
        try:
            self.scheme_step_substs.all().delete()
            for element in data_list:
                position_temp   = element[0]
                steh_koef_temp  = element[1]
                reac_subst_temp = element[2]
                step_subst = Scheme_step_subst.objects.get_or_create( step = self, reac_substance = reac_subst_temp, position = position_temp, stoich_koef =steh_koef_temp )[0]
                step_subst.save()
                self.scheme_step_substs.add(step_subst)
        except:
            return False
        return True

    def check_step_balance(self, error_list): #если нужна передача по ссылке, то передаем лист
        try:
            error_str=''
            step_substs = self.scheme_step_substs.all()
            atoms_list = []
            atoms_count_list = []
            subst_count = step_substs.count()
            G_coll = np.zeros((1,subst_count))
            i = 0
            for subst_i in step_substs:
                G_coll[0][i] =  subst_i.stoich_koef
                if subst_i.reac_substance.substance is None:
                    error_str = 'Невозможно проверить баланс стадии. Псевдониму '+str(subst_i.reac_substance.alias)+' не сопоставлено вещество реакции'
                    error_list.append(error_str) 
                    return False
                subst_consist_list = subst_i.reac_substance.substance.consist.all()
                list_temp = []
                for subst_consist in subst_consist_list:
                    atom_j = subst_consist.atom
                    atoms_list = atoms_list + [atom_j.symbol]
                    list_temp2 = [atom_j.symbol, subst_consist.atom_count]
                    list_temp = list_temp + [list_temp2]
                atoms_count_list = atoms_count_list + [list_temp]
                i = i+1
            #удаляем дубликаты в списке атомов
            atoms_list = list(set(atoms_list))
            elem_count = len(atoms_list)
            #строки - число атомов хим элемента в веществе, стоблцы - хим.элементы
            A_mtrx = np.zeros((subst_count, elem_count))
            i = 0
            for elem_i in atoms_count_list : #бежим по веществам
                for elem_j in elem_i: #бежим по атомам
                    symbol = elem_j[0]
                    atom_cnt = elem_j[1]
                    pos_symbol = atoms_list.index(symbol)
                    if pos_symbol < 0:
                        error_str = 'Этого не может быть, потому что этого быть не может'
                        error_list.append(error_str)
                        return False
                    A_mtrx[i][pos_symbol] = A_mtrx[i][pos_symbol] + float(atom_cnt)
                i = i+1
            GA = np.dot(G_coll, A_mtrx)
            GA_zero = np.zeros((1, elem_count))
            b = np.array_equal(GA, GA_zero)
            #b = not b
            if not b:
                i = 0
                k=0
                error_str = 'Не соблюдается баланс по элементу(-ам): '
                while i < elem_count:
                    elem = GA[0][i]
                    if elem!=0.0:
                        if k != 0:
                            error_str = error_str + ', '
                        error_str = error_str + str(atoms_list[i])
                        k = 1
                    i = i+1
                error_list.append(error_str)
            self.is_good_balance = b
            self.save()
            return b
        except:
            error_str = 'Неизвестная ошибка по исключению'
            error_list.append(error_str)
            return False

    class Meta:
        ordering            = ["order"]
        verbose_name        = ('Стадия схемы')##Механизма или Схемы??? я путаюсь Рита: это общая модель схемы и механизма и маршрута. ПО крайней мере по вертабело. Пока так. Дойдем до маршрутов - будет видно
        verbose_name_plural = ('Стадии схемы')


#Вещества реакции
class Reaction_subst(models.Model):
    id_react_subst = models.AutoField(primary_key=True, verbose_name='ИД')
    reaction = models.ForeignKey(Reaction, null=False, on_delete=models.CASCADE, related_name='substances')
    substance = models.ForeignKey(Substance, null=True, blank=True, default=None, on_delete=models.PROTECT, related_name='+')
    alias = models.CharField(max_length=250, verbose_name='Псевдоним', null=False)
    brutto_formula_short = models.CharField(max_length=250, verbose_name='Краткая брутто-формула')
    brutto_formula_short_formatted = models.CharField(max_length=250, verbose_name='Краткая брутто-формула')
    note = models.TextField(blank=True, verbose_name='Примечание')

    def __unicode__(self):
        return self.alias

    def after_create(self):
        if self.substance:
            self.brutto_formula_short_formatted = decorate_formula(self.brutto_formula_short)
        else:
            self.brutto_formula_short_formatted = self.brutto_formula_short

    class Meta:
        ordering = ["id_react_subst", "reaction"]
        verbose_name = ('Вещество реакции')
        verbose_name_plural = ('Вещества реакции')
        unique_together = (('reaction', 'alias'))


#Вещество в стадии схемы реакции
class Scheme_step_subst(models.Model):
    #первичный ключ, только для возможности django создать ключ
    id_step = models.AutoField (primary_key = True, verbose_name='ИД')
    step         = models.ForeignKey(Scheme_step, null = False, on_delete=models.CASCADE, related_name='scheme_step_substs')
    reac_substance    = models.ForeignKey(Reaction_subst, null = False, on_delete=models.CASCADE, related_name='+')
    position     =    models.IntegerField(verbose_name='Позиция вещества в стадии')
    stoich_koef  =    models.DecimalField(max_digits=6, decimal_places=3,default = 0, verbose_name='Стехиометрический коэффициент')

    #def __unicode__ (self):
        #return self.id_step

    class Meta:
        ordering            = ["id_step", "position"]
        unique_together     = ('step', 'reac_substance')
        verbose_name        = ('Вещество стадии')
        verbose_name_plural = ('Вещества стадии')


#Права пользователя
#Считаем, что если есть запист в этой таблице, то Пользователь имеет право на чтение Реакции
#Если is_owner == True то пользователь может редактировать реакцию и расшаривать ее другим Пользователям
class User_reaction(models.Model):
    id_user_reaction = models.AutoField (primary_key = True, verbose_name='ИД')
    reaction = models.ForeignKey(Reaction, related_name='users', verbose_name='Реакция', null = False,on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reactions', verbose_name='Пользователь', null = False,on_delete=models.CASCADE)
    is_owner = models.BooleanField(default = False, verbose_name='Владелец')

    class Meta:
      verbose_name = ('Доступ к Реакции')
      verbose_name_plural = ('Права на Реакции ')
      unique_together = ('reaction', 'user')

#Синонимы вещества
class Substance_synonym (models.Model):
    id_subst_synonym = models.AutoField (primary_key = True, verbose_name='ИД')
    substance = models.ForeignKey(Substance, null = True, on_delete=models.PROTECT, related_name='synonyms', verbose_name='Вещество')
    name = models.CharField (max_length = 250, verbose_name='Название')

    def __unicode__ (self):
        return self.name

    class Meta:
        ordering            = ["name"]
        verbose_name        = ('Синоним вещества')
        verbose_name_plural = ('Синонимы вещества')


#Тэги реакции
class Reaction_tag(models.Model):
    id_reaction_tag = models.AutoField (primary_key = True, verbose_name='ИД')
    reaction = models.ForeignKey(Reaction, null = True, on_delete=models.PROTECT, related_name='reac_tags', verbose_name='Реакция')
    tag = models.CharField (max_length = 250, verbose_name='Тэг')

    def __unicode__ (self):
        return self.tag

    class Meta:
      ordering = ["tag"]
      verbose_name = ('Тэг реакции')
      verbose_name_plural = ('Тэги реакции')


# Свойства
class Dict_feature(models.Model):
    id_feature = models.IntegerField(primary_key = True, verbose_name='Номер свойства')
    name = models.CharField(max_length=250, unique=True, verbose_name='Название свойства')

    def __unicode__ (self):
        return self.name

    class Meta:
        verbose_name = ('Свойство')
        verbose_name_plural = ('Свойства')
        ordering = ["id_feature"]


#Свойства реакции
class Reaction_feature(models.Model):
    id_reaction_feature = models.AutoField (primary_key = True, verbose_name='ИД')
    reaction = models.ForeignKey(Reaction, null = True, on_delete=models.PROTECT, related_name='reac_features', verbose_name='Реакция')
    feature = models.ForeignKey(Dict_feature, null = True, on_delete=models.PROTECT, related_name='+',default=0, verbose_name='Свойство')

    class Meta:
      verbose_name = ('Свойство реакции')
      verbose_name_plural = ('Свойства реакции')
      ordering = ["id_reaction_feature"]


# Функции модели
class Dict_model_function(models.Model):
    id_func = models.IntegerField(primary_key = True, verbose_name='Номер функции модели')
    name = models.CharField(max_length=250, unique=True, verbose_name='Название функции модели')
    symbol = models.CharField(max_length=10, unique=True, verbose_name='Символ')

    def __unicode__ (self):
        return self.name

    class Meta:
        verbose_name = ('Функция модели')
        verbose_name_plural = ('Функции модели')
        ordering = ["id_func"]

# Аргументы модели
class Dict_model_argument(models.Model):
    id_arg = models.IntegerField(primary_key = True, verbose_name='Номер аргумента модели')
    name = models.CharField(max_length=250, unique=True, verbose_name='Название аргумента модели')
    symbol = models.CharField(max_length=10, unique=True, verbose_name='Символ')

    def __unicode__ (self):
        return self.name

    class Meta:
        verbose_name = ('Аргумент модели')
        verbose_name_plural = ('Аргументы модели')
        ordering = ["id_arg"]

# Единицы измерения
class Dict_measure_unit(models.Model):
    id_unit = models.IntegerField(primary_key = True, verbose_name='Номер единицы измерения')
    code = models.CharField(max_length=250, verbose_name='Обозначение')
    name = models.CharField(max_length=250, unique=True, verbose_name='Название единицы измерения')
    is_si = models.BooleanField(default = True, verbose_name='СИ')
    multiplier = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Множитель')
    unit_si = models.ForeignKey('self', null = True, blank=True, related_name='+' )


    def __unicode__ (self):
        return self.name

    class Meta:
        verbose_name = ('Единица измерения')
        verbose_name_plural = ('Единицы измерения')
        ordering = ["id_unit"]


#Серия для Экспериментов
class Exper_serie (models.Model):
    id_serie = models.AutoField(primary_key=True, verbose_name='ИД')
    reaction = models.ForeignKey(Reaction, null=False, on_delete=models.CASCADE, related_name='exper_series')
    name = models.CharField(max_length=250, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_archive = models.BooleanField(default=False, verbose_name='Поместить в Архив')

    class Meta:
        verbose_name = ('Серия экспериментов')
        verbose_name_plural = ('Серии экспериментов')

    def __unicode__(self):
        return self.name


#Эксперименты
class Experiment (models.Model):
    id_experiment    = models.AutoField (primary_key = True, verbose_name='ИД')
    reaction     = models.ForeignKey(Reaction, null = False, on_delete=models.CASCADE, related_name='experiments' )
    argument_measure = models.ForeignKey(Dict_measure_unit, null = True, on_delete=models.PROTECT, related_name='+',verbose_name='Единица измерения аргумента',default=0)
    function_measure = models.ForeignKey(Dict_measure_unit, null = True, on_delete=models.PROTECT, related_name='+',verbose_name='Единица измерения функции',default=0)
    init_function_measure = models.ForeignKey(Dict_measure_unit, null = True, on_delete=models.PROTECT, related_name='+',verbose_name='Единица измерения начальных концентраций',default=0)
    description  = models.TextField (blank = True, verbose_name='Описание')
    func = models.ForeignKey(Dict_model_function, null = True, on_delete=models.PROTECT, related_name='+',verbose_name='Функция',default=0)
    arg = models.ForeignKey(Dict_model_argument, null = True, on_delete=models.PROTECT, related_name='+',verbose_name='Аргумент',default=0)
    exper_date = models.DateTimeField (default=timezone.now, verbose_name='Дата проведения')
    updated_by   = models.TextField (verbose_name='Обновил(а)')
    updated_date = models.DateTimeField (default=timezone.now, verbose_name='Дата обновления')
    is_favorite  = models.BooleanField(default = False, verbose_name='Избранное')
    exper_serie = models.ForeignKey(Exper_serie, null=True, blank=True, default=None, on_delete=models.PROTECT,
        related_name='experiments', verbose_name='Серия')

    created_date = models.DateTimeField (default=timezone.now, verbose_name='Дата создания')
    name         = models.CharField (max_length = 250, verbose_name='Название')
    created_by   = models.TextField (verbose_name='Создал(ла)')#todo data type

    def __unicode__ (self):
        return self.name

    class Meta:
      ordering            = ["id_experiment"]
      verbose_name = ('Эксперимент')
      verbose_name_plural = ('Эксперименты')

class Dict_subst_role (models.Model):
    id_role = models.IntegerField (primary_key = True, verbose_name='ИД')
    name         = models.CharField (max_length = 250, verbose_name='Название')

    def __unicode__ (self):
        return self.name

    class Meta:
      ordering            = ["id_role"]
      verbose_name = ('Роль вещества в механизме')
      verbose_name_plural = ('Роли вещества в механизме')

class Dict_exper_param (models.Model):
    id_experparam = models.IntegerField(primary_key = True, verbose_name='ИД')
    name         = models.CharField (max_length = 250, verbose_name='Название')

    def __unicode__ (self):
        return self.name

    class Meta:
      ordering            = ["id_experparam"]
      verbose_name = ('Дополнительные данные эксперимента')
      verbose_name_plural = ('Дополнительные данные эксперимента')

class Dict_exper_subst_param (models.Model):
    id_expersubstparam = models.IntegerField (primary_key = True, verbose_name='ИД')
    name         = models.CharField (max_length = 250, verbose_name='Название')

    def __unicode__ (self):
        return self.name

    class Meta:
      ordering            = ["id_expersubstparam"]
      verbose_name = ('Дополнительная информация о веществе реакции')
      verbose_name_plural = ('Дополнительная информация о веществе реакции')

class Exper_data (models.Model):
    id_exper_data = models.AutoField (primary_key = True, verbose_name='ИД')
    experiment    = models.ForeignKey(Experiment, null = False, on_delete=models.PROTECT, related_name='exper_data' )
    value = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Значение')
    exper_param    = models.ForeignKey(Dict_exper_param, null = False, on_delete=models.PROTECT, related_name='+',default=0)
    dict_unit_id_unit = models.ForeignKey(Dict_measure_unit, null = False, on_delete=models.PROTECT, related_name='+',default=0)

    class Meta:
      verbose_name = ('Дополнительная информация эксперимента')
      verbose_name_plural = ('Дополнительная информация эксперимента')

class Exper_subst (models.Model):
    id_expersubst = models.AutoField (primary_key = True, verbose_name='ИД')
    experiment    = models.ForeignKey(Experiment, null = False, on_delete=models.PROTECT, related_name='exper_substs')
    reaction_subst = models.ForeignKey(Reaction_subst, null = False, on_delete=models.PROTECT, related_name='+' )
    dict_subst_role = models.ForeignKey(Dict_subst_role, null = False, on_delete=models.PROTECT, related_name='+',default=0)
    is_observed  = models.BooleanField(default = False, verbose_name='Наблюдаемое')
    # todo правильное название?
    init_func_val = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Начальное значение')

    def __unicode__ (self):
        return self.reaction_subst.substance.formula_brutto

    class Meta:
      ordering            = ["id_expersubst"]
      verbose_name = ('Вещество реакции в эксперименте')
      verbose_name_plural = ('Вещества реакции в эксперименте')

class Exper_subst_data (models.Model):
    id_exper_subst_data = models.AutoField (primary_key = True, verbose_name='ИД')
    exper_subst    = models.ForeignKey(Exper_subst, null = False, on_delete=models.PROTECT, related_name='exper_subst_data' )
    value = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Значение')
    subst_param    = models.ForeignKey(Dict_exper_subst_param, null = False, on_delete=models.PROTECT, related_name='+',default=0)
    unit = models.ForeignKey(Dict_measure_unit, null = False, on_delete=models.PROTECT, related_name='+',default=0)

    class Meta:
      verbose_name = ('Дополнительные экспериментальные данные')
      verbose_name_plural = ('Дополнительные экспериментальные данные')

class Exper_point (models.Model):
    id_point = models.AutoField (primary_key = True, verbose_name='ИД')
    exper_subst    = models.ForeignKey(Exper_subst, null = False, on_delete=models.PROTECT, related_name='exper_points', verbose_name='Вещество эксперимента')
    arg_val = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Значение аргумента')
    func_val = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Значение концентрации')

    def __unicode__ (self):
        return self.exper_subst.reaction_subst.substance.formula_brutto

    class Meta:
      verbose_name = ('Экспериментальные данные')
      verbose_name_plural = ('Экспериментальные данные')


##Задачи
class Dict_problem_type(models.Model):
    id_problem_type = models.IntegerField(primary_key=True, verbose_name='ИД')
    name = models.CharField(max_length=250, unique=True, verbose_name='Тип задачи')

    class Meta:
        verbose_name = ('Вид задачи')
        verbose_name_plural = ('Виды задач')

    def __unicode__(self):
        return self.name


class Problem(models.Model):
    id_problem = models.AutoField(primary_key=True, verbose_name='ИД')
    reaction = models.ForeignKey(Reaction, null=False, on_delete=models.CASCADE, related_name='problems')
    problem_type = models.ForeignKey(Dict_problem_type, verbose_name='Вид задачи', null=False, on_delete=models.PROTECT,
        related_name='+', default=0)
    description = models.TextField(blank=True, verbose_name='Описание')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = ('Задача')
        verbose_name_plural = ('Задачи')

    def __unicode__(self):
        return self.id_problem

class Dict_calc_criteria_constraints(models.Model):
    id_criteria = models.AutoField(primary_key=True, verbose_name='ИД')
    name  = models.CharField(max_length=250, unique=True, verbose_name='Тип критерия/ограничения')

    class Meta:
        verbose_name = ('Тип критерия/ограничения')
        verbose_name_plural = ('Типы критериев/ограничений')

    def __unicode__(self):
        return self.name

class Dict_calc_functional(models.Model):
    id_func = models.AutoField(primary_key=True, verbose_name='ИД')
    name  = models.CharField(max_length=250, unique=True, verbose_name='Вид функционала невязки')

    class Meta:
        verbose_name = ('Вид функционала невязки')
        verbose_name_plural = ('Виды функционалов невязки')

    def __unicode__(self):
        return self.name

class Dict_calc_param(models.Model):
    id_dict_param = models.AutoField(primary_key=True, verbose_name='ИД')
    name  = models.CharField(max_length=250, unique=True, verbose_name='Название параметра')
    mask  = models.CharField(max_length=20, unique=True, verbose_name='Маска')
    class Meta:
        verbose_name = ('Параметр решения задачи')
        verbose_name_plural = ('Параметры решения задачи')

    def __unicode__(self):
        return self.name


