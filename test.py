# coding: utf-8
from socket import *

addr = (gethostbyname("localhost"), 65007)
sock = socket(AF_INET, SOCK_DGRAM)

def send(offset, byte):
    str = offset + byte + ";"
    sock.sendto(str.encode('utf-8'), addr)
    print("sent: " + str)

def sendb(offset, byte):
    send(offset, format(byte, '02x'))

# 7seg test
send("00", "FF") #all 
send("01", "00") #none
sendb("02", 0b00000110) #1
sendb("03", 0b01011011) #2
sendb("04", 0b01001111) #3
sendb("05", 0b01100110) #4
sendb("06", 0b01101101) #5
sendb("07", 0b01111100) #6
sendb("08", 0b01010101) #?
sendb("09", 0b00000000) #
sendb("0A", 0b00000000)
sendb("0B", 0b00000000)

sock.close()
