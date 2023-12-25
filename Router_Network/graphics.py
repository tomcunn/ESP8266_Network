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
red = (255,0,0)

field = np.zeros((WIDTH,HEIGHT))

point_list = []
np_points = np.array = []

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

        self.screen.fill(lightbrown)

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def draw(self):
         pygame.draw.circle(self.screen, (0,255,0), (250,250), 20)

    def update(self):
        self.draw()
        self.DrawBoundary()
        self.GeneratePath()
        pygame.display.update()

    def events(self):
        key_press = pygame.K_t
        self.key_press =  pygame.K_t
        run_loop = True
        self.mouse_click = False

        #Check for pygame events
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                run_loop=False # Flag that we are done so we exit this loop
        
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.KEYDOWN:
                key_press = event.key
                self.key_press = event.key

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_click = True
        
        return run_loop, key_press
    
    # Given two points,determine which pixels to color
    def DetermineWhichPixelsToColor(x1,y1,x2,y2,field):
        dx = x2 - x1
        dy = y2 - y1
        distance  = x2-x1
        for x in range(int(distance)):
            y = y1 + dy * (x - x1) / dx
            field[int(x1),int(y)] = 1

    
    def AddMouseClicksToList(self):
        if(self.mouse_click == True):
            pos = pygame.mouse.get_pos()
            point_list.append(pos)
            np_points.append(pos)
            pygame.draw.circle(self.screen,red,pos,4)
            print(np_points)

    def DrawBoundary(self):
        if(self.key_press == pygame.K_p):
            pygame.draw.polygon(self.screen, blue, point_list)
            field_size = 0
            percent_screen = 0
            ##Check every point to see if it is within the polygon
            #Check to see if the points are blue
            for x in range(WIDTH):
                for y in range(HEIGHT):
                    pixel_color = self.screen.get_at((x, y))
                    if(pixel_color[0] == 0 and pixel_color[1] == 0 and pixel_color[2] == 255):
                        field[x,y] = 10
                        field_size = field_size +1
                        
                        
            print("field scan complete")
            print("Field Size is: " + str(field_size) + " pixels")

            percent_screen = field_size/(WIDTH*HEIGHT)*100
            print("Field is: " + str(percent_screen) +" percent of screen")

    def GeneratePath(self):
         TOOL_SIZE = 10
         if(self.key_press == pygame.K_m):
            print("Generating Toolpaths")
            x_list = []
            #Create a list of X coordinates that have field in them
            print("Creating a list of x values that need a path")
            for x in range(WIDTH):
                for y in range(HEIGHT):
                    if(field[x,y] == 10):
                        x_list.append(x)
                        break
            #Based on the tool width, determine which points to act upon
            #Find the first point
            First_point = x_list[0] + TOOL_SIZE/2
            x_action_list=[First_point]
            last_point = x_list[len(x_list)- 1]
            print("First point: " + str(First_point))
            print("last point: " + str(last_point))


            