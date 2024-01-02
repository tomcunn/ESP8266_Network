import pygame
import socket
import time
import select
import WifiConnection as wifi
import JoystickControl as joy
import controls
import graphics
import IRCamera

print("starting program")
red = (255,0,0)
green = (0,255,0)

counter = 0

def RX_Data():
    data = [0x00,0x00,0x00]
    ready = select.select([myUDP.server], [], [], 0.1)
    if ready[0]:
        data,addr = myUDP.server.recvfrom(100)

        #If the first data byte is 0x80, do not check the register
        if (data[0] != 0x80):
            #Check to see if this is from a new address, check the connection list
            for myConnection in ConnectionList:
                dataToSend = myConnection.register(data,addr)
                myUDP.packetsend2(dataToSend,addr)

    return data

##################### INIT ########################################
myUDP = wifi.UDP_Connection()

tractor_grey =      wifi.ESP8266_Connection("Rover_Grey")
tractor_orange =    wifi.ESP8266_Connection("Rover_Orange")
IR_Camera =         wifi.ESP8266_Connection("IR_Camera")

ConnectionList = [tractor_grey,tractor_orange,IR_Camera]
myGraphics = graphics.graphics()
myJOY = joy.GamePadController()

run_loop = True


################ MAIN LOOP ########################################
while(run_loop):

    #Process Incoming Data
    mydata = RX_Data()

    #Process Operator Inputs
    joyx,joyy = myJOY.GetJoyStickData()
    run_loop, key_press = myGraphics.events()

    myGraphics.AddMouseClicksToList()

    #Get position

    
    if (mydata[0] == 0x80):
        x1,y1,x2,y2 = IRCamera.ProcessCameraData(mydata)
        myGraphics.DrawPosition(x1,y1,red)
        myGraphics.DrawPosition(x2,y2,green)
    
    #Process Controls
    speedleft,speedright = controls.SpeedControlJoystick(joyx,joyy)
    #print(speedleft,speedright)

    keyspeedleft,keyspeedright  = controls.SpeedControlKeyboard(key_press)
    #print(keyspeedleft,keyspeedright)

    #Send outputs
    if(tractor_grey.connection == True):
        datatoSend = bytes([0x4D,int(speedleft),int(speedright)])
        myUDP.packetsend3(datatoSend,tractor_grey)

    if(tractor_orange.connection == True):
        datatoSend = bytes([0x4D,int(keyspeedleft),int(keyspeedright)])
        myUDP.packetsend3(datatoSend,tractor_orange)

    #Update graphics
    myGraphics.update()
    
