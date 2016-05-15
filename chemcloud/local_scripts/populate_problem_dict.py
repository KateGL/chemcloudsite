# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemcloud.settings')

import django
django.setup()


from chemical.chemical_models import Problem, Dict_problem_type


def populate():
#dict_problem_type
   add_dict_problem_type(1,'Прямая задача химической кинетики')
   add_dict_problem_type(2,'Обратная задача химической кинетики')
   add_dict_problem_type(3,'Анализ неопределенности кинетических параметров')
   add_dict_problem_type(4,'Анализ чувствительности кинетических параметров')
   add_dict_problem_type(5,'Анализ жесткости системы ОДУ')
   add_dict_problem_type(6,'Оптимизация условий проведения реакции')
   add_dict_problem_type(7,'Расчет энергий активаций с помощью МНК')
   add_dict_problem_type(8,'Выделение маршрутов механизма реакции')

def add_dict_problem_type(id,nm):
    a = Dict_problem_type.objects.get_or_create(id_problem_type=id,name=nm)[0]
    a.save()
    return a

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    populate()
    print "Data successfully added!"
