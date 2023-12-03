import pygame
import socket
import time


print("starting program")

UDP_IP = "192.168.0.120"
UDP_PORT = 5000
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MESSAGE = b"CPU Message"
addr = (UDP_IP , UDP_PORT)
client.sendto(MESSAGE,addr)
print("Client connected")
is_running = True

while(is_running):
#    
    data, addr = client.recvfrom(1024) # buffer size is 1024 bytes
    #print("received message: %s" % data)
    if(data):
        print(str(data) + ","+ str(addr));

    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             is_running = False

    pygame.display.update()
