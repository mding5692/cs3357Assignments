import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = '127.0.0.1'
UDP_PORT = 5005
unpacker = struct.Struct('I I 32s')
timeOutValue = 9.0 # Specifies the time it takes to timeout

print('UDP target IP:', UDP_IP)
print('UDP target port:', UDP_PORT)

# Creates the information to be sent through
packets = ['NCC-1701','NCC-1664','NCC-1017']

#Assigns certain variables for ack and sequence number so easy to reference later on
ack = 0
seq = 0

# Sends each data as packet
for data in packets:

	# Converts raw_data from string into bytes
	dataBytes = data.encode("utf-8")

	#Create the Checksum
	values = (ack,seq,dataBytes)
	UDP_Data = struct.Struct('I I 8s')
	packed_data = UDP_Data.pack(*values)
	chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding='UTF-8')

	#Build the UDP Packet
	values = (ack,seq,dataBytes,chksum)
	UDP_Packet_Data = struct.Struct('I I 8s 32s')
	UDP_Packet = UDP_Packet_Data.pack(*values)

	#Send the UDP Packet
	sock = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP
	# Uses socket library's timeout function to handle timeouts
	while True:
		# Sends the UDP Packet
		print("Sent data:", values)
		sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
		print("UDP Packet has been sent.")

		# Sets timeout and receives response from receiver
		try:
			sock.settimeout(timeOutValue)
			resp, server_addr = sock.recvfrom(4096)
			print("Received response")
			if resp is not None: # breaks out of loop if we received it on time
				break
		# Else grabs exception from settimeout
		except socket.timeout:
			print("ERROR: Timer expired!")
			print("Sending packet again...")
			continue

	# Unpacks response and gets ACK
	RESP_Packet = unpacker.unpack(resp)
	print("Data received from server: ", RESP_Packet)
	respSeq = RESP_Packet[1]

	# Keeps looping and sending previous data if corrupted
	while respSeq != seq: 
		# indicate to user that packet being resent
		print("Data was corrupted")
		print("Resending previous packet")
		sock = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP
		sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
		resp, server_addr = sock.recvfrom(4096) # receives new check
		print("Packet sent back from receiver ", resp)

		# Unpacks response to see values contained
		RESP_Packet = unpacker.unpack(resp)
		respAck = RESP_Packet[0]

	# Switches up ack and seq for next packet
	if seq == 0:
		seq = 1
	else:
		seq = 0

# Close connection at the end
sock.close()
