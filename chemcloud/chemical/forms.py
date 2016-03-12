# -*- coding: utf-8 -*-
from django import forms
from .models import Reaction_scheme, Substance, Reaction
import re
from .utils import check_blocks


#Реакции
class ReactionForm(forms.ModelForm):
    class Meta:
       model = Reaction
       fields = '__all__'

#Механизмы реакции
class ReacSchemeForm(forms.ModelForm):
    class Meta:
        model = Reaction_scheme
        fields = ('name', 'description', 'is_possible',)

#Вещества
class BruttoFormulaField(forms.CharField):
    def validate(self, value):
        super(BruttoFormulaField, self).validate(value)
        if re.sub(r'[A-Za-z0-9\(\)\[\]]','', value)!= '':
            raise forms.ValidationError("Брутто-формула может содержать только числа, латиницу и скобки")
        if not check_blocks(value,'(',')'):
            raise forms.ValidationError("Проверьте правильность расположения круглых скобок!")
        if not check_blocks(value,'[',']'):
            raise forms.ValidationError("Проверьте правильность расположения квадратных скобок!")
#не совсем правильно, тк допустива конструкция [(])

class SubstanceForm(forms.ModelForm):
    formula_brutto = BruttoFormulaField( label="Брутто-формула")
    note = forms.CharField(widget=forms.Textarea, required = False, label="Примечание")
    class Meta:
       model = Substance
       fields = ('name', 'charge', 'is_radical', 'formula_brutto', 'note')

#Эксперименты
