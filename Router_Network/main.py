import pygame
import socket
import time
import select
import WifiConnection as wifi
import JoystickControl as joy
import controls
import graphics

print("starting program")

counter = 0

def RX_Data():
    ready = select.select([myUDP.server], [], [], 0.1)
    if ready[0]:
        data,addr = myUDP.server.recvfrom(100)

        #Check to see if this is from a new address, check the connection list
        for myConnection in ConnectionList:
             myConnection.register(data,addr)


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

    #Process Vehicle Connections
    RX_Data()

    #Process Operator Inputs
    joyx,joyy = myJOY.GetJoyStickData()
    run_loop, key_press = myGraphics.events()

    #Process Location


    #Process Controls
    speedleft,speedright = controls.SpeedControlJoystick(joyx,joyy)
    #print(speedleft,speedright)

    keyspeedleft,keyspeedright  = controls.SpeedControlKeyboard(key_press)
    print(keyspeedleft,keyspeedright)

    #Send outputs
    if(tractor_grey.connection == True):
        datatoSend = bytes([0x4D,int(speedleft),int(speedright)])
        myUDP.packetsend3(datatoSend,tractor_grey)

    if(tractor_orange.connection == True):
        datatoSend = bytes([0x4D,int(keyspeedleft),int(keyspeedright)])
        myUDP.packetsend3(datatoSend,tractor_orange)

    #Update graphics
    myGraphics.update()
    
    #Check for data from tractors


    time.sleep(0.02)
