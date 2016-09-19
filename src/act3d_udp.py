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
import act3d
from act3d.constants import *
    
class ACT3D_Communicator:
        
    def __init__(self):
        rospy.loginfo("Initializing ACT3D robot")
             
        # setup publishers, subscribers, timers:
        self.dyn_sub = rospy.Subscriber("cursor_dyn",cursor_dyn,self.set_dyn)
        #self.genmsg_sub = rospy.Subscriber("gen_msg",String,self.send_msg)
        self.cursor_pub = rospy.Publisher("cursor_state",cursor,queue_size=5)
        self.startup_pub = rospy.Publisher("act3d_ready",Bool,queue_size =1)
        
        self.cursor_state = cursor()
        act3d.startup()##don't start timer until after setup is complete
        self.init_standardComm()
        [self.cursor_state.sys_time,self.cursor_state.pos,self.cursor_state.vel,self.cursor_state.acc,self.cursor_state.force]\
            = act3d.get_cursor_state()
        self.cursor_pub.publish(self.cursor_state)
        self.startup_pub.publish(False)
        return
    
    def init_standardComm():
        self.update_timer = rospy.Timer(rospy.Duration(DT), self.timercb)
        self.bias_sub = rospy.Subscriber("cursor_bias", Float32MultiArray, self.set_bias)
        return
    
    def shutdowm_standardComm():
        self.update_timer.shutdown()
        self.bias_sub.unregister()
        return
    
    def timercb(self,data):
        [self.cursor_state.sys_time,self.cursor_state.pos,self.cursor_state.vel,self.cursor_state.acc,self.cursor_state.force]\
            = act3d.get_cursor_state()
        self.cursor_pub.publish(self.cursor_state)
                  
        return
    

    def set_bias(self,data):
        msg = "set bf1 force "+str(data)+";"
        response,_ = act3d.fedex.send_msg(msg)
        return
        
    def set_dyn(self,data):
        self.shutdowm_standardComm()
        rospy.loginfo("Setting Cursor dynamics.")
        msg = "set sp1 stiffness ["+DELIM.join(map(str,data.sp))+"];set sp1 position["+DELIM.join(map(str,HOME))+"];"+\
            "set sp1 enabled 1;set ds dampcoeff ["+DELIM.join(map(str,data.ds))+"];set ds enabled 1;"
        msg2 = "create biasforce bf1;set bf1 force [0.0,0.0,0.0];set cursor inertia ["+DELIM.join(map(str,data.inertia))+"];"+\
            "create damper d1;set d1 dampcoeff ["+DELIM.join(map(str,data.damp))+"];"+\
            "set bf1 maxforce ["+str(MAX_F)+"];set bf1 enabled 1;set d1 enabled 1;set cursor maxvelocity ["+str(data.maxvel)+"];"
        response,_ = act3d.fedex.send_msg(msg+msg2)
        response,_ = act3d.fedex.send_msg(act3d.ON+"set cursor respondtoforce true;")
        self.init_standardComm()
        self.startup_pub.publish(True)
        return
"""    
    def send_msg(self,data):
        response,_=act3d.fedex.send_msg(data)
        return
"""        
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
