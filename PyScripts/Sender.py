import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

data = 0000 # Will be a dynamically updating numpy array probably...

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.sendto(data, (UDP_IP, UDP_PORT))