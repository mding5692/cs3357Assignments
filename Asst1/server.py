import socket

TCP_IP = '192.168.56.1'
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Server Address:', TCP_IP)
print('Client Address:', addr)
print("Connection to Client Established")
conn.close()