
import act3d
from act3d.constants import *
"""
act3d.startup()
reply = act3d.get_cursor_state()
"""
sock_rcv.bind((UDP_R_IP,UDP_R_PORT))

sock_rcv.listen(4) 
client_socket, client_address = sock_rcv.accept()
print(client_address, "has connected")
while 1==1:
    recvieved_data = s.recv(1024)
    print(recvieved_data)
