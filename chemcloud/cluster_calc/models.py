# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Кластер
class Cluster(models.Model):
    id_cluster = models.AutoField(primary_key=True, verbose_name='ИД')
    name = models.CharField(max_length=250, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')


#Пользователь кластера
class Cluster_user(models.Model):
    id_cluster_user = models.AutoField(primary_key=True, verbose_name='ИД')
    user = models.ForeignKey(User, related_name='clusters', verbose_name='Пользователь', null=False, on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster, related_name='users', verbose_name='Кластер', null=False, on_delete=models.CASCADE)


#