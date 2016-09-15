#!/usr/bin/env python

"""
Katie fitzsimons

This node runs a timer that communicates with the NACT3D to get the position, velocity, 
acceleration, and force of the ACT3D system. It published these to the topic cursor_state 
and updates a biasforce based on the topic, cursor_bias.

SUBSCRIBERS:
    - cursor_bias (float32[])
    - cursor_dyn (cursor_dyn)
    - genmsg_sub(string)

PUBLISHERS:
    - cursor_state (nact3d/cursor)

SERVICES:

"""
import rospy

#from nact3d.msg import Floats
#from nact3d.msg import cursor
#from nact3d.msg import cursor_dyn
import act3d
from act3d.constants import *
    
class ACT3D_Communicator:

    def __init__(self):
        rospy.loginfo("Initializing ACT3D robot")
             
        # setup publishers, subscribers, timers:
        self.bias_sub = rospy.Subscriber("cursor_bias", Floats, self.set_bias)
        self.dyn_sub = rospy.Subscriber("cursor_dyn",cursor_dyn,self.set_dyn)
        self.genmsg_sub = rospy.Subscriber("gen_msg",String,self.send_msg)
        self.sim_timer = rospy.Timer(rospy.Duration(DT), self.timercb)
        self.cursor_pub = rospy.Publisher("cursor_state",cursor,queue_size=5)
        
        self.cursor_state = cursor()
        self.dyn_set = False
        act3d.startup()

        return
        
    def timercb(self,data):
        if not self.dyn_set:
            return
        [self.cursor.sys_time,self.cursor.pos,self.cursor.vel,self.cursor.acc,self.cursor.force]\
            = get_cursor_state()
        self.cursor_pub.publish(self.cursor)
                  
        return


    def set_bias(self,data):
        msg = "set bf1 force "+str(data)+";"
        sock_send.sendto(msg, (UDP_S_IP,UDP_S_PORT))
        return
        
    def set_dyn(self,data):
        msg = "set sp1 stiffness ["+DELIM.join(map(str,data.sp))+"];set sp1 position["+DELIM.join(map(str,HOME))+"];"+\
            "set sp1 enabled 1;set ds dampcoeff ["+DELIM.join(map(str,data.ds))+"];set ds enabled 1;"
        response = act3d.send_msg(msg)
        msg = "create biasforce bf1;set bf1 force [0,0,0];set cursor inertia ["+DELIM.join(map(str,data.inertia))+"];"+\
            "create damper d1;set d1 dampcoeff ["+DELIM.join(map(str,data.damp))+"];"+\
            "set bf1 maxforce ["+DELIM.join(map(str,MAX_F))+"];set bf1 enabled 1;set d1 enabled 1;"
        response = act3d.send_msg(msg)
        response = act3d.send_msg(ON)
        self.dyn_set = True
        return
    
    def send_msg(self,data):
        response=act3d.send_msg(data)
        return
        
def main():
    """
    Run the main loop, by instatiating a System class, and then
    calling ros.spin
    """
    rospy.init_node('act3d_udp', log_level=rospy.INFO)
    
    rospy.on_shutdown(act3d.shutdown)

    try:
        comm = ACT3D_Communicator()
    except rospy.ROSInterruptException: pass

    rospy.spin()


if __name__=='__main__':
    main()
