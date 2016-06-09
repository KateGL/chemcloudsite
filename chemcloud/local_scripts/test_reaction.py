# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemcloud.settings')

import django
django.setup()

from datetime import datetime,date,time

#from chemical.models import Dict_atom
from chemical.chemical_models import Dict_atom,Dict_feature,Dict_model_function
from chemical.chemical_models import Dict_model_argument,Dict_measure_unit
from chemical.chemical_models import Reaction, User_reaction,Substance,Substance_synonym
from chemical.chemical_models import Reaction_subst,Reaction_scheme,Scheme_step,Scheme_step_subst
from chemical.chemical_models import Experiment,Substance_consist,Dict_exper_param,Dict_exper_subst_param
from chemical.chemical_models import Dict_subst_role,Exper_subst_data,Exper_subst,Exper_data,Exper_serie
from chemical.chemical_models import Exper_point,Reaction_feature
from django.contrib.auth.models import User

def drop_all():
     User_reaction.objects.all().delete()
     Substance_synonym.objects.all().delete()
     Exper_subst_data.objects.all().delete()
     Exper_point.objects.all().delete()
     Exper_subst.objects.all().delete()
     Reaction_subst.objects.all().delete()
     Substance.objects.all().delete()
     Exper_data.objects.all().delete()
     Exper_serie.objects.all().delete()
     Experiment.objects.all().delete()
     Reaction_feature.objects.all().delete()
     Reaction.objects.all().delete()
     Reaction_scheme.objects.all().delete()
     Scheme_step.objects.all().delete()
     Scheme_step_subst.objects.all().delete()
     Substance_consist.objects.all().delete()

     print "dropped test reactions data"

