# -*- coding: utf-8 -*-

def check_blocks(s, begin, end):
    meetings = 0
    for c in s:
        if c == begin:
            meetings += 1
        elif c == end:
            meetings -= 1
            if meetings < 0:
                return False
    return meetings == 0

#пока просто добавляет тэги <sub> вокруг цифр
def decorate_formula(formula_s):
     numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
     formula=''
     num=''
     for s in formula_s:
         if s in numbers:
             num= num+s
         else:
             if num > '':
                 num='<sub>'+num+'</sub>'
             formula=formula+num+s
             num=''
     if num > '':
         num='<sub>'+num+'</sub>'
         formula=formula+num
     return formula