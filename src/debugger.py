#import act3d
#from act3d.constants import *

#act3d.startup()
#reply = act3d.get_cursor_state()
DELIM = ","
def single_msg(str1):
    str1=str1[str1.find('[')+1:str1.find(']')]
    j=10
    arr=[]
    while j>0:
        j=str1.find(',')
        if j >0:
            arr.append(float(str1[:j]))
            str1=str1[j+1:]
        else:
            arr.append(float(str1))
    return arr
    
def parser(string):
    msglist = [int(string[string.find('{')+1:string.find('}')])]
    
    str2 = string[string.find('}')+1:]
    j=1
    while j>0:
        j=str2.find(';')
        if j>0:
            msglist.append(single_msg(str2[:j]))
            str2=str2[j+1:]
    return msglist
            
def single_gen(str1):
    if str1[0] == "[": arr = [float(x) for x in str1[1:-1].split(DELIM,10)]
    else : return str1
    return arr

def gen_msg(string):
    msglist = [int(string[string.find('{')+1:string.find('}')])]
    str2 = string[string.find('}')+1:]
    str3 = [single_gen(x) for x in str2.split(";",30)[:-1]]
    msglist = msglist+str3
    return msglist

test="{1234}[5.6,7.89,10];[11,12,13.14];Attribute set;Attribute set;"


test2 = gen_msg(test)
print test2

