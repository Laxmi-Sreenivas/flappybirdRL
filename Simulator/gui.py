'''
- GUI of Simulator
- Updates Based on State Change From Simulator
    - Bird Location
    - Pipe Location
'''
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 
import pygame 

import copy
import Simulator.config as config

class GUI:
    def __init__(self,pipe_info,pipe_gap):
        pygame.init() #Simulation Begins
        self.pipe_gap = pipe_gap

        #Importing Images
        self.images  = {}
        self.loadAssests()

        #Window Settings
        self.window = pygame.display.set_mode(config.window_size) #Game Screen Size
        pygame.display.set_icon(self.images["birdDownFlap"]) #Game Icon
        pygame.display.set_caption('Flappy Bird')  #Game Caption

        #Display Settings
        self.update(copy.deepcopy(config.origin),pipe_info) #Intially Player at Origin

    #Loading Images
    def loadAssests(self):
        self.images["background"] = pygame.image.load('./Simulator/assets/background-day.png')
        self.images["base"] = pygame.image.load('./Simulator/assets/base.png')
        self.images["pipe"] = pygame.image.load('./Simulator/assets/pipe-green.png')
        self.images["flipped pipe"] = pygame.transform.flip(self.images["pipe"], False, True)
        self.images["birdDownFlap"] = pygame.image.load('./Simulator/assets/redbird-downflap.png')
        self.images["birdMidFlap"] = pygame.image.load('./Simulator/assets/redbird-midflap.png')
        self.images["birdUpFlap"] = pygame.image.load('./Simulator/assets/redbird-upflap.png')

    #Renders Pipes
    def renderPipes(self,player_pos,pipe_info):
        for (xPos,yPos) in pipe_info:
            #Lower Pipe Creation
            #lower pipe -> pipe_gap//2 units below ypos
            #pipe start from xpos and ends at xPos + pipe_width
            lower_pipe_pos = (xPos-player_pos[0],yPos+self.pipe_gap//2) #Relative Position of Lower Pipe
            lower_pipe_size = (config.pipe_width, config.window_size[1] - config.groundLevel - lower_pipe_pos[1])

            #Upper Pipe Creation
            #upper pipe -> pipe_gap//2 units above ypos
            #pipe start from xpos and ends at xPos + pipe_width
            upper_pipe_pos = (xPos-player_pos[0],0) #Relative Position of Upper Pipe
            upper_pipe_size = (config.pipe_width,yPos - self.pipe_gap//2)

            #Putting Pipes on Screen
            self.window.blit(pygame.transform.scale(self.images["pipe"], lower_pipe_size),lower_pipe_pos)
            self.window.blit(pygame.transform.scale(self.images["flipped pipe"],upper_pipe_size),upper_pipe_pos)


    #Updates Screen
    def update(self,player_pos,pipe_info):
        #Putting Objects on Screen
        self.window.blit(pygame.transform.scale(self.images["background"], config.window_size),(0,0)) #BackGround
        
        self.window.blit(pygame.transform.scale(self.images["base"],
                            (config.window_size[0],config.groundLevel)),
                                (0,config.window_size[1]-config.groundLevel)) #Base
        
        self.window.blit(pygame.transform.scale(self.images["birdUpFlap"], 
                            (config.bird_size,config.bird_size)), 
                                (config.origin[0],player_pos[1])) #Bird  
        
        self.renderPipes(player_pos,pipe_info) #Pipes

        #Actual Screen Update
        pygame.display.update()

    #Closing GUI Window
    def __del__(self):
        pygame.quit() #Simulation Ends