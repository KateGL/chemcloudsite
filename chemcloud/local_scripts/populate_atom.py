# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemcloud.settings')

import django
django.setup()

#from chemical.models import Dict_atom
from chemical.chemical_models import Dict_atom,Dict_feature,Dict_model_function
from chemical.chemical_models import Dict_model_argument,Dict_measure_unit

def drop_all():
     Dict_atom.objects.all().delete()
     Dict_feature.objects.all().delete()
     Dict_model_function.objects.all().delete()
     Dict_model_argument.objects.all().delete()
     Dict_measure_unit.objects.all().delete()
     print "dropped all data"

def populate():

   add_atom(atom_num=1, symb="H",  atom_m=1.00800002,  n = "Водород",   nl = "Hydrogenium")
   add_atom(atom_num=2, symb="He",  atom_m=4.00299978,  n = "Гелий",   nl = "Helium")	
   add_atom(atom_num=3, symb="Li",  atom_m=6.94099998,  n = "Литий",   nl =  "Lithium")
   add_atom(atom_num=4, symb="Be",  atom_m=9.01220036,  n = "Бериллий",   nl =  "Beryllium")
   add_atom(atom_num=5, symb="B",  atom_m=10.6110001,  n = "Бор",   nl =  "Borum")
   add_atom(atom_num=6, symb="C",  atom_m=12.0109997,  n = "Углерод",   nl =  "Carboneum")
   add_atom(atom_num=7, symb="N",  atom_m=14.007,  n = "Азот",   nl =  "Nitrogenium")
   add_atom(atom_num=8, symb="O",  atom_m=15.9989996,  n = "Кислород",   nl =  "Oxygenium")
   add_atom(atom_num=9, symb="F",  atom_m=18.9979992,  n = "Фтор",   nl =  "Fluorum")
   add_atom(atom_num=10, symb="Ne",  atom_m=20.1790009,  n = "Неон",   nl =  "Neon")
   add_atom(atom_num=11, symb="Na",  atom_m=22.9899998,  n = "Натрий",   nl =  "Natrium")
   add_atom(atom_num=12, symb="Mg",  atom_m=24.3120003,  n = "Магний",   nl =  "Magnesium")
   add_atom(atom_num=13, symb="Al",  atom_m=26.0919991,  n = "Алюминий",   nl =  "Aluminium")
   add_atom(atom_num=14, symb="Si",  atom_m=28.0860004,  n = "Кремний",   nl =  "Silicium")
   add_atom(atom_num=15, symb="P",  atom_m=30.9740009,  n = "Фосфор",   nl =  "Phosphorus")
   add_atom(atom_num=16, symb="S",  atom_m=32.0639992,  n = "Сера",   nl =  "Sulfur")
   add_atom(atom_num=17, symb="Cl",  atom_m=35.4529991,  n = "Хлор",   nl =  "Chlorum")
   add_atom(atom_num=18, symb="Ar",  atom_m=39.9480019,  n = "Аргон",   nl =  "Argon")
   add_atom(atom_num=19, symb="K",  atom_m=39.1020012,  n = "Калий",   nl =  "Kalium")
   add_atom(atom_num=20, symb="Ca",  atom_m=40.0800018,  n = "Кальций",   nl =  "Calcium")
   add_atom(atom_num=21, symb="Sc",  atom_m=44.9560013,  n = "Скандий",   nl =  "Scandium")
   add_atom(atom_num=22, symb="Ti",  atom_m=47.9560013,  n = "Титан",   nl =  "Titanium")
   add_atom(atom_num=23, symb="V",  atom_m=50.9410019,  n = "Ванадий",   nl =  "Vanadium")
   add_atom(atom_num=24, symb="Cr",  atom_m=51.9959984,  n = "Хром",   nl =  "Chromium")
   add_atom(atom_num=25, symb="Mn",  atom_m=54.9379997,  n = "Марганец",   nl =  "Manganum")
   add_atom(atom_num=26, symb="Fe",  atom_m=55.848999,  n = "Железо",   nl =  "Ferrum")
   add_atom(atom_num=27, symb="Co",  atom_m=58.9329987,  n = "Кобальт",   nl =  "Cobaltum")
   add_atom(atom_num=28, symb="Ni",  atom_m=58.7000008,  n = "Никель",   nl =  "Niccolum")
   add_atom(atom_num=29, symb="Cu",  atom_m=63.5460014,  n = "Медь",   nl =  "Cuprum")
   add_atom(atom_num=30, symb="Zn",  atom_m=65.3700027,  n = "Цинк",   nl =  "Zincum")
   add_atom(atom_num=31, symb="Ga",  atom_m=69.7200012,  n = "Галлий",   nl =  "Gallium")
   add_atom(atom_num=32, symb="Ge",  atom_m=72.5899963,  n = "Германий",   nl =  "Germanium")
   add_atom(atom_num=33, symb="As",  atom_m=74.9919968,  n = "Мышьяк",   nl =  "Arsenicum")
   add_atom(atom_num=34, symb="Se",  atom_m=78.9599991,  n = "Селен",   nl =  "Selenium")
   add_atom(atom_num=35, symb="Br",  atom_m=79.9039993,  n = "Бром",   nl =  "Bromum")
   add_atom(atom_num=36, symb="Kr",  atom_m=83.8000031,  n = "Криптон",   nl =  "Krypton")
   add_atom(atom_num=37, symb="Rb",  atom_m=85.4680023,  n = "Рубидий",   nl =  "Rubidium")
   add_atom(atom_num=38, symb="Sr",  atom_m=87.6200027,  n = "Стронций",   nl =  "Strontium")
   add_atom(atom_num=39, symb="Y",  atom_m=88.9059982,  n = "Иттрий",   nl =  "Yttrium")
   add_atom(atom_num=40, symb="Zr",  atom_m=91.2200012,  n = "Цирконий",   nl =  "Zirconium")
   add_atom(atom_num=41, symb="Nb",  atom_m=92.9059982,  n = "Ниобий",   nl =  "Niobium")
   add_atom(atom_num=42, symb="Mo",  atom_m=95.9400024,  n = "Молибден",   nl =  "Molybdaenum")
   add_atom(atom_num=43, symb="Tc",  atom_m=99,  n = "Технеций",   nl =  "Technetium")
   add_atom(atom_num=44, symb="Ru",  atom_m=101.07,  n = "Рутений",   nl =  "Ruthenium")
   add_atom(atom_num=45, symb="Rh",  atom_m=102.905998,  n = "Родий",   nl =  "Rhodium")
   add_atom(atom_num=46, symb="Pd",  atom_m=106.400002,  n = "Палладий",   nl =  "Palladium")
   add_atom(atom_num=47, symb="Ag",  atom_m=107.867996,  n = "Серебро",   nl =  "Argentum")
   add_atom(atom_num=48, symb="Cd",  atom_m=112.410004,  n = "Кадмий",   nl =  "Cadmium")
   add_atom(atom_num=49, symb="In",  atom_m=114.82,  n = "Индий",   nl =  "Indium")
   add_atom(atom_num=50, symb="Sn",  atom_m=118.690002,  n = "Олово",   nl =  "Stannum")
   add_atom(atom_num=51, symb="Sb",  atom_m=121.75,  n = "Сурьма",   nl =  "Stibium")
   add_atom(atom_num=52, symb="Te",  atom_m=127.599998,  n = "Теллур",   nl =  "Tellurium")
   add_atom(atom_num=53, symb="I",  atom_m=126.904999,  n = "Йод",   nl =  "Iodum")
   add_atom(atom_num=54, symb="Xe",  atom_m=131.300003,  n = "Ксенон",   nl =  "Xenon")
   add_atom(atom_num=55, symb="Cs",  atom_m=132.904999,  n = "Цезий",   nl =  "Caesium")
   add_atom(atom_num=56, symb="Ba",  atom_m=137.339996,  n = "Барий",   nl =  "Barium")
   add_atom(atom_num=57, symb="La",  atom_m=138.906006,  n = "Лантан",   nl =  "Lanthanum")
   add_atom(atom_num=58, symb="Ce",  atom_m=140.119995,  n = "Церий",   nl =  "Cerium")
   add_atom(atom_num=59, symb="Pr",  atom_m=140.908005,  n = "Празеодим",   nl =  "Praseodymium")
   add_atom(atom_num=60, symb="Nd",  atom_m=144.240005,  n = "Неодим",   nl =  "Neodymium")
   add_atom(atom_num=61, symb="Pm",  atom_m=145,  n = "Прометий",   nl =  "Promethium")
   add_atom(atom_num=62, symb="Sm",  atom_m=150.399994,  n = "Самарий",   nl =  "Samarium")
   add_atom(atom_num=63, symb="Eu",  atom_m=151.960007,  n = "Европий",   nl =  "Europium")
   add_atom(atom_num=64, symb="Gd",  atom_m=157.25,  n = "Гадолиний",   nl =  "Gadolinium")
   add_atom(atom_num=65, symb="Tb",  atom_m=158.925995,  n = "Тербий",   nl =  "Terbium")
   add_atom(atom_num=66, symb="Dy",  atom_m=162.5,  n = "Диспрозий",   nl =  "Dysprosium")
   add_atom(atom_num=67, symb="Ho",  atom_m=164.929993,  n = "Гольмий",   nl =  "Holmium")
   add_atom(atom_num=68, symb="Er",  atom_m=167.259995,  n = "Эрбий",   nl =  "Erbium")
   add_atom(atom_num=69, symb="Tm",  atom_m=168.934006,  n = "Тулий",   nl =  "Thulium")
   add_atom(atom_num=70, symb="Yb",  atom_m=173.039993,  n = "Иттербий",   nl =  "Ytterbium")
   add_atom(atom_num=71, symb="Lu",  atom_m=174.970001,  n = "Лютеций",   nl =  "Lutetium")
   add_atom(atom_num=72, symb="Hf",  atom_m=178.490005,  n = "Гафний",   nl =  "Hafnium")
   add_atom(atom_num=73, symb="Ta",  atom_m=180.947998,  n = "Тантал",   nl =  "Tantalum")
   add_atom(atom_num=74, symb="W",  atom_m=183.850006,  n = "Вольфрам",   nl =  "Wolframium")
   add_atom(atom_num=75, symb="Re",  atom_m=186.207001,  n = "Рений",   nl =  "Rhenium")
   add_atom(atom_num=76, symb="Os",  atom_m=190.199997,  n = "Осмий",   nl =  "Osmium")
   add_atom(atom_num=77, symb="Ir",  atom_m=192.220001,  n = "Иридий",   nl =  "Iridium")
   add_atom(atom_num=78, symb="Pt",  atom_m=195.089996,  n = "Платина",   nl =  "Platinum")
   add_atom(atom_num=79, symb="Au",  atom_m=196.966995,  n = "Золото",   nl =  "Aurum")
   add_atom(atom_num=80, symb="Hg",  atom_m=200.589996,  n = "Ртуть",   nl =  "Hydrargyrum")
   add_atom(atom_num=81, symb="Tl",  atom_m=204.369995,  n = "Таллий",   nl =  "Thallium")
   add_atom(atom_num=82, symb="Pb",  atom_m=207.190002,  n = "Свинец",   nl =  "Plumbum")
   add_atom(atom_num=83, symb="Bi",  atom_m=208.979996,  n = "Висмут",   nl =  "Bismuthum")
   add_atom(atom_num=84, symb="Po",  atom_m=210,  n = "Полоний",   nl =  "Polonium")
   add_atom(atom_num=85, symb="At",  atom_m=210,  n = "Астат",   nl =  "Astatium")
   add_atom(atom_num=86, symb="Rn",  atom_m=222,  n = "Радон",   nl =  "Radon")
   add_atom(atom_num=87, symb="Fr",  atom_m=223,  n = "Франций",   nl =  "Francium")
   add_atom(atom_num=88, symb="Ra",  atom_m=226,  n = "Радий",   nl =  "Radium")
   add_atom(atom_num=89, symb="Ac",  atom_m=227,  n = "Актиний",   nl =  "Actinium")
   add_atom(atom_num=90, symb="Th",  atom_m=232.037994,  n = "Торий",   nl =  "Thorium")
   add_atom(atom_num=91, symb="Pa",  atom_m=231,  n = "Протактиний",   nl =  "Protactinium")
   add_atom(atom_num=92, symb="U",  atom_m=238.289993,  n = "Уран",   nl =  "Uranium")
   add_atom(atom_num=93, symb="Np",  atom_m=237,  n = "Нептуний",   nl =  "Neptunium")
   add_atom(atom_num=94, symb="Pu",  atom_m=244,  n = "Плутоний",   nl =  "Plutonium")
   add_atom(atom_num=95, symb="Am",  atom_m=243,  n = "Америций",   nl =  "Americium")
   add_atom(atom_num=96, symb="Cm",  atom_m=247,  n = "Кюрий",   nl =  "Curium")
   add_atom(atom_num=97, symb="Bk",  atom_m=247,  n = "Берклий",   nl =  "Berkelium")
   add_atom(atom_num=98, symb="Cf",  atom_m=251,  n = "Калифорний",   nl =  "Californium")
   add_atom(atom_num=99, symb="Es",  atom_m=254,  n = "Эйнштейний",   nl =  "Einsteinium")
   add_atom(atom_num=100, symb="Fm",  atom_m=257,  n = "Фермий",   nl =  "Fermium")
   add_atom(atom_num=101, symb="Md",  atom_m=258,  n = "Менделевий",   nl =  "Mendelevium")
   add_atom(atom_num=102, symb="No",  atom_m=259,  n = "Нобелий",   nl =  "Nobelium")
   add_atom(atom_num=103, symb="Lr",  atom_m=260,  n = "Лоуренсий",   nl =  "Lawrencium")
   add_atom(atom_num=104, symb="Rf",  atom_m=261,  n = "Резерфордий",   nl =  "Rutherfordium")
   add_atom(atom_num=105, symb="Db",  atom_m=262,  n = "Дубний",   nl =  "Dubnium")
   add_atom(atom_num=106, symb="Sg",  atom_m=263,  n = "Сиборгий",   nl =  "Seaborgium")
   add_atom(atom_num=107, symb="Bh",  atom_m=262,  n = "Борий",   nl =  "Bohrium")
   add_atom(atom_num=108, symb="Hn",  atom_m=265,  n = "Хассий ",   nl =  "Hassium")
   add_atom(atom_num=109, symb="Mt",  atom_m=268,  n = "Мейтнерий",   nl =  "Meitnerium")
   add_dict_feature(1,'Нестационарная')
   add_dict_feature(2,'Изотермическая')
   add_dict_feature(3,'Закрытая')
   add_dict_model_function(1,'Концентрация','x')
   add_dict_model_argument(1,'Время','t')
   add_dict_model_argument(2,'Длина реактора','l')
   add_dict_measure_unit(1,'empty','Пусто',1,1,None)
   b = Dict_measure_unit.objects.get(id_unit=1)
   add_dict_measure_unit(2,'сек','Секунда',1,1,b)
   b = Dict_measure_unit.objects.get(id_unit=2)
   add_dict_measure_unit(3,'мин','Минута',0,60,b)
   add_dict_measure_unit(4,'ч','Час',0,3600,b)
   b = Dict_measure_unit.objects.get(id_unit=1)
   add_dict_measure_unit(5,'М','Моль/л',1,1,b)
   add_dict_measure_unit(6,'doli','Мольные доли',1,1,b)
   add_dict_measure_unit(7,'%','Процентные соотношения наблюдаемых веществ',1,1,b)
   add_dict_measure_unit(8,'м','Метр',1,1,b)
   b = Dict_measure_unit.objects.get(id_unit=8)
   add_dict_measure_unit(9,'см','Сантиметр',0,100,b)
   b = Dict_measure_unit.objects.get(id_unit=1)
   add_dict_measure_unit(10,'%','Проценты',1,1,b)
   add_dict_measure_unit(11,'кг/(м2*сек)','Массовая скорость потока',1,1,b)

