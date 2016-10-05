import socket

TCP_IP = '10.0.2.15'
TCP_PORT = 5005

def sendMessage(clientSocket, msg):
    clientSocket.send(msg.encode())
    print("Request has been sent from client")

def receiveResponse(clientSocket):
    response = clientSocket.recv(1024).decode()
    print("Response has been received from server")
    return response

print ("Attempting to contact server at ",TCP_IP,":",TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print ("Connection to Server Established")

message = "What is the current date and time?"
sendMessage(s,message)
print(receiveResponse(s))
s.close()