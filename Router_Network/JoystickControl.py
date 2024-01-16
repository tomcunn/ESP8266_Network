##################################################
#
#  Pygame Joystick input module
#
#  Use the get name funciton to identify which 
#  joystick that you want to use. 
#
###################################################

import pygame

TARGET_JOYSTICK = "Nintendo Switch Pro Controller"
#TARGET_JOYSTICK = "Afterglow Gamepad for PS3"

class GamePadController:
    def __init__(self):
        
        #init to 99, meaning that no joystick was found
        self.gamepad_ID = 99

        # Get count of joysticks
        print("Checking for Joysticks")
        joystick_count = pygame.joystick.get_count()
        print("Number of joysticks: {}".format(joystick_count))

        #Find the ID of the joystick and init it
        if(joystick_count > 0):
            for x in range(joystick_count):
                name = pygame.joystick.Joystick(x).get_name()
                print(name)
                if(name == TARGET_JOYSTICK):
                    self.gamepad_ID = x
                    print("Found gamepad controller : " +  str(self.gamepad_ID))
                    self.mypad =  pygame.joystick.Joystick(self.gamepad_ID)
                    self.mypad.init()


    def GetJoyStickData(self):

        x_pos = 0
        y_pos = 0

        if(self.gamepad_ID != 99):
            x_pos = self.mypad.get_axis(0)
            y_pos = self.mypad.get_axis(1)
            x_button = self.mypad.get_button(2)
            b_button = self.mypad.get_button(1)
            a_button = self.mypad.get_button(0)
            y_button = self.mypad.get_button(3)

            #print(str(x_pos),str(y_pos))

        return x_pos,y_pos,x_button,b_button,a_button,y_button
