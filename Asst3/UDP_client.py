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
packets = ['NCC-1701','NCC-1664','NCC-1017']

#Assigns certain variables for ack and sequence number so easy to reference later on
ack = 0
seq = 0

# Loops through raw_data_list and sends each raw_data
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
	sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
	print("UDP Packet has been sent.")

	# Receives response from receiver
	resp, server_addr = sock.recvfrom(4096)
	print("Packet sent back from receiver: ", resp)

	# Unpacks response and gets ACK
	RESP_Packet = unpacker.unpack(resp)
	respAck = RESP_Packet[0]

	# Keeps looping and sending previous data if corrupted
	while respAck != ack: 
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

	# Assigns correct sequence number after checking if previous sent data is not corrupt
	correctRespSeq = RESP_Packet[1]

	# Switches up ack and seq for next packet
	seq = correctRespSeq
	if ack == 0:
		ack = 1
	else:
		ack = 0

# Close connection at the end
sock.close()
