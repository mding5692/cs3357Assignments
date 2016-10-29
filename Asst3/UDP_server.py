import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = '127.0.0.1'
UDP_PORT = 5005
unpacker = struct.Struct('I I 8s 32s')


#Create the socket and listen
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
print("Server set-up and listening at: ", UDP_IP)

while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)

    # Prints out received UDP packet
    print('received from:', addr)
    print('received message:', UDP_Packet)

    # assigns variables to hold ack and sequence numbers to make it easy to reference later
    ack = UDP_Packet[0]
    seq = UDP_Packet[1]

    #Create the Checksum for comparison
    values = (ack,seq,UDP_Packet[2])
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding='UTF-8')
    
    #Compare Checksums to test for corrupt data
    if UDP_Packet[3] == chksum:
        print('CheckSums Match, Packet OK')

    else:
        print('Checksums Do Not Match, Packet Corrupt')
        # Sends previous Ack to receiver to show that is corrupted
        sock.sendto(ack,addr)
