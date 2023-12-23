import pygame
from JoystickControl import GamePadController 
import time



pygame.init()

Gamepad = GamePadController()

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Set the width and height of the screen [width,height]
size = [500, 980]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Joystick")

run_loop=True

while(run_loop):
    x,y  = Gamepad.GetJoyStickData()

    print(x,y)

    #Check for pygame events
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            run_loop=False # Flag that we are done so we exit this loop
     
    # Limit to 20 frames per second
    clock.tick(20)
