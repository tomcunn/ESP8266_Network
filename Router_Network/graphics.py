import pygame
import numpy as np
from enum import Enum

HEIGHT = 500
WIDTH = 500
REDRAW = 25

# Define some colors
darkgrey = (40, 40, 40)
lightgrey = (150, 150, 150)
lightbrown = (202,176,0)
darkbrown = (128,89,0)
blue = (0,0,255)

field = np.zeros((WIDTH,HEIGHT))

class Season(Enum):
    Tillage = 1
    Planting = 2
    Grow1 = 3
    Grow2 = 4
    Grow3 = 5
    FullGrown = 6
    Golden = 7
    Harvest = 8

class graphics:
    def __init__(self):
        pygame.init()
        self.season = Season.Tillage
        pygame.display.set_caption("Multi Rover Control")
        # Set the width and height of the screen [width,height]
        size = [500, 500]
        self.screen = pygame.display.set_mode(size)

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def draw(self):
         pygame.draw.circle(self.screen, (0,255,0), (250,250), 20)

    def update(self):
        self.draw()
        pygame.display.update()

    def events(self):
        key_press = pygame.K_t
        run_loop = True

        #Check for pygame events
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                run_loop=False # Flag that we are done so we exit this loop
        
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.KEYDOWN:
                key_press = event.key
        
        return run_loop, key_press
    
    # Given two points,determine which pixels to color
    def DetermineWhichPixelsToColor(x1,y1,x2,y2,field):
        dx = x2 - x1
        dy = y2 - y1
        distance  = x2-x1
        for x in range(int(distance)):
            y = y1 + dy * (x - x1) / dx
            field[int(x1),int(y)] = 1