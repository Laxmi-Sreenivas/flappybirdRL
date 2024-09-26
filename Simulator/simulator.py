'''
- Updates the Environment Given The Information
- Updates the Environment GUI aswell
- Relays back the new State to Manager
- Environment Info :
    - How far should Pillars be 
    - What the height difference of Pillars Should Be
    - How Big the Gap Should be 
'''
from Simulator.gui import GUI
import Simulator.config as config
import random
import copy
import json

class Simulator :
    def __init__(self,info,address):
        self.__address = address
        info = json.loads(info)

        #Loading Simulator Level Info
        self.xGap = info["xGap"] #Spacing Across x Axis
        self.yGap = info["yGap"] #Max Spacing Across y Axis
        self.hGap = info["hGap"] #Hole Size between the Pipes
        self.player_speed = info["xSpeed"] #Player Movement Speed
        self.player_jump  = info["ySpeed"] #Player Jump Speed

        print(f'Client{self.__address} : Simulation Begins')
        
        #Generating Pipes In Simulation Range
        self.pipesInfo = [] #No Pillar State
        self.player_pos = copy.deepcopy(config.origin) # Default Position of Player [Used For Reset]
        self.reset()
            
        #GUI Setup
        self.gui = GUI(self.pipesInfo,self.hGap)
        print(f'Client{self.__address} : GUI Initalized')
    
    #Spawns a New Pipe Based on Previous Pipe
    def spawnNextPipe(self):
        #Y-Coordinate of Pipe
        yPrev = self.pipesInfo[-1][1]
        yPos = random.randint(yPrev - self.yGap, yPrev + self.yGap)

        #X-Coordinate of Pipe
        xPrev = self.pipesInfo[-1][0]
        xPos = xPrev + self.xGap

        #Clipping at Ends if PipeLen is too Small
        yPos = min(yPos,config.window_size[1] - config.pipe_len - self.hGap - config.groundLevel)
        yPos = max(yPos,config.pipe_len + self.hGap)

        self.pipesInfo.append((xPos,yPos))

    #Resets Player Position
    #Used at Start or When Game Ends
    def reset(self):
        self.player_pos = copy.deepcopy(config.origin) #Reseting Player's Position
        self.pipesInfo = [(self.xGap,config.window_size[1]//2)] #Initial Pipe

        #Generating Initial Pipes Sequentially
        #pipe position = xGap,2*XGap,......n*XGap
        for _ in range(2*self.xGap,config.window_size[0],self.xGap):
           self.spawnNextPipe()

    def detectCollision(self):
        #Rect -> Top Left x, Top Left y, Width, Height
        check_collision = lambda rect1, rect2 : (
            rect1[0] < rect2[0] + rect2[2] and
            rect1[0] + rect1[2] > rect2[0] and
            rect1[1] < rect2[1] + rect2[3] and
            rect1[1] + rect1[3] > rect2[1]
        )

        #Bird Rectangle
        bird = [self.player_pos[0],self.player_pos[1],config.bird_size,config.bird_size]

        #Pipe Rectangles
        xPos,yPos = self.pipesInfo[0]

        #lower pipe -> pipe_gap//2 units below ypos
        #pipe start from xpos and ends at xPos + pipe_width
        lx,ly = (xPos,yPos+self.hGap//2)
        lw,lh = (config.pipe_width,config.window_size[1]-config.groundLevel-ly)
        lowerPipe = [lx,ly,lw,lh]

        #upper pipe -> pipe_gap//2 units above ypos
        #pipe start from xpos and ends at xPos + pipe_width
        ux,uy = (xPos,0) 
        uw,uh = (config.pipe_width,yPos-self.hGap//2)
        upperPipe = [ux,uy,uw,uh]

        if check_collision(bird,lowerPipe) or check_collision(bird,upperPipe):
            return True

        #Floor Check : Simple Y-Value check if Enough
        if self.player_pos[1] >= config.window_size[1]-config.groundLevel :
            return True 

        return False

    def update(self,action):
        self.player_pos[0] += self.player_speed #X-Axis Pos Update
        
        #Y-Axis Pos Update
        if action == "JUMP":
            self.player_pos[1] -= self.player_jump 
        if action == "FALL" :
            self.player_pos[1] += config.gravity

        #Adding new Pillar when in Reach
        #Player Reach = player_pos  + window_size
        #Right End of Pipe = last pipe pos + xGap - pipe width//2
        #Right End of Pipe <= Player Reach 
        #But considering origin
        #Right End of Pipe <= Player Reach - origin
        if (self.pipesInfo[-1][0] + self.xGap - config.pipe_width//2) <= (self.player_pos[0] + config.window_size[0]) - config.origin[0] :
            self.spawnNextPipe()
        elif len(self.pipesInfo) <= 2 :
            self.spawnNextPipe()

        #Removing Crossed Pillar
        #player pos - Left End > 0 Ideally
        #But we our origin is 10, it should be
        #player pos - Left End > origin
        if self.player_pos[0] - (self.pipesInfo[0][0] + config.pipe_width//2) >= config.origin[0]:
            self.pipesInfo.pop(0)

        #Collision Check
        #We reset the birds Position & Notify the Simulator for the same
        if self.detectCollision():
            self.reset()
            print(f'Client{self.__address} : Level Restart Due to Collision')

        #Updating GUI
        self.gui.update(self.player_pos,self.pipesInfo)

        return "state"

    #Graciously Closing Simulator
    def __del__(self):
        del self.gui
        print(f'Client{self.__address} : GUI Closed')
        print(f'Client{self.__address} : Simualtion Ended')
