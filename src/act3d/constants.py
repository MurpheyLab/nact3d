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

sock_end = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock_rcv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

##############
####ACT3D ####
##############
HOME = [0.55,0.,0.]
INERTIA_INIT = [10,10,10]
DAMP_INIT = [20,20,20]
K_INIT = [30,30,30]
K_DEFAULT = [1000,0,1000]
DAMP_DEFAULT = [100,0,100]

MAX_VEL = 6
MAX_F = 100

