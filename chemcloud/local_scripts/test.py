def decorate_formula(s):
     numbers = ['0','1','2','3','4','5','6','7','8','9']
     formula=''
     num=''
     for i in s:
         if s in numbers:
             num= num+s
             print('num '+num)
         else:
             if num > '':
                 num='<sub>'+num+'</sub>'
                 print('num '+num)
             formula=formula+num+s
             print('formula '+formula)
             num=''
     print('formula '+formula)
     return formula

if __name__ == '__main__':
    decorate_formula('H2O')
