import socket
from datetime import datetime

TCP_IP = '192.168.56.1'
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print('Server is listening at Port', TCP_IP)

def notifyThatServerIsConnected(conn, addr):
    print('Client Address:', addr)
    print("Connection to Client Established")

def showRequest(socket):
    print("Client request:", socket.recv(1024).decode())

def getCurrTime():
    currTime = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
    response = "Current Date and Time: %s " % currTime
    return response

def sendResponseToClient(socket,response):
    socket.send(response.encode())
    print("Response has been sent to client")

while 1:
    socket, address = s.accept()
    notifyThatServerIsConnected(socket,address)
    showRequest(socket)
    currDateTime = getCurrTime()
    sendResponseToClient(s, currDateTime)


