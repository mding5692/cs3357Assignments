import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = '127.0.0.1'
UDP_PORT = 5005
unpacker = struct.Struct('I I 32s')

print('UDP target IP:', UDP_IP)
print('UDP target port:', UDP_PORT)

# Creates the information to be sent through
raw_data_list = ['NCC-1701','NCC-1664','NCC-1017']

#Assigns certain variables for ack and sequence number so easy to reference later on
ack = 0
seq = 0

# Loops through raw_data_list and sends each raw_data
for raw_data in raw_data_list:

	# Converts raw_data from string into bytes
	raw_data_as_bytes = raw_data.encode("utf-8")

	#Create the Checksum
	values = (ack,seq,raw_data_as_bytes)
	UDP_Data = struct.Struct('I I 8s')
	packed_data = UDP_Data.pack(*values)
	chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding='UTF-8')

	#Build the UDP Packet
	values = (ack,seq,raw_data_as_bytes,chksum)
	UDP_Packet_Data = struct.Struct('I I 8s 32s')
	UDP_Packet = UDP_Packet_Data.pack(*values)

	#Send the UDP Packet
	sock = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP
	sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
	print("Sending Packet: ", values)
	print("UDP Packet has been sent.")

	# Receives response from receiver
	resp, server_addr = sock.recvfrom(4096)

	# Unpacks response to see values contained
	RESP_Packet = unpacker.unpack(resp)
	print("Packet sent back from receiver: ", RESP_Packet)

	# Assigns ack to variable currAck for comparison
	currSeq = seq
	respSeq = RESP_Packet[1]

	# Checks ack response and sends new packets based on that information
	while respSeq != currSeq: 
		print("Different ack recieved - corrupted data sent")
		sock = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP
		print("Resent packet: ", UDP_Packet)
		sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
		print("UDP Packet has been resent.") # sends packet again if previous packet was corrupted
		resp, server_addr = sock.recvfrom(4096) # receives new check
		print("Packet received from receiver ", resp)

		# Unpacks response to see values contained
		RESP_Packet = unpacker.unpack(resp)
		respAck = RESP_Packet[0]

	# Switches up seq for next packet
	if seq == 0:
		seq = 1
	else:
		seq = 0

# Close connection at the end
sock.close()
