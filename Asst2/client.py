import socket

# Used to configure server address and port for client to connect to
TCP_IP = '192.168.56.1'
TCP_PORT = 5005

# Indicates to user that client is sending request
print ("Attempting to contact server at ",TCP_IP,":",TCP_PORT)
# Socket setup to enable connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Indicates to user that client is connected
s.connect((TCP_IP, TCP_PORT))
print ("Connection to Server Established")
# Used to prompt user to ask question or else type exit to close the server
breakStr = "---------------------------------"
msgStr = "Enter your message below: \n"
print(breakStr)
print("Instructions: Type 'What is the current date and time?' to get current time and date.")
print("Else type 'exit' to stop server!")
print(breakStr)
# Stores user input as message and validates input
message = raw_input(msgStr)
# if message is blank, keeps prompting user
while message == "":
	message = raw_input(msgStr)
# sends to server as utf-8 string
s.send(message.encode('utf-8'))
# indicates to user that request has been sent
print("Request has been sent from client")
# Indicates and handles response from server
response = s.recv(1024).decode('utf-8')
print("Response has been received from server")
# Indicates to user if response is empty that server is closed, else prints response
if response == "":
	print("Exited program and closed server successfully!")
else:
	print("Response: ", response)
# Closes client
s.close()
