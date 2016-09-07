from act3d.constants import *

close = "set bf1 force [0,0,0];set all enabled 0;remove all;"
###init####
def startup():
    sock_rcv.bind((UDP_R_IP,UDP_R_PORT))
    setup="set all enabled 0;remove all;set system arm left;set cursor resetforcesensor 1;"
    sock_send.sendto(setup,(UDP_S_IP,UDP_S_PORT))
    
    startup="set cursor resetforcesensor 0;set cursor inertia "+str(INERTIA_INIT)+";set cursor respondtoforce false;\
        set cursor maxvelocity 0.1;create spring sp1;set sp1 stiffness "+str(K_INIT)+";set sp1 position "+str(homepos)+";\
        set sp1 enabled 1;create damper ds;set ds dampcoeff "+str(DAMP_INIT)+";set ds enabled 1;"
    sock_send.sendto(startup,(UDP_S_IP,UDP_S_PORT))
    
    #Set robot into centering position.
    print "Go to Home position"

    homing = True
    msg = "get cursor modelpos;get cursor modelvel;"
    while homing = True:
        sock_send.sendto(msg,(UDP_S_IP,UDP_S_PORT))
        try:
            data,addr = sock_rcv.recvfrom(BUFF)
        except socket.error as err:
            rospy.logger("Socket Error: {0}".format(err))
        reply = act3d.parser(data)   
        if np.linalg.norm(np.array(reply[1])-np.array(HOME))<0.001 and np.linalg.norm(reply[2])<0.01:
            homing = false
        time.sleep(0.1)
    print "SAFE!"
    time.sleep(1.5)

    msg = "set cursor maxvelocity "+str(MAX_VEL)+";set cursor respondtoforce true;"
    sock_send.sendto(msg,(UDP_S_IP,UDP_S_PORT))
    msg = "set sp1 stiffness "+str(K_DEFAULT)+";set sp1 position"+str(homepos)+";set sp1 enabled 1;\
        set ds dampcoeff "+str(DAMP_DEFAULT)+";set ds enabled 1;"
    sock_send.sendto(msg,(UDP_S_IP,UDP_S_PORT))

default_dyn = trepsys_dyn()
default_dyn.inertia = [60,60,60]
default_dyn.damp = DAMP_DEFAULT
#####set dynamics####
def set_dyn(sys_dyn=default_dyn):
    msg = "create biasforce bf1;set bf1 force [0,0,0];set cursor inertia "+str(sys_dyn.inertia)+";create damper d1;\
        set d1 dampcoeff "+str(sys_dyn.damp)+";set bf1 maxforce "+str(MAX_F)+";set bf1 enabled 1;set d1 enabled 1;"
    sock_send.sendto(msg,(UDP_S_IP,UDP_S_PORT))

########Communication timer######
def get_cursor_state():
    msg = "get cursor modelpos;get cursor modelvel;get cursor modelacc;get cursor measforce;"
    sock_send.sendto(msg, (UDP_S_IP,UDP_S_PORT))
    try:
        data,addr = sock_rcv.recvfrom(BUFF)
    except socket.error as err:
        rospy.logger("Socket Error: {0}".format(err))
    reply = act3d.parser(data)#format should be [timestamp,[pos],[vel],[acc],[force]]
    sys_time=reply[0]
    pos = reply[1]
    vel = reply[2]
    acc = reply[3]
    force = reply[4]
    return [sys_time,pos,vel,acc,force]
    
    
    
msg=parser(data)    
msg.multi_msg()