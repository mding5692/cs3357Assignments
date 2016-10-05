import socket

TCP_IP = '10.0.2.15'
TCP_PORT = 5005

print ("Attempting to contact server at ",TCP_IP,":",TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print ("Connection to Server Established")
s.close()