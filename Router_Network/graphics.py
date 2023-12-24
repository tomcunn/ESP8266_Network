import pygame

class graphics:
    def __init__(self):
        pygame.init()

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