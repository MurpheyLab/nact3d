from act3d.constants import *

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