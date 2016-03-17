# -*- coding: utf-8 -*-
from django import forms
from .models import Reaction_scheme, Substance, Reaction


#Реакции
class ReactionForm(forms.ModelForm):
    class Meta:
       model = Reaction
       fields = '__all__'

#Механизмы реакции
class ReacSchemeForm(forms.ModelForm):
    name        = forms.CharField(max_length=255, label="Название")
    description = forms.CharField(widget=forms.Textarea, label="Описание")
    is_possible = forms.BooleanField(label="Вероятный")

    class Meta:
        model = Reaction_scheme
        fields = ('name', 'description', 'is_possible',)

#Вещества
class SubstanceForm(forms.ModelForm):
    class Meta:
       model = Substance
       fields = '__all__'

#Эксперименты
