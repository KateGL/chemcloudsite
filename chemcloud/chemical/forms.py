# -*- coding: utf-8 -*-
from django import forms
from .models import Reaction_scheme
from django.utils import encoding

class ReacSchemeForm(forms.ModelForm):
	fname        = forms.CharField(max_length=255, label="Название")
	fdescription = forms.CharField(widget=forms.Textarea, label="Описание")
	fis_possible = forms.BooleanField(label="Вероятный")

	class Meta:
		model = Reaction_scheme
		fields = ('fname', 'fdescription', 'fis_possible',)