def populate():

    # тестовая реакция
   add_reaction(id_reac=1, nm='Паровая конверсия пропана', dscr='Низкотемпературная паровая конверсия пропана', is_f=1, cb='Admin', ub='Admin')
   b = Reaction.objects.get(id_reaction=1)
   c = User.objects.get(id=1)
   add_user_reaction(b,c,1)
   c = Dict_feature.objects.get(id_feature=0)
   add_reaction_feature(1,b,c)
   add_substance(1,'пропан',0,0,'C3H8','пропан')
   add_substance(2,'вода',0,0,'H2O','вода')
   add_substance(3,'оксид углерода (IV)',0,0,'CO2','углекислый газ')
   add_substance(4,'водород',0,0,'H2','водород')
   add_substance(5,'метан',0,0,'CH4','метан')
   c = Substance.objects.get(id_substance=1)
   add_reac_subst(b,c,'x1','C3H8','')
   c = Substance.objects.get(id_substance=2)
   add_reac_subst(b,c,'x2','H2O','')
   c = Substance.objects.get(id_substance=3)
   add_reac_subst(b,c,'x3','CO2','')
   c = Substance.objects.get(id_substance=4)
   add_reac_subst(b,c,'x4','H2','')
   c = Substance.objects.get(id_substance=5)
   add_reac_subst(b,c,'x5','CH4','')

   add_reac_scheme(1,b,'Схема реакции паровой конверсии пропана','Схема реакции паровой конверсии пропана',1,'Admin','Admin')
   c = Reaction_scheme.objects.get(id_scheme=1)
   add_scheme_step(1,c,'Стадия № 1',1,0,'Первая стадия','', True)
   add_scheme_step(2,c,'Стадия № 2',2,1,'Вторая стадия','', True)
   c = Scheme_step.objects.get(id_step=1)
   d = Substance.objects.get(id_substance=1)
   f = Reaction_subst.objects.get(reaction=b,substance=d)
   add_scheme_step_subst(1,c,f,1,-1)
   d = Substance.objects.get(id_substance=2)
   f = Reaction_subst.objects.get(reaction=b,substance=d)
   add_scheme_step_subst(2,c,f,2,-6)
   d = Substance.objects.get(id_substance=3)
   f = Reaction_subst.objects.get(reaction=b,substance=d)
   add_scheme_step_subst(3,c,f,3,3)
   d = Substance.objects.get(id_substance=4)
   f = Reaction_subst.objects.get(reaction=b,substance=d)
   add_scheme_step_subst(4,c,f,4,10)
   c = Scheme_step.objects.get(id_step=2)
   d = Substance.objects.get(id_substance=3)
   f = Reaction_subst.objects.get(reaction=b,substance=d)
   add_scheme_step_subst(5,c,f,1,-1)
   d = Substance.objects.get(id_substance=4)
   f = Reaction_subst.objects.get(reaction=b,substance=d)
   add_scheme_step_subst(6,c,f,2,-4)
   d = Substance.objects.get(id_substance=5)
   f = Reaction_subst.objects.get(reaction=b,substance=d)
   add_scheme_step_subst(7,c,f,3,1)
   d = Substance.objects.get(id_substance=2)
   f = Reaction_subst.objects.get(reaction=b,substance=d)
   add_scheme_step_subst(8,c,f,4,2)
   # Добавление состава веществ

   # C3H8
   c = Substance.objects.get(id_substance=1)
   d = Dict_atom.objects.get(atom_number=1)
   add_substance_consist(c,d,8)
   d = Dict_atom.objects.get(atom_number=6)
   add_substance_consist(c,d,3)

   # H2O
   c = Substance.objects.get(id_substance=2)
   d = Dict_atom.objects.get(atom_number=1)
   add_substance_consist(c,d,2)
   d = Dict_atom.objects.get(atom_number=8)
   add_substance_consist(c,d,1)

   # CO2
   c = Substance.objects.get(id_substance=3)
   d = Dict_atom.objects.get(atom_number=6)
   add_substance_consist(c,d,1)
   d = Dict_atom.objects.get(atom_number=8)
   add_substance_consist(c,d,2)

   # H2
   c = Substance.objects.get(id_substance=4)
   d = Dict_atom.objects.get(atom_number=1)
   add_substance_consist(c,d,2)

   # CH4
   c = Substance.objects.get(id_substance=5)
   d = Dict_atom.objects.get(atom_number=6)
   add_substance_consist(c,d,1)
   d = Dict_atom.objects.get(atom_number=1)
   add_substance_consist(c,d,4)

   # Добавление экспериментов
   add_exper_serie(1,b,'Первая серия','Первая серия опытов реакции паровой конверсии пропана. Условия: Катализатор НИАП-12-05(з-15). 34% CH4, 17% C3H8, 49% H2O,   H2O/C(в пропане) = 1,    H2O/C = 0.58;  GHSV= 670 1/ч,    G(влаж.смеси)=0.17 мл/сек')
   # Эксперимент 1
   d = Dict_measure_unit.objects.get(id_unit=8)
   e = Dict_measure_unit.objects.get(id_unit=6)
   f = Dict_model_function.objects.get(id_func=1)
   g = Dict_model_argument.objects.get(id_arg=2)
   h = date(2005,7,14)
   i = time(12,30)
   add_exper(1,b,d,e,e,'Эксперимент 1. Катализатор НИАП-12-05',f,g,datetime.combine(h,i),'Admin',1,'Эксперимент 1','Admin')
   a = Experiment.objects.get(id_experiment=1)
   b = Exper_serie.objects.get(id_serie=1)
   
   # Добавление веществ реакции в эксперименте
   b = Reaction.objects.get(id_reaction=1)
   # C3H8
   c = Substance.objects.get(id_substance=1)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   e = Dict_subst_role.objects.get(id_role=1)
   add_exper_subst(1,a,d,e,1,17)
   # H2O
   c = Substance.objects.get(id_substance=2)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   add_exper_subst(2,a,d,e,0,49)
   # O2
   c = Substance.objects.get(id_substance=3)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   e = Dict_subst_role.objects.get(id_role=3)
   add_exper_subst(3,a,d,e,1,0)
   # H2
   c = Substance.objects.get(id_substance=4)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   add_exper_subst(4,a,d,e,1,0)
   # CH4
   c = Substance.objects.get(id_substance=5)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   e = Dict_subst_role.objects.get(id_role=1)
   add_exper_subst(5,a,d,e,1,34)

   # данные Эксперимента 1
   c = Exper_subst.objects.get(id_expersubst=1)
   add_exper_point(1,c,0.02,0.04)
   c = Exper_subst.objects.get(id_expersubst=3)
   add_exper_point(2,c,0.02,10.09)
   c = Exper_subst.objects.get(id_expersubst=4)
   add_exper_point(3,c,0.02,5.18)
   c = Exper_subst.objects.get(id_expersubst=5)
   add_exper_point(4,c,0.02,83.26)

   # Эксперимент 2
   b = Reaction.objects.get(id_reaction=1)
   d = Dict_measure_unit.objects.get(id_unit=8)
   e = Dict_measure_unit.objects.get(id_unit=6)
   f = Dict_model_function.objects.get(id_func=1)
   g = Dict_model_argument.objects.get(id_arg=2)
   h = date(2005,7,14)
   i = time(12,30)

   add_exper(2,b,d,e,e,'Эксперимент 2. Катализатор НИАП-12-05',f,g,datetime.combine(h,i),'Admin',1,'Эксперимент 2','Admin')
   a = Experiment.objects.get(id_experiment=2)
   b = Exper_serie.objects.get(id_serie=1)
   
   # Добавление вещест реакции в эксперименте
   b = Reaction.objects.get(id_reaction=1)
   # C3H8
   c = Substance.objects.get(id_substance=1)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   e = Dict_subst_role.objects.get(id_role=1)
   add_exper_subst(6,a,d,e,1,17)
   # H2O
   c = Substance.objects.get(id_substance=2)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   add_exper_subst(7,a,d,e,0,49)
   # CO2
   c = Substance.objects.get(id_substance=3)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   e = Dict_subst_role.objects.get(id_role=3)
   add_exper_subst(8,a,d,e,1,0)
   # H2
   c = Substance.objects.get(id_substance=4)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   add_exper_subst(9,a,d,e,1,0)
   # CH4
   c = Substance.objects.get(id_substance=5)
   d = Reaction_subst.objects.get(reaction=b,substance=c)
   e = Dict_subst_role.objects.get(id_role=1)
   add_exper_subst(10,a,d,e,1,34)

   # данные Эксперимента 2
   c = Exper_subst.objects.get(id_expersubst=6)
   add_exper_point(5,c,0.02,0.03)
   add_exper_point(6,c,0.03,0.04)
   c = Exper_subst.objects.get(id_expersubst=8)
   add_exper_point(7,c,0.02,9.94)
   add_exper_point(8,c,0.03,10.94)
   c = Exper_subst.objects.get(id_expersubst=9)
   add_exper_point(9,c,0.02,3.83)
   c = Exper_subst.objects.get(id_expersubst=10)
   add_exper_point(10,c,0.02,84.99)
   add_exper_point(11,c,0.03,89.94)


   # Print out what we have added to the user.
   #for a in Dict_atom.objects.all():
   #         print "{0}- {1} ".format(str(a), a.symbol)
   #for a in Dict_feature.objects.all():
   #         print "{0}- {1} ".format(str(a), a.name)

