# -*- coding: utf-8 -*-
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Атом
class Dict_atom(models.Model):
    atom_number = models.IntegerField(primary_key = True, verbose_name='Атомный номер')
    symbol = models.CharField(max_length=3, unique=True, verbose_name='Обозначение')
    atom_mass = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Атомная масса')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название (рус)')
    name_latin = models.CharField(max_length=100, unique=True, verbose_name='Название (лат)')
    class Meta:
        verbose_name = ('Атом')
        verbose_name_plural = ('Атомы')
        ordering = ["atom_number"]

    def __unicode__ (self):
        return self.symbol

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

    def __unicode__ (self):
        return self.name

    def consist_create(self):#создает состав вещества на основе брутто-формулы
        self.consist.all().delete()#clear consist
        atoms_dict = self.get_atom_dict()# ахтунг! говнокод
        #atoms_dict = {'H':2, 'Oh':3}
        for key, val in atoms_dict.items():
            try:
              atom = Dict_atom.objects.get(symbol=key)
              if atom:
                co = Substance_consist.objects.get_or_create(atom =atom, substance = self, atom_count = val)[0]
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
class Substance_consist(models.Model):
    substance = models.ForeignKey(Substance, null = False, on_delete=models.CASCADE, related_name='consist')
    atom = models.ForeignKey(Dict_atom, null = False, on_delete=models.CASCADE, related_name='+')
    atom_count = models.DecimalField(max_digits=11, decimal_places=7,default = 0, verbose_name = 'Количество атомов')
    class Meta:
        verbose_name = ('Состав Вещества')
        verbose_name_plural = ('Составы Вещества')

    #def __unicode__ (self):
    #   return self.substance

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
            empty_step = Scheme_step.objects.get_or_create( scheme = self, order = new_order, is_revers = False )[0]
            empty_step.save()
            self.steps.add(empty_step)
        except:
            return -1
        return empty_step

    class Meta:
        ordering            = ["updated_date"]
        verbose_name        = ('Механизм')
        verbose_name_plural = ('Механизмы')

#Стадия схемы реакции
class Scheme_step(models.Model):
    id_step       = models.AutoField (primary_key = True, verbose_name='ИД')
    scheme        = models.ForeignKey(Reaction_scheme, null = False, on_delete=models.CASCADE, related_name='steps')
    name          = models.CharField (max_length = 250, verbose_name='Обозначение')
    order         = models.IntegerField (verbose_name='№ п/п')
    is_revers     = models.BooleanField (verbose_name='Обратимая')
    note            = models.CharField (max_length = 250, blank = True, verbose_name='Примечание')
    rate_equation = models.TextField (blank= True, verbose_name='Выражение для скорости')#todo data type
    def __unicode__ (self):
        return self.name

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

    def check_step_balance(self):
        try:
            step_substs = self.scheme_step_substs.all()
            atoms_list = []
            A_mtrx_Transp = []
            G_coll = []
            for subst_i in step_substs:
                G_coll = G_coll + [subst_i.stoich_koef]
                print(G_coll)
                atoms = subst_i.reac_substance.substance.consist.all()
                print(atoms)
                print('tututu3')
                for atom_j in atoms:
                    atoms_list = atoms_list + [atom.symbol]
            print (atoms_list )
            atoms_list = list(set(atoms_list))
            print (atoms_list )
            print('tututu345')
        except:
            print('tututu567')
            return False
        return True

    class Meta:
        ordering            = ["order"]
        verbose_name        = ('Стадия схемы')##Механизма или Схемы??? я путаюсь Рита: это общая модель схемы и механизма и маршрута. ПО крайней мере по вертабело. Пока так. Дойдем до маршрутов - будет видно
        verbose_name_plural = ('Стадии схемы')

#Вещества реакции
class Reaction_subst(models.Model):
    reaction = models.ForeignKey(Reaction, null = False, on_delete=models.CASCADE, related_name='substances' )
    substance = models.ForeignKey(Substance, null = True, on_delete=models.PROTECT, related_name='+' )
    alias = models.CharField (max_length = 250, verbose_name='Псевдоним', null = False)
    brutto_formula_short = models.CharField (max_length = 250, verbose_name='Краткая брутто-формула')
    #brutto_formula_short_formatted = models.CharField (max_length = 250, verbose_name='Краткая брутто-формула')
    note = models.TextField(blank = True,  verbose_name='Примечание')


    def __unicode__ (self):
        return self.alias

    class Meta:
      verbose_name = ('Вещество реакции')
      verbose_name_plural = ('Вещества реакции')
      unique_together = ('reaction', 'substance')

