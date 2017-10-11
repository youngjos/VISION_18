import socket
import numpy as np

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

def sendNum(num) :
    data = (num).to_bytes(2, byteorder='big')
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(data, (UDP_IP, UDP_PORT))
    return

sendNum(28524)
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)



