from act3d.constants import *

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
    


if __name__=='__main__':
    """
    MESSAGE = "get cursor modelpos;get cursor modelvel;get cursor modelacc;get cursor measforce;"

    sock_send.sendto(MESSAGE, (UDP_S_IP,UDP_S_PORT))
    try:
        data,addr = sock_rcv.recvfrom(BUFF)
        print "recieved message:",data
    except socket.timeout:
        rospy.logger("UDP comm timed out")
    except socket.error as err:
        rospy.logger("Socket Error: {0}".format(err))
    """
    
    test = '{1234}[1234,5678.25,146];{1234}[19.2];{1234}[586.34,789.23];{1234}[45286,125.668,256];'
    msg=parser(test)    
    print msg