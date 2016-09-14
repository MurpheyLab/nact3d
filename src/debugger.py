import act3d
from act3d.constants import *

setup="set all enabled 0;remove all;set system arm left;set cursor resetforcesensor false;"
#setup="set cursor resetforcesensor false;set system arm left;"
sock_send.sendto(setup,(UDP_S_IP,UDP_S_PORT))
try:
    data,addr = sock_rcv.recvfrom(BUFF)
    print data
except socket.error as err:
    print err
    
statemsg = "get state;"
sock_send.sendto(statemsg,(UDP_S_IP,UDP_S_PORT))
try:
    data,addr = sock_rcv.recvfrom(BUFF)
    print data
except socket.error as err:
    print err


startup="set cursor resetforcesensor 0;set cursor inertia "+str(INERTIA_INIT)+";set cursor respondtoforce false;"+\
    "set cursor maxvelocity 0.1;create spring sp1;set sp1 stiffness "+str(K_INIT)+";set sp1 position "+str(HOME)+";"+\
    "set sp1 enabled 1;create damper ds;set ds dampcoeff "+str(DAMP_INIT)+";set ds enabled 1;"
sock_send.sendto(startup,(UDP_S_IP,UDP_S_PORT))
try:
    data,addr = sock_rcv.recvfrom(BUFF)
    print data
except socket.error as err:
    print err
    
#Set robot into centering position.
print "Go to Home position"

homing = True
msg = "get cursor modelpos;get cursor modelvel;"
while homing == True:
    sock_send.sendto(msg,(UDP_S_IP,UDP_S_PORT))
    try:
        data,addr = sock_rcv.recvfrom(BUFF)
        print data
    except socket.error as err:
        print err
        reply = act3d.parser(data)   
    if np.linalg.norm(np.array(reply[1])-np.array(HOME))<0.001 and np.linalg.norm(reply[2])<0.01:
        homing = false
    time.sleep(0.1)
print "SAFE!"
time.sleep(1.5)

msg = "set cursor maxvelocity "+str(MAX_VEL)+";set cursor respondtoforce true;"
sock_send.sendto(msg,(UDP_S_IP,UDP_S_PORT))
try:
    data,addr = sock_rcv.recvfrom(BUFF)
    print data
except socket.error as err:
    print err    
   
