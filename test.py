# coding: utf-8
from socket import *

addr = (gethostbyname("localhost"), 65007)
sock = socket(AF_INET, SOCK_DGRAM)

def send(offset, byte):
    str = offset + byte + ";"
    sock.sendto(str.encode('utf-8'), addr)
    print("sent: " + str)

send("00", "F")
send("01", "A")

sock.close()
