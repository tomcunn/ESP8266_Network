import pygame
import socket
import time


print("starting program")


UDP_SERVER = "192.168.0.173"
UDP_PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((UDP_SERVER,UDP_PORT))
MESSAGE = b"CPU Message"

counter = 0

# Create a class that stores all of the parameters regarding the tractors
class IP_Connection:
    def __init__(self,name):
        self.name = name
        self.address = ('0.0.0.0',10000)
        self.connection = False

tractor_grey =      IP_Connection("Rover_Grey")
tractor_orange =    IP_Connection("Rover_Orange")
IR_Camera =         IP_Connection("IR_Camera")

# Main Loop
while(True):
    #Recieve a UDP packet    
    data, addr = server.recvfrom(1024) # buffer size is 1024 bytes
    
    #check to see if the request is to register
    if(tractor_orange.connection == False):    
        if(data.decode() == tractor_orange.name):
            tractor_orange.connection = True
            tractor_orange.address = addr
            print(str(tractor_orange.name) + " Connected @ " + str(tractor_orange.address))

    if(tractor_grey.connection == False):
        if(data.decode() == tractor_grey.name):
            tractor_grey.connection = True
            tractor_grey.address = addr
            print(str(tractor_grey.name) + " Connected @ "  + str(tractor_grey.address))

    if(IR_Camera.connection == False):
        if(data.decode() == IR_Camera.name):
            IR_Camera.connection = True
            IR_Camera.address = addr
            print("Camera Connected"  + str(IR_Camera.address))
        
    if(data):
        counter=counter+1
  #     print(str(data) + ","+ str(addr) + "," + str(counter));
    
    if(tractor_grey.connection == True):
        server.sendto("This is for the grey tractor".encode(),tractor_grey.address)
    
    if(tractor_orange.connection == True):
      #  print("Send to" + str(tractor_orange.address))
        server.sendto("This is for the orange tractor".encode(),tractor_orange.address)
