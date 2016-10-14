import socket
from datetime import datetime

TCP_IP = '192.168.56.1'
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Server is listening at Port", TCP_IP)

while 1:
    response = "Error: no valid data sent through"
    conn, addr = s.accept()
    print("Client Address: ", addr)
    print("Connection to Client Established...")
    request = conn.recv(1024).decode()
    print("Client request: ", request)
    if request == "What is the current date and time?":
        currTime = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
        response = "Current Date and Time: %s " % currTime
    elif request == "exit":
        print("Client sent request to stop server!")
        break
    conn.send(response.encode())
    print("Response has been sent to client")
conn.close()

