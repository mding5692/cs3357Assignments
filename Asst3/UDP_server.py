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

while 1:
    # Data is received from socket
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)

    # Prints out received UDP packet
    print('received from:', addr)
    print('received message:', UDP_Packet)

    # uses references for the ack, seq, data and chksum
    reqAck = UDP_Packet[0]
    reqSeq = UDP_Packet[1]
    reqData = UDP_Packet[2]
    reqChksum = UDP_Packet[3]

    #Create the Checksum for comparison
    values = (reqAck,reqSeq,reqData)
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding='UTF-8')

    #Compare Checksums to test for corrupt data
    if reqChksum == chksum:
        print('Chksum is correct, Request data: ', reqData.decode("utf-8"))

        # Assigns different seq for response
        if reqSeq == 0:
            respSeq = 1
        else:
            respSeq = 0

        # Same ack sent back
        respAck = reqAck

        # Creates checksum for response and puts response into packet
        response = (respAck,respSeq,reqData)
        print("Response sent: ", response)
        UDP_Data = struct.Struct('I I 8s')
        resp_data = UDP_Data.pack(*response)
        respChksum =  bytes(hashlib.md5(resp_data).hexdigest(), encoding='UTF-8')
        response = (respAck,respSeq,reqData,respChksum)
        UDP_Data = struct.Struct('I I 8s 32s')
        UDP_Packet = UDP_Data.pack(*response)

        # Sends same ACK to indicate not corrupt
        sock.sendto(UDP_Packet,addr)
    else:
        # indicates that packet is corrupt
        print('Checksums Do Not Match, Packet Corrupt')

        # Sends previous ACK to represent NACK
        if reqAck == 1:
            respAck = 0
        else:
            respAck = 1

        # Creates checksum for response and puts into packet
        response = (respAck,respSeq,reqData)
        print("Response sent: ", response)
        UDP_Data = struct.Struct('I I 8s')
        resp_data = UDP_Data.pack(*response)
        respChksum =  bytes(hashlib.md5(resp_data).hexdigest(), encoding='UTF-8')
        response = (respAck,respSeq,reqData,respChksum)
        UDP_Data = struct.Struct('I I 8s 32s')
        UDP_Packet = UDP_Packet_Data.pack(*response)

        # Sends different ACK to indicate corrupted data
        sock.sendto(UDP_Packet,addr)        
