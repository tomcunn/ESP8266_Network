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
                datatoSend = bytes([0x49,0x50,0x4C])
                myUDP.packetsend2(datatoSend,self.address)
                    

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

    def packetsend2(self,dataToSend,addr):
        self.server.sendto(dataToSend,addr)

    def packetsend3(self,dataToSend,connection):
        self.server.sendto(dataToSend,connection.address)
##################### INIT ########################################
myUDP = UDP_Connection()

tractor_grey =      ESP8266_Connection("Rover_Grey")
tractor_orange =    ESP8266_Connection("Rover_Orange")
IR_Camera =         ESP8266_Connection("IR_Camera")

ConnectionList = [tractor_grey,tractor_orange,IR_Camera]

################ PYGAME INIT ###############################
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Multi Rover Control")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

run_loop = True
speed = 0x7D

################ MAIN LOOP ########################################
while(run_loop):

    #Check for pygame events
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            run_loop=False # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.KEYDOWN:
             # checking if key "A" was pressed
            if event.key == pygame.K_a:
                speed = 0x7D
                print(speed)
               
            # checking if key "Q" was pressed
            if event.key == pygame.K_q:
                speed = 0xFA
                print(speed)
        
            # checking if key "Z" was pressed
            if event.key == pygame.K_z:
                speed = 0x00
                print(speed)


    #Check for data from tractors
    ready = select.select([myUDP.server], [], [], 0.1)
    if ready[0]:
        data,addr = myUDP.server.recvfrom(100)

        #Check to see if this is from a new address, check the connection list
        for myConnection in ConnectionList:
             myConnection.register(data,addr)

        if(data):
            counter=counter+1
  #     print(str(data) + ","+ str(addr) + "," + str(counter));
    
    
    if(tractor_grey.connection == True):
        #myUDP.packetsend("This is for the grey tractor",tractor_grey)
        datatoSend = bytes([0x10,speed,speed])
        myUDP.packetsend3(datatoSend,tractor_grey)
        #print("sending data")
    if(tractor_orange.connection == True):
      #  print("Send to" + str(tractor_orange.address))
        #myUDP.packetsend("This is for the orange tractor",tractor_orange)
        datatoSend = bytes([0x4D,speed,speed])
        myUDP.packetsend3(datatoSend,tractor_orange)

    time.sleep(0.02)
