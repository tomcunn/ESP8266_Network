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
    ready = select.select([myUDP.server], [], [], 0.04)
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


hitch_pos = 90

run_loop = True


################ MAIN LOOP ########################################
while(run_loop):

    #Process Incoming Data
    mydata = RX_Data()

    #Process Operator Inputs
    joyx,joyy,x_button,b_button,a_button,y_button = myJOY.GetJoyStickData()
    run_loop, key_press = myGraphics.events()

    myGraphics.AddMouseClicksToList()

    #Process Hitch Controls
    hitch_pos = controls.HitchControl(hitch_pos,x_button,b_button)

    #Get position
    if (mydata[0] == 0x80):
        x1,y1,x2,y2 = IRCamera.ProcessCameraData(mydata)
        if(hitch_pos == 180):
            myGraphics.DrawPosition(x1,y1,red)
            myGraphics.DrawPosition(x2,y2,green)
        #print(x1,y1)

    #Process Controls
    speedleft,speedright = controls.SpeedControlJoystick(joyx , joyy)
    #print(int(speedleft),int(speedright))

    keyspeedleft,keyspeedright  = controls.SpeedControlKeyboard(key_press)
    #print(keyspeedleft,keyspeedright)

    #Send outputs
    if(tractor_grey.connection == True):
        datatoSend = bytes([0x4D,int(speedleft),int(speedright),int(hitch_pos),int(a_button),int(y_button)])
        myUDP.packetsend3(datatoSend,tractor_grey)
        #print(datatoSend)

    if(tractor_orange.connection == True):
        datatoSend = bytes([0x4D,int(speedleft),int(speedright),int(hitch_pos)])
        myUDP.packetsend3(datatoSend,tractor_orange)

    #Update graphics
    myGraphics.update()
    
