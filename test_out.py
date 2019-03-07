# coding: utf-8
from socket import gethostbyname, socket, AF_INET, SOCK_DGRAM

addr = (gethostbyname("localhost"), 65008)
sock = socket(AF_INET, SOCK_DGRAM)

def send(offset, byte):
    str = offset + byte + ";"
    sock.sendto(str.encode('utf-8'), addr)
    print("sent: " + str)

def sendb(offset, byte):
    send(offset, format(byte, '02x'))

# button test
send("48", "FF") #all 
send("49", "11") #none

sock.close()
