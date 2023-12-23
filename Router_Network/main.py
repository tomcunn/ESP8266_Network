import pygame
import socket
import time
import select
import WifiConnection as wifi
import  JoystickControl as joy


print("starting program")

counter = 0

##################### INIT ########################################
myUDP = wifi.UDP_Connection()

tractor_grey =      wifi.ESP8266_Connection("Rover_Grey")
tractor_orange =    wifi.ESP8266_Connection("Rover_Orange")
IR_Camera =         wifi.ESP8266_Connection("IR_Camera")

ConnectionList = [tractor_grey,tractor_orange,IR_Camera]

################ PYGAME INIT ###############################
pygame.init()

myJOY = joy.GamePadController()

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


    #Read in the joystick data
    x,y = myJOY.GetJoyStickData()

    print(x,y)

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
        datatoSend = bytes([0x4D,speed,speed])
        myUDP.packetsend3(datatoSend,tractor_grey)
        #print("sending data")
    if(tractor_orange.connection == True):
      #  print("Send to" + str(tractor_orange.address))
        #myUDP.packetsend("This is for the orange tractor",tractor_orange)
        datatoSend = bytes([0x4D,speed,speed])
        myUDP.packetsend3(datatoSend,tractor_orange)

    time.sleep(0.02)