#def add_reaction(id_reac, nm, dscr, is_f, cb, cd, ub, ud):
def add_reaction(id_reac, nm, dscr, is_f, cb, ub):
    #a = Reaction.objects.get_or_create(id_reaction=id_reac, name=nm, description=dscr, is_favorite=is_f, created_by=cb, created_date=cd, updated_by=ub, updated_date=ud)[0]
    a = Reaction.objects.get_or_create(id_reaction=id_reac, name=nm, description=dscr, is_favorite=is_f, created_by=cb, updated_by=ub)[0]
    a.save()
    return a

def add_user_reaction(reac,us,is_ow):
    #a = Reaction.objects.get_or_create(id_reaction=id_reac, name=nm, description=dscr, is_favorite=is_f, created_by=cb, created_date=cd, updated_by=ub, updated_date=ud)[0]
    a = User_reaction.objects.get_or_create(reaction=reac,user=us,is_owner=is_ow)[0]
    a.save()
    return a

def add_substance(id_s,nm,ch,is_r,fb,nt):
    a = Substance.objects.get_or_create(id_substance=id_s,name=nm,charge=ch,is_radical=is_r,formula_brutto=fb,note=nt)[0]
    a.after_create()
    a.save()
    return a

def add_reac_subst(r,s,al,bfs,nt):
    a = Reaction_subst.objects.get_or_create(reaction=r,substance=s,alias=al,brutto_formula_short=bfs,note=nt)[0]
    a.after_create()
    a.save()
    return a

def add_reac_scheme(id_s,r,nm,descr,is_p,cb,ub):
    a = Reaction_scheme.objects.get_or_create(id_scheme=id_s,reaction=r,name=nm,description=descr,is_possible=is_p,created_by=cb,updated_by=ub)[0]
    a.save()
    return a

def add_scheme_step(id_s,s,nm,od,is_r,nt,re, bl):
    a = Scheme_step.objects.get_or_create(id_step=id_s,scheme=s,name=nm,order=od,is_revers=is_r,note=nt,rate_equation=re, is_good_balance = bl)[0]
    a.save()
    return a

def add_scheme_step_subst(id_s,s,rs,p,sk):
    a = Scheme_step_subst.objects.get_or_create(id_step=id_s,step=s,reac_substance=rs,position=p,stoich_koef=sk)[0]
    a.save()
    return a

def add_exper(id_e,r,am,fm,ifm,des,id_f,id_a,ed,ub,is_f,nm,cb):
    a = Experiment.objects.get_or_create(id_experiment=id_e,reaction=r,argument_measure=am,function_measure=fm,init_function_measure=ifm,description=des,func=id_f,arg=id_a,exper_date=ed,updated_by=ub,is_favorite=is_f,name=nm,created_by=cb)[0]
    a.save()
    return a

def add_substance_consist(s,a,ac):
    a = Substance_consist.objects.get_or_create(substance=s,atom=a,atom_count=ac)[0]
    a.save()
    return a

def add_exper_subst(id_es,e,rs,dsr,io,ifv):
    a = Exper_subst.objects.get_or_create(id_expersubst=id_es,experiment=e,reaction_subst=rs,dict_subst_role=dsr,is_observed=io,init_func_val=ifv)[0]
    a.save()
    return a

def add_exper_serie(id_s,react,n,d):
    a = Exper_serie.objects.get_or_create(id_serie=id_s,reaction=react,name=n,description=d)[0]
    a.save()
    return a


def add_exper_point(ip,es,av,fv):
    a = Exper_point.objects.get_or_create(id_point=ip,exper_subst=es,arg_val=av,func_val=fv)[0]
    a.save()
    return a

def add_reaction_feature(irf,r,f):
    a = Reaction_feature.objects.get_or_create(id_reaction_feature=irf,reaction=r,feature=f)[0]
    a.save()
    return a

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    drop_all()
    populate()
    print "Data successfully added!"
