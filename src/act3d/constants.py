import socket
import rospy
import time
import act3d
import numpy as np

DT = 1./100.

#####PORTS######
UDP_S_IP = "192.168.5.100"
UDP_S_PORT = 12346
UDP_R_IP = "192.168.5.99"
UDP_R_PORT = 12348
BUFF = 2048

sock_send = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock_rcv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock_rcv.settimeout(5.0)

##############
####ACT3D ####
##############
HOME = [0.65,0.02,-0.03]
INERTIA_INIT = [10.0,10.0,10.0]
DAMP_INIT = [20,20,20]
K_INIT = [30,30,30]
K_DEFAULT = [1000,0,1000]
DAMP_DEFAULT = [100,0,100]

MAX_VEL = 6
MAX_F = 100
DELIM = ","

###################
####ROS Imports####
###################
import rospy
from nact3d.msg import cursor
from nact3d.msg import cursor_dyn
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Float32

DEFAULT_DYN = cursor_dyn()
DEFAULT_DYN.inertia = [5.0,5.0,5.0]
DEFAULT_DYN.damp = [0.1,0.1,0.1]
DEFAULT_DYN.sp = K_DEFAULT
DEFAULT_DYN.ds = DAMP_DEFAULT

###############################
####ACT3D standard Commands####
###############################
ON = "set system statecmd cmd_on;"
IDLE = "set system statecmd cmd_idle;"
MOVE = "set cursor respondtoforce true;"
PAUSE = "set cursor respondtoforce false;"
