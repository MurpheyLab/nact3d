
import act3d
from act3d.constants import *

act3d.startup()
reply = act3d.get_cursor_state()

"""
  
DELIM = ","
def single_gen(str1):
    if str1[str1.find("}")+1] == "[": 
        try:
            arr = [float(x) for x in str1[str1.find("}")+2:-1].split(DELIM,10)]
        except:
            arr = str1[str1.find("}")+2:-1]
    else : return str1[str1.find("}")+1:]
    return arr

def parser(string):
    msglist = [int(string[string.find('{')+1:string.find('}')])]
    str2 = string[string.find('}')+1:]
    str3 = [single_gen(x) for x in str2.split(";",30)[:-1]]
    msglist = msglist+str3
    return msglist

test="{3150538}[0.542323,-0.0105815,-0.0001724];{3150538}[0,0,0];{5678}Attribute set;Attribute set;{101213}[cmd_on];"


test2 = parser(test)
print test2

"""