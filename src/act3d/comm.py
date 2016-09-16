from act3d.constants import *

UDPinUSE = False

def send_msg(str):
    global UDPinUSE
    while UDPinUSE==True:
        pass ###wait
    UDPinUSE = True
    sock_send.sendto(str,(UDP_S_IP,UDP_S_PORT))
    try:
        data,addr = sock_rcv.recvfrom(BUFF)
    except socket.error as err:
        rospy.logerr("Error message received:%s", err)
        data = err
    return data
    #UDPinUSE = False
    

###init####
def startup():
    global UDPinUSE 
    sock_rcv.bind((UDP_R_IP,UDP_R_PORT))

    syscheck = "get system arm;"
    response = send_msg(syscheck); UDPinUSE = False
    reply = act3d.gen_msg(response)
    if reply[1][0]=='left':
        setup="set all enabled 0;remove all;set cursor resetforcesensor false;set cursor respondtoforce true;"+\
            "set cursor inertia [10,10,10];set cursor maxvelocity 0.2;"
    else:
        setup="set all enabled 0;remove all;set cursor resetforcesensor false;set system arm left;"+\
            "set cursor inertia [10,10,10];set cursor maxvelocity 0.2;"
    data = send_msg(setup); UDPinUSE = False
    data=send_msg(IDLE); UDPinUSE = False
    
    active = False
    print "Use the ACT3D to define a safe workspace. When you have done so, switch out of teaching mode."
    while active == False:
        switch = raw_input("Have you switched to active mode?[y/n]")
        if switch == 'y' or switch == "Y" or switch == "yes" or switch == "Yes":
            active = True

    #######Switch from TEACHING mode to ACTIVE mode ########################

    startup="set cursor resetforcesensor 0;set cursor inertia ["+DELIM.join(map(str,INERTIA_INIT))+"];set cursor respondtoforce false;"+\
        "set cursor maxvelocity 0.1;create spring sp1;set sp1 stiffness ["+ DELIM.join(map(str,K_INIT))+"];"+\
        "set sp1 position ["+DELIM.join(map(str,HOME))+"];set sp1 enabled 1;create damper ds;set ds dampcoeff ["+\
        DELIM.join(map(str,DAMP_INIT))+"];set ds enabled 1;"

    data = send_msg(startup); UDPinUSE = False
    #Set robot into centering position.
    print "Go to Home position."
    time.sleep(2.0)
    data=send_msg(ON); UDPinUSE = False
    homing = True
    msg = "get cursor modelpos;get cursor modelvel;"
    data = send_msg(ON); UDPinUSE = False
    while homing == True:
        data=send_msg(msg); UDPinUSE = False
        reply = act3d.parser(data)   
        if np.linalg.norm(np.array(reply[1])-np.array(HOME))<0.001 and np.linalg.norm(reply[2])<0.01:
            data=send_msg(IDLE); UDPinUSE = False
            homing = False
        time.sleep(0.1)
    print "SAFE!"
    time.sleep(1.5)
    return
    


########Communication timer######
def get_cursor_state():
    global UDPinUSE
    msg = "get cursor modelpos;get cursor modelvel;get cursor modelacc;get cursor measforce;"
    stateinfo=send_msg(msg); UDPinUSE = False
    reply = act3d.parser(stateinfo)#format should be [timestamp,[pos],[vel],[acc],[force]]
    sys_time=reply[0]
    pos = reply[1]
    vel = reply[2]
    acc = reply[3]
    force = reply[4]
    return [sys_time,pos,vel,acc,force]

####shutdown procedure####
def shutdown():
    global UDPinUSE
    UDPinUSE=False
    response = send_msg(IDLE); UDPinUSE = False
    offmsg = "set all enabled false;set cursor respondtoforce false;set cursor inertia ["+DELIM.join(map(str,INERTIA_INIT))+"];"+\
        "set cursor maxvelocity 0.2;"
    response = send_msg(offmsg); UDPinUSE = False
    print "NACT3D resetting before shutdown"

