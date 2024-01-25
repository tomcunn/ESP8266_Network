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

        self.foundcontrollerone = False
        self.foundcontrollertwo = False

        self.ControllerList = []

        #Find the ID of the joystick and init it
        if(joystick_count > 0):
            for x in range(joystick_count):
                name = pygame.joystick.Joystick(x).get_name()
                print(name)
                if(name == TARGET_JOYSTICK):
                    #Check to see if controller one is found
                    if(self.foundcontrollerone == False):
                        self.gamepad_ID = x
                        self.foundcontrollerone = True
                        print("Found Controller One")
                        print("Found gamepad controller : " +  str(self.gamepad_ID))
                        controller1 = self.SwitchController()
                        controller1.pad = pygame.joystick.Joystick(self.gamepad_ID)
                        #self.mypad =  pygame.joystick.Joystick(self.gamepad_ID)
                        #self.mypad.init()
                        controller1.pad.init()
                        self.ControllerList.append("controller1")

                    #Check to see f controlle two if found
                    elif(self.foundcontrollerone == True):
                        self.gamepad_ID = x
                        self.foundcontrollertwo = True
                        print("Found Controller Two")
                        print("Found gamepad controller : " +  str(self.gamepad_ID))
                        #self.mypad2 =  pygame.joystick.Joystick(self.gamepad_ID)
                        #self.mypad2.init()

                        controller2 = self.SwitchController()
                        controller2.pad = pygame.joystick.Joystick(self.gamepad_ID)
                        controller2.pad.init()
                        self.ControllerList.append("controller2")

    def UpdatedControllers(self):
        for i in self.ControllerList:
            self.SwitchController.update(i)

    class SwitchController:
        def __init__(self):
            self.pad = 0
            self.discovered = False
            self.joyx = 0
            self.joyy = 0
            self.a_button = 0
            self.b_button = 0
            self.x_button = 0
            self.y_button   = 0

        def update(self,controller):
            self.joyx =      controller.get_axis(0)
            self.joyy =      controller.get_axis(1)
            self.a_button =  controller.get_button(2)
            self.b_button =  controller.get_button(1)
            self.x_button =  controller.get_button(0)
            self.y_button =  controller.get_button(3)
            #Instance of mypads = Gamepad()
            # mypads.controller1.joyx
            #
    def GetJoyStickData(self,ID):
        x_pos = 0
        y_pos = 0
        x_button = 0
        b_button = 0
        a_button = 0
        y_button = 0 

        if(self.gamepad_ID != 99):
            if(ID == 1):
                x_pos = self.mypad.get_axis(0)
                y_pos = self.mypad.get_axis(1)
                x_button = self.mypad.get_button(2)
                b_button = self.mypad.get_button(1)
                a_button = self.mypad.get_button(0)
                y_button = self.mypad.get_button(3)
            elif(ID ==2 and self.foundcontrollertwo == True):
                x_pos = self.mypad2.get_axis(0)
                y_pos = self.mypad2.get_axis(1)
                x_button = self.mypad2.get_button(2)
                b_button = self.mypad2.get_button(1)
                a_button = self.mypad2.get_button(0)
                y_button = self.mypad2.get_button(3)
            #print(str(x_pos),str(y_pos))

        return x_pos,y_pos,x_button,b_button,a_button,y_button