#Вещество в стадии схемы реакции
class Scheme_step_subst(models.Model):
    #первичный ключ, только для возможности django создать ключ
    id_step = models.AutoField (primary_key = True, verbose_name='ИД')
    step         = models.ForeignKey(Scheme_step, null = False, on_delete=models.CASCADE, related_name='scheme_step_substs')
    reac_substance    = models.ForeignKey(Reaction_subst, null = False, on_delete=models.CASCADE, related_name='+')
    position     =    models.IntegerField(verbose_name='Позиция вещества в стадии')
    stoich_koef  =    models.DecimalField(max_digits=6, decimal_places=3,default = 0, verbose_name='Стехиометрический коэффициент')
    class Meta:
        ordering            = ["id_step", "position"]
        unique_together     = ('step', 'reac_substance')
        verbose_name        = ('Вещество стадии')
        verbose_name_plural = ('Вещества стадии')


#Права пользователя
#Считаем, что если есть запист в этой таблице, то Пользователь имеет право на чтение Реакции
#Если is_owner == True то пользователь может редактировать реакцию и расшаривать ее другим Пользователям
class User_reaction(models.Model):
    reaction = models.ForeignKey(Reaction, related_name='users', verbose_name='Реакция', null = False,on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reactions', verbose_name='Пользователь', null = False,on_delete=models.CASCADE)
    is_owner = models.BooleanField(default = False, verbose_name='Владелец')

    class Meta:
      verbose_name = ('Доступ к Реакции')
      verbose_name_plural = ('Права на Реакции ')
      unique_together = ('reaction', 'user')

#Синонимы вещества
class Substance_synonym (models.Model):
    substance = models.ForeignKey(Substance, null = True, on_delete=models.PROTECT, related_name='synonyms' )
    name = models.CharField (max_length = 250, verbose_name='Название')

    def __unicode__ (self):
        return self.name

    class Meta:
        ordering            = ["name"]
        verbose_name        = ('Синоним вещества')
        verbose_name_plural = ('Синонимы вещества')


#Тэги реакции
class Reaction_tag(models.Model):
    reaction = models.ForeignKey(Reaction, null = True, on_delete=models.PROTECT, related_name='+' )
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
        ordering = ["name"]


#Свойства реакции
class Reaction_feature(models.Model):
    reaction = models.ForeignKey(Reaction, null = True, on_delete=models.PROTECT, related_name='+' )
    feature = models.ForeignKey(Dict_feature, null = True, on_delete=models.PROTECT, related_name='+' )

    class Meta:
      verbose_name = ('Свойство реакции')
      verbose_name_plural = ('Свойства реакции')


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
        ordering = ["name"]

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
        ordering = ["name"]

# Единицы измерения
class Dict_measure_unit(models.Model):
    id_unit = models.IntegerField(primary_key = True, verbose_name='Номер единицы измерения')
    code = models.CharField(max_length=250, verbose_name='Обозначение')
    name = models.CharField(max_length=250, unique=True, verbose_name='Название единицы измерения')
    is_si = models.BooleanField(default = True, verbose_name='СИ')
    multiplier = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Множитель')
    id_unit_si = models.ForeignKey('self', null = True, blank=True, related_name='+' )


    def __unicode__ (self):
        return self.name

    class Meta:
        verbose_name = ('Единица измерения')
        verbose_name_plural = ('Единицы измерения')
        ordering = ["name"]


#Эксперименты
class Experiment (models.Model):
    id_experiment    = models.AutoField (primary_key = True, verbose_name='ИД')
    reaction     = models.ForeignKey(Reaction, null = False, on_delete=models.CASCADE, related_name='experiments' )
    argument_measure = models.ForeignKey(Dict_measure_unit, null = True, on_delete=models.PROTECT, related_name='+' )
    function_measure = models.ForeignKey(Dict_measure_unit, null = True, on_delete=models.PROTECT, related_name='+' )
    init_function_measure = models.ForeignKey(Dict_measure_unit, null = True, on_delete=models.PROTECT, related_name='+' )
    description  = models.TextField (blank = True, verbose_name='Описание')
    id_func = models.ForeignKey(Dict_model_function, null = True, on_delete=models.PROTECT, related_name='+' )
    id_arg = models.ForeignKey(Dict_model_argument, null = True, on_delete=models.PROTECT, related_name='+' )
    exper_date = models.DateTimeField (default=timezone.now, verbose_name='Дата проведения')
    updated_by   = models.TextField (verbose_name='Обновил(а)')
    updated_date = models.DateTimeField (default=timezone.now, verbose_name='Дата обновления')
    is_favorite  = models.BooleanField(default = False, verbose_name='Избранное')
    created_date = models.DateTimeField (default=timezone.now, verbose_name='Дата создания')
    name         = models.CharField (max_length = 250, verbose_name='Название')
    created_by   = models.TextField (verbose_name='Создал(ла)')#todo data type

    def __unicode__ (self):
        return self.name

    class Meta:
      ordering            = ["updated_date"]
      verbose_name = ('Эксперимент')
      verbose_name_plural = ('Эксперименты')

class Dict_subst_role (models.Model):
    id_role = models.AutoField (primary_key = True, verbose_name='ИД')
    name         = models.CharField (max_length = 250, verbose_name='Название')

    def __unicode__ (self):
        return self.name

    class Meta:
      ordering            = ["id_role"]
      verbose_name = ('Роль вещества в механизме')
      verbose_name_plural = ('Роли вещества в механизме')

class Dict_exper_param (models.Model):
    id_experparam = models.AutoField (primary_key = True, verbose_name='ИД')
    name         = models.CharField (max_length = 250, verbose_name='Название')

    def __unicode__ (self):
        return self.name

    class Meta:
      ordering            = ["id_experparam"]
      verbose_name = ('Дополнительные данные эксперимента')
      verbose_name_plural = ('Дополнительные данные эксперимента')

class Dict_exper_subst_param (models.Model):
    id_expersubstparam = models.AutoField (primary_key = True, verbose_name='ИД')
    name         = models.CharField (max_length = 250, verbose_name='Название')

    def __unicode__ (self):
        return self.name

    class Meta:
      ordering            = ["id_expersubstparam"]
      verbose_name = ('Дополнительная информация о веществе реакции')
      verbose_name_plural = ('Дополнительная информация о веществе реакции')

class Exper_data (models.Model):
    experiment    = models.ForeignKey(Experiment, null = False, on_delete=models.PROTECT, related_name='exper_data' )
    value = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Значение')
    exper_param    = models.ForeignKey(Dict_exper_param, null = False, on_delete=models.PROTECT, related_name='+' )
    dict_unit_id_unit = models.ForeignKey(Dict_measure_unit, null = False, on_delete=models.PROTECT, related_name='+' )

    class Meta:
      verbose_name = ('Дополнительная информация эксперимента')
      verbose_name_plural = ('Дополнительная информация эксперимента')


class Exper_subst (models.Model):
    id_expersubst = models.AutoField (primary_key = True, verbose_name='ИД')
    experiment    = models.ForeignKey(Experiment, null = False, on_delete=models.PROTECT, related_name='exper_subst' )
    reaction_subst = models.ForeignKey(Reaction_subst, null = False, on_delete=models.PROTECT, related_name='+' )
    dict_subst_role = models.ForeignKey(Dict_subst_role, null = False, on_delete=models.PROTECT, related_name='+' )
    is_observed  = models.BooleanField(default = False, verbose_name='Наблюдаемое')
    # todo правильное название?
    init_func_val = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Начальное значение')

    def __unicode__ (self):
        return self.id_expersubst

    class Meta:
      ordering            = ["id_expersubst"]
      verbose_name = ('Вещество реакции в эксперименте')
      verbose_name_plural = ('Вещества реакции в эксперименте')

class Exper_subst_data (models.Model):
    exper_subst    = models.ForeignKey(Exper_subst, null = False, on_delete=models.PROTECT, related_name='exper_subst_data' )
    value = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Значение')
    subst_param    = models.ForeignKey(Dict_exper_subst_param, null = False, on_delete=models.PROTECT, related_name='+' )
    unit = models.ForeignKey(Dict_measure_unit, null = False, on_delete=models.PROTECT, related_name='+' )

    class Meta:
      verbose_name = ('Дополнительные экспериментальные данные')
      verbose_name_plural = ('Дополнительные экспериментальные данные')

###
class Exper_point (models.Model):
    id_point = models.AutoField (primary_key = True, verbose_name='ИД')
    exper_subst    = models.ForeignKey(Exper_subst, null = False, on_delete=models.PROTECT, related_name='exper_point' )
    arg_val = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Значение аргумента')
    func_val = models.DecimalField(max_digits=11, decimal_places=7, verbose_name='Значение концентрации')

    subst_param    = models.ForeignKey(Dict_exper_subst_param, null = False, on_delete=models.PROTECT, related_name='+' )
    unit = models.ForeignKey(Dict_measure_unit, null = False, on_delete=models.PROTECT, related_name='+' )

    class Meta:
      verbose_name = ('Экспериментальные данные')
      verbose_name_plural = ('Экспериментальные данные')
