# -*- coding: utf-8 -*-
from django import forms
from .models import Reaction_scheme
from django.utils import encoding

class ReacSchemeForm(forms.ModelForm):
	name        = forms.CharField(max_length=255, label="Название")
	description = forms.CharField(widget=forms.Textarea, label="Описание")
	is_possible = forms.BooleanField(label="Вероятный")

	class Meta:
		model = Reaction_scheme
		fields = ('name', 'description', 'is_possible',)