#5 M Моль/л Да 1 1
#6 doli Мольные доли Да 1 1
#7 % Процентные соотношения наблюдаемых веществ Да 1 1
#8 м Метр Да 1 1
#9 см Сантиметр Нет 100 8
#10 % Проценты Да 1 1
#11 (Ед.изм.Скорости потока, Лениза, в твоих реакциях есть? Тогда укажи)


    # Print out what we have added to the user.
   #for a in Dict_atom.objects.all():
   #         print "{0}- {1} ".format(str(a), a.symbol)
   #for a in Dict_feature.objects.all():
   #         print "{0}- {1} ".format(str(a), a.name)

def add_atom(atom_num, symb, atom_m, n, nl):
    a = Dict_atom.objects.get_or_create(atom_number=atom_num, symbol=symb, atom_mass = atom_m, name = n, name_latin = nl)[0]
    a.save()
    return a

def add_dict_feature(id_feature_,name_):
    a = Dict_feature.objects.get_or_create(id_feature=id_feature_, name=name_)[0]
    a.save()
    return a

def add_dict_model_function(id_func_,name_,symbol_):
    a = Dict_model_function.objects.get_or_create(id_func=id_func_, name=name_,symbol=symbol_)[0]
    a.save()
    return a

def add_dict_model_argument(id_arg_,name_,symbol_):
    a = Dict_model_argument.objects.get_or_create(id_arg=id_arg_, name=name_,symbol=symbol_)[0]
    a.save()
    return a

def add_dict_measure_unit(id_unit_,code_,name_,is_si_,multiplier_,id_unit_si_):
    a = Dict_measure_unit.objects.get_or_create(id_unit=id_unit_,code=code_, name=name_,is_si=is_si_,multiplier=multiplier_,id_unit_si=id_unit_si_)[0]
    a.save()
    return a

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    drop_all()
    populate()
    print "Data successfully added!"