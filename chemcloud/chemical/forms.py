# -*- coding: utf-8 -*-
#from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.utils import timezone
#from django.forms.util import flatatt
from .chemical_models import Reaction_scheme, Substance, Reaction, Experiment, Reaction_subst, Problem, Exper_serie
import re
from chemical.utils import check_blocks


class DateWithPickerField(forms.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d.%m.%Y %H:%M",))
        super(DateWithPickerField, self).__init__(*args, **kwargs)

#Реакции
class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ('name', 'description', 'is_favorite')
#        fields = ('name', 'description', 'is_favorite', 'is_notstationary', 'is_isothermal')


#Поделиться реакцией
class ReactionShareForm(forms.Form):
    user_email = forms.EmailField(label='Email пользователя')
    CHOICES = (('0', "Только чтение"), ('1', "Разрешить чтение, редактирование, делиться"))
    rights = forms.ChoiceField(label='Права', widget=forms.RadioSelect, choices=CHOICES, initial='0')
    message = forms.CharField(widget=forms.Textarea, required=False, label="Сообщение")


#Механизмы реакции
class ReacSchemeForm(forms.ModelForm):
    class Meta:
        model = Reaction_scheme
        fields = ('name', 'description', 'is_possible',)


#Вещества
class BruttoFormulaField(forms.CharField):
    def validate(self, value):
        super(BruttoFormulaField, self).validate(value)
        if re.sub(r'[A-Za-z0-9\(\)\[\]]', '', value) != '':
            raise forms.ValidationError("Брутто-формула может содержать только числа, латиницу и скобки")
        if not check_blocks(value, '(', ')'):
            raise forms.ValidationError("Проверьте правильность расположения круглых скобок!")
        if not check_blocks(value, '[', ']'):
            raise forms.ValidationError("Проверьте правильность расположения квадратных скобок!")
#не совсем правильно, тк допустива конструкция [(])
#проверка на то, что в


class SubstanceForm(forms.ModelForm):
    formula_brutto = BruttoFormulaField(label="Брутто-формула")
    note = forms.CharField(widget=forms.Textarea, required=False, label="Примечание")

    class Meta:
        model = Substance
        fields = ('name', 'charge', 'is_radical', 'formula_brutto', 'note')


#Вещества реакции
class ReactionSubstForm(forms.ModelForm):
    class Meta:
        model = Reaction_subst
        fields = ('substance', 'alias', 'brutto_formula_short', 'note')


#Серия для Экспериментов
class ExperSerieForm(forms.ModelForm):

    class Meta:
        model = Exper_serie
        fields = ('name', 'description', 'is_archive')


#Эксперименты
class ExperimentForm(forms.ModelForm):
    exper_date = DateWithPickerField(initial=timezone.now, label="Дата проведения")
    class Meta:
        model = Experiment
        fields = ('name', 'exper_date', 'description', 'exper_serie', 'is_favorite', 'func', 'function_measure', 'arg',
            'argument_measure', 'init_function_measure')


#Задачи
class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('problem_type', 'description' )




