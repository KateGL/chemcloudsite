# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Faq(models.Model):
	question = models.CharField (max_length = 250, verbose_name='Вопрос')
	answer = models.CharField (max_length = 250, verbose_name='Ответ')
	def __unicode__(self):
		return self.question	

# Тут надо расширить модель Пользователя для тго чтобы прописать доступы и тд
