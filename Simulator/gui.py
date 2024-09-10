'''
- GUI of Simulator
- Updates Based on State Change From Simulator
    - Bird Location
    - Pipe Location
'''
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 
import pygame 

class GUI:
    def __init__(self,window_size,ground_level,pipe_info,pipe_gap,pipe_width):
        pygame.init() #Simulation Begins

        #Params
        self.pipe_gap = pipe_gap  #Gap Between Upper & Lower Pipe
        self.pipe_width = pipe_width #Width of Pipes
        self.ground_level = ground_level #Elevation of Pipes
        self.window_size = window_size  #Window Size
        self.pipe_info = pipe_info #Pipe Positions
        self.origin = (10,self.window_size[1]//2) #x-axis origin
        self.player_pos = self.origin #Actual Position

        #Importing Images
        self.images  = {}
        self.images["background"] = pygame.image.load('./Simulator/assets/background-day.png')
        self.images["base"] = pygame.image.load('./Simulator/assets/base.png')
        self.images["pipe"] = pygame.image.load('./Simulator/assets/pipe-green.png')
        self.images["flipped pipe"] = pygame.transform.flip(self.images["pipe"], False, True)
        self.images["birdDownFlap"] = pygame.image.load('./Simulator/assets/redbird-downflap.png')
        self.images["birdMidFlap"] = pygame.image.load('./Simulator/assets/redbird-midflap.png')
        self.images["birdUpFlap"] = pygame.image.load('./Simulator/assets/redbird-upflap.png')

        #Window Settings
        self.window = pygame.display.set_mode(self.window_size) #Game Screen Size
        pygame.display.set_icon(self.images["birdDownFlap"]) #Game Icon
        pygame.display.set_caption('Flappy Bird')  #Game Caption

        #Display Settings
        self.update(self.player_pos,self.pipe_info)

    #Renders Pipes
    def renderPipes(self):
        for (xPos,yPos) in self.pipe_info:
            #Lower Pipe Creation
            lower_pipe_pos = (xPos-self.player_pos[0],yPos+self.pipe_gap//2) #Relative Position of Lower Pipe
            lower_pipe_size = (self.pipe_width, self.window_size[1] - self.ground_level - lower_pipe_pos[1])

            #Upper Pipe Creation
            upper_pipe_pos = (xPos-self.player_pos[0],0) #Relative Position of Upper Pipe
            upper_pipe_size = (self.pipe_width,yPos - self.pipe_gap//2)

            #Putting Pipes on Screen
            self.window.blit(pygame.transform.scale(self.images["pipe"], lower_pipe_size),lower_pipe_pos)
            self.window.blit(pygame.transform.scale(self.images["flipped pipe"],upper_pipe_size),upper_pipe_pos)


    #Updates Screen
    def update(self,new_player_pos,new_pipe_info):
        #Updating Positions
        self.player_pos = new_player_pos 
        self.pipe_info  = new_pipe_info

        #Putting Objects on Screen
        self.window.blit(pygame.transform.scale(self.images["background"], self.window_size),(0,0)) #BackGround
        self.window.blit(pygame.transform.scale(self.images["base"],(self.window_size[0],self.ground_level)),(0,self.window_size[1]-self.ground_level)) #Base
        self.window.blit(self.images['birdUpFlap'], self.origin) #Bird  
        self.renderPipes() #Pipes

        #Actual Screen Update
        pygame.display.update()

    #Closing GUI Window
    def __del__(self):
        pygame.quit() #Simulation Ends