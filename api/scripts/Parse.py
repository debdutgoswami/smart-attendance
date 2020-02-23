from word2number import w2n
import json

def seperate(text: str, end: int, prevContext: int):
    final = list()
    prev = prevContext
    for i in text.split():
        try:
            num = int(w2n.word_to_num(i))
            if prev==num:
                continue
            if prev == None or prev+1 == num or (prev==1 and num==2):
                prev = num
                final.append(num)
            else:
                copy = int(str(num)[::-1])
                temp = set()
                while(copy!=0):
                    temp.add(copy%10)
                    prev = copy%10
                    copy//=10
                temp = sorted(list(temp))
                for t in temp:
                    final.append(t)
        except ValueError:
            final.append(i)

    return final
    '''for i in range(len(temp)):
        try:
            num = int(temp[i])
            if(len(str(temp[i]))>1 and ((i==0 and type(temp[i+1])==str and temp[i]>end) or )):
                prev = None
                copy = num
                while(copy>0):
                    a = copy%10
                    if prev==None or prev+1==a:
                        prev = a
                        final.append(a)
        except ValueError:
            final.append(i)'''

#print(seperate("123 222 absent 3456 7 7 7 absent eight nine 10 11 twelve 12 12 13 absent", 10))