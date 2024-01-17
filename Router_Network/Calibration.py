import pygame
import socket
import time
import WifiConnection as wifi
import IRCamera
import select


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

print("starting program")

pygame.init()
pygame.display.set_caption('Position System')
width, height = (1280,720)
surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
surface.fill(pygame.Color('#FFFFFF'))
print(width)
print(height)

##################### INIT ########################################
myUDP = wifi.UDP_Connection()
IR_Camera =         wifi.ESP8266_Connection("IR_Camera")

ConnectionList = [IR_Camera]

font = pygame.font.SysFont(None, 60)

pygame.draw.circle(surface, (0,255,0), (width/2,height/2), 20)
pygame.draw.circle(surface, (0,0,255), (100,100), 20)
pygame.draw.circle(surface, (0,0,255), (100,height-100), 20)
pygame.draw.circle(surface, (0,0,255), (width-100,100), 20)
pygame.draw.circle(surface, (0,0,255), (width-100,height-100), 20)
pygame.draw.circle(surface, (0,0,255), (width/2+200,height/2), 20)
pygame.draw.circle(surface, (0,0,255), (width/2-200,height/2), 20)

pygame.draw.circle(surface, (0,0,255), (width/2,height/2+200), 20)
pygame.draw.circle(surface, (0,0,255), (width/2,height/2-200), 20)

while(True):
#    
    #surface.fill(pygame.Color('#000000'))

    pygame.draw.circle(surface, (0,255,0), (width/2,height/2), 20)
    pygame.draw.circle(surface, (0,0,255), (width/2+200,height/2), 20)
    pygame.draw.circle(surface, (0,0,255), (width/2-200,height/2), 20)

    pygame.draw.circle(surface, (0,0,255), (width/2,height/2+200), 20)
    pygame.draw.circle(surface, (0,0,255), (width/2,height/2-200), 20)
    
    data = RX_Data()
    

        #Get position
    if (data[0] == 0x80):
        xpos,ypos,x2,y2 = IRCamera.ProcessCameraData(data)
        print(str(xpos) + ","+ str(ypos))
        pygame.draw.circle(surface, (0,0,0), (int(xpos*1.2269+19), int(height - (ypos*1.12994-188))), 40)
        surface.set_at((int(xpos*1.2269+19), int(height - (ypos*1.12994-188))), (255,0,255))
    
    
    img = font.render(str(xpos) + ","+ str(ypos), True, (0,120,120))
    surface.blit(img, (80, 80))


    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             is_running = False

    pygame.display.update()