from act3d.constants import *

class UDP_sender:
    def __init__(self):
        self.UDPinUSE = False

    def send_msg(self,str):
        while self.UDPinUSE==True:
            pass ###wait
        self.UDPinUSE = True
        sock_send.sendto(str,(UDP_S_IP,UDP_S_PORT))
        try:
            data,addr = sock_rcv.recvfrom(BUFF)
        except socket.error as err:
            rospy.logerr("Error message received:%s", err)
            data = err
        return data, self.reset()
    
    def reset(self):
        self.UDPinUSE = False
        return

fedex = UDP_sender()

###init####
def startup():
    sock_rcv.bind((UDP_R_IP,UDP_R_PORT))
    syscheck = "get system arm;"
    response,_ = fedex.send_msg(syscheck)
    reply = act3d.parser(response)
    if reply[1][0]=='left':
        setup="set all enabled 0;remove all;set cursor resetforcesensor false;set cursor respondtoforce true;"+\
            "set cursor inertia [10,10,10];set cursor maxvelocity 0.2;"
    else:
        setup="set all enabled 0;remove all;set cursor resetforcesensor false;set system arm left;set cursor respondtoforce true;"+\
            "set cursor inertia [10,10,10];set cursor maxvelocity 0.2;"
    data,_ = fedex.send_msg(setup)
    data,_=fedex.send_msg(IDLE)
    
    active = False
    print "Use the ACT3D to define a safe workspace. When you have done so, switch out of teaching mode."
    while active == False:
        #print fedex.send_msg("get system state;get system statecmd;get cursor respondtoforce;")
        switch = raw_input("Have you switched to active mode?[y/n]")
        if switch == 'y' or switch == "Y" or switch == "yes" or switch == "Yes":
            active = True

    #######Switch from TEACHING mode to ACTIVE mode ########################

    startup="set cursor resetforcesensor 0;set cursor inertia ["+DELIM.join(map(str,INERTIA_INIT))+"];set cursor respondtoforce false;"+\
        "set cursor maxvelocity 0.1;create spring sp1;set sp1 stiffness ["+ DELIM.join(map(str,K_INIT))+"];"+\
        "set sp1 position ["+DELIM.join(map(str,HOME))+"];set sp1 enabled 1;create damper ds;set ds dampcoeff ["+\
        DELIM.join(map(str,DAMP_INIT))+"];set ds enabled 1;"

    data,_ = fedex.send_msg(startup)
    #Set robot into centering position.
    print "Go to Home position."
    time.sleep(2.0)
    data,_=fedex.send_msg(ON)
    homing = True
    msg = "get cursor modelpos;get cursor modelvel;"
    data,_ = fedex.send_msg(ON)
    while homing == True:
        data,_=fedex.send_msg(msg)
        reply = act3d.parser(data)   
        if np.linalg.norm(np.array(reply[1])-np.array(HOME))<0.001 and np.linalg.norm(reply[2])<0.01:
            data,_=fedex.send_msg(IDLE)
            homing = False
        time.sleep(0.1)
    print "SAFE! Please, hold still while the force sensor is zeroed."
    data,_=fedex.send_msg("set cursor resetforcesensor true;")
    time.sleep(3.0)
    data,_=fedex.send_msg("set cursor resetforcesensor false;")
    print "Force sensor zeroed."
    time.sleep(1.0)
    return
    


########Communication timer######
def get_cursor_state():
    msg = "get cursor modelpos;get cursor modelvel;get cursor modelacc;get cursor measforce;get cursor measjointangles;"
    stateinfo,_=fedex.send_msg(msg)
    reply = act3d.parser(stateinfo)#format should be [timestamp,[pos],[vel],[acc],[force]]
    sys_time=reply[0]
    pos = reply[1]
    vel = reply[2]
    acc = reply[3]
    force = reply[4]
    angle = reply[5]
    return [sys_time,pos,vel,acc,force,angle]

####shutdown procedure####
def shutdown():
    response,_ = fedex.send_msg(IDLE)
    offmsg = "set all enabled false;set cursor respondtoforce false;set cursor inertia ["+DELIM.join(map(str,INERTIA_INIT))+"];"+\
        "set cursor maxvelocity 0.2;"
    response,_ = fedex.send_msg(offmsg)
    print "NACT3D resetting before shutdown"
    #sock_rcv.shutdown(socket.SHUT_RD)
    sock_rcv.close()
    #sock_send.shutdown(socket.SHUT_RDWR)
    sock_send.close()

