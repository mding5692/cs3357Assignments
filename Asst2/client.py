import socket

TCP_IP = '192.168.56.1'
TCP_PORT = 5005

print ("Attempting to contact server at ",TCP_IP,":",TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print ("Connection to Server Established")
breakStr = "---------------------------------"
print(breakStr)
print("Instructions: Type 'What is the current date and time?' to get current time and date.")
print("Else type 'exit' to stop server!")
print(breakStr)
message = input("Enter your message below: \n")
s.send(message.encode('utf-8'))
print("Request has been sent from client")
response = s.recv(1024).decode('utf-8')
print("Response has been received from server")
if response == "":
	print("Exited program and closed server successfully!")
else:
	print("Response: ", response)
s.close()
