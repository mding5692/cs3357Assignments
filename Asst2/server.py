# For commandline - type python server.py and then wait for client requests

import socket
# Uses datetime library to get current data and format it in response
from datetime import datetime

# Server address and port used as configuration
TCP_IP = '192.168.40.1'
TCP_PORT = 5005

# Creates socket using python socket library
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binds to configured server address
s.bind((TCP_IP, TCP_PORT))
# listens to server and indicates to user
s.listen(1)
print("Server is listening at Port", TCP_IP)

# while loop that keeps running server and listening for client requests until exit command sent by client
while 1:
    # creates a default error response in case bad input is sent in 
    response = "Error: no valid data sent through"
    # connection is established
    conn, addr = s.accept()
    # indicates to user when connected
    print("Client Address: ", addr)
    print("Connection to Client Established...")
    # client request is processed and decoded
    request = conn.recv(1024).decode()
    # Client request indicated by server
    print("Client request: ", request)
    # Checks if request is valid, and creates a new datetime and closes server is exit is sent, else just sends error message
    if request == "What is the current date and time?":
        # Changes to current date if valid request
        currTime = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
        response = "Current Date and Time: %s " % currTime
    elif request == "exit":
        # Else if request is to exit, it closes server and breaks out of while loop
        print("Client sent request to stop server!")
        break
    conn.send(response.encode())
    # Sends the response to client
    print("Response has been sent to client")
# Closes server depending on if while loop is broken
conn.close()

