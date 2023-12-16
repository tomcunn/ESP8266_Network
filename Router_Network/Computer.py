import pygame
import socket
import time
import select


print("starting program")

counter = 0

# Create a class that stores all of the parameters regarding the tractors
class ESP8266_Connection:
    def __init__(self,name):
        self.name = name
        self.address = ('0.0.0.0',10000)
        self.connection = False
    
    def register(self,data,addr):
        if(self.connection == False):
            if(data.decode() == self.name):
                self.connection = True
                self.address = addr
                print(str(self.name) + " Connected @ " + str(self.address))
                    

#Manage the overall UDP Interface
class UDP_Connection:
    def __init__(self):
        UDP_SERVER = "192.168.0.173"
        UDP_PORT = 5000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((UDP_SERVER,UDP_PORT))
        self.server.setblocking(0)

    def packetsend(self,dataToSend,connection):
        self.server.sendto(dataToSend.encode(),connection.address)


myUDP = UDP_Connection()

tractor_grey =      ESP8266_Connection("Rover_Grey")
tractor_orange =    ESP8266_Connection("Rover_Orange")
IR_Camera =         ESP8266_Connection("IR_Camera")

ConnectionList = [tractor_grey,tractor_orange,IR_Camera]

# Main Loop
while(True):
    
    ready = select.select([myUDP.server], [], [], 0.1)
    if ready[0]:
        data,addr = myUDP.server.recvfrom(100)

        #Check to see if this is from a new address, check the connection list
        for myConnection in ConnectionList:
             myConnection.register(data,addr)

        if(data):
            counter=counter+1
  #     print(str(data) + ","+ str(addr) + "," + str(counter));
    
    #print("not blocking no more")
    
    if(tractor_grey.connection == True):
        myUDP.packetsend("This is for the grey tractor",tractor_grey)
    
    if(tractor_orange.connection == True):
        print("Send to" + str(tractor_orange.address))
        myUDP.packetsend("This is for the orange tractor",tractor_orange)
