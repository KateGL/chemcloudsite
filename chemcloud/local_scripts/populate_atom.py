# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemcloud.settings')

import django
django.setup()

from chemical.models import Atom

def drop_all():
     Atom.objects.all().delete()
     print "dropped all atoms" 

def populate():   

    add_atom(atom_num=2, symb="H2",  atom_m=0.002,  n = "Водород2",   nl =  "Hg2")
    add_atom(atom_num=21, symb="H21",  atom_m=0.002,  n = "Водород21",   nl =  "Hg21")
    add_atom(atom_num=22, symb="H22",  atom_m=0.002,  n = "Водород22",   nl =  "Hg22")
    add_atom(atom_num=23, symb="H23",  atom_m=0.002,  n = "Водород23",   nl =  "Hg23")
    add_atom(atom_num=24, symb="H24",  atom_m=0.002,  n = "Водород24",   nl =  "Hg24")
    add_atom(atom_num=25, symb="H25",  atom_m=0.002,  n = "Водород25",   nl =  "Hg25")
    add_atom(atom_num=26, symb="H26",  atom_m=0.002,  n = "Водород26",   nl =  "Hg26")
    add_atom(atom_num=27, symb="H27",  atom_m=0.002,  n = "Водород27",   nl =  "Hg27")
    add_atom(atom_num=28, symb="H28",  atom_m=0.002,  n = "Водород28",   nl =  "Hg28")
    add_atom(atom_num=29, symb="H29",  atom_m=0.002,  n = "Водород29",   nl =  "Hg29")
    add_atom(atom_num=32, symb="H32",  atom_m=0.002,  n = "Водород32",   nl =  "Hg32")
    add_atom(atom_num=42, symb="H42",  atom_m=0.002,  n = "Водород42",   nl =  "Hg42")
    add_atom(atom_num=52, symb="H52",  atom_m=0.002,  n = "Водород52",   nl =  "Hg52")


    # Print out what we have added to the user.
    for a in Atom.objects.all():
            print "{0}- {1} ".format(str(a), a.symbol)

def add_atom(atom_num, symb, atom_m, n, nl):
    a = Atom.objects.get_or_create(atom_number=atom_num, symbol=symb, atom_mass = atom_m, name = n, name_latin = nl)[0]
    a.save()
    return a


# Start execution here!
if __name__ == '__main__':
    print "Starting Atom population script..."
    drop_all()
    populate()
