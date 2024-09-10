'''
- Updates the Environment Given The Information
- Updates the Environment GUI aswell
- Relays back the new State to Manager
- Environment Info :
    - How far should Pillars be 
    - What the height difference of Pillars Should Be
    - How Big the Gap Should be 
'''
from gui import GUI
import random

class Simulator :
    def __init__(self,info,address):
        self.__address = address
        self.xGap = int(info[0]) #Spacing Across x Axis
        self.yGap = int(info[1]) #Max Spacing Across y Axis
        self.hGap = int(info[2]) #Hole Size between the Pipes

        print(f'Client{self.__address} : Simulation Begins')
        
        #Window & Player Configuration
        self.window_size = (1000,600) #Simulation Window Size
        self.origin  = [10,self.window_size[1]//2] #xAxis Origin
        self.groundLevel = 40  #Defining Ground Level (All Pipes are elevated)
        self.pipe_width = 30 #Width of Pipes
        self.pipe_len = 20 # Min Pipe Len
        self.player_speed = 5 #Player Movement Speed
        self.gravity = 0.5 #Ingame Gravity

        #Generating Pipes In Simulation Range
        self.pipesInfo = [] #No Pillar State
        self.player_pos = [10,self.window_size[1]//2] # Default Position of Player [Used For Reset]
        self.reset()
            
        #GUI Setup
        self.gui = GUI(self.window_size,self.groundLevel,self.pipesInfo,self.hGap,self.pipe_width)
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
        yPos = min(yPos,self.window_size[1] - self.pipe_len - self.hGap - self.groundLevel)
        yPos = max(yPos,self.pipe_len + self.hGap)

        self.pipesInfo.append((xPos,yPos))

    #Resets Player Position
    #Used at Start or When Game Ends
    def reset(self):
        self.player_pos = [10,self.window_size[1]//2] #Reseting Player's Position
        self.pipesInfo = [(self.xGap,self.window_size[0]//2)] #Initial Pipe

        #Generating Initial Pipes Sequentially
        #pipe position = xGap,2*XGap,......n*XGap
        for _ in range(2*self.xGap,self.window_size[0],self.xGap):
           self.spawnNextPipe()

    def update(self,action):
        self.player_pos[0] += self.player_speed #X-Axis Pos Update
        self.player_pos[1] += self.gravity #Y-Axis Pos Update

        #Similarly Adding new Pillar when in Reach
        #Player Reach = player_pos  + window_size
        #Right End of Pipe = last pipe pos + xGap - pipe width//2
        #Right End of Pipe <= Player Reach 
        #But considering origin
        #Right End of Pipe <= Player Reach - origin
        if (self.pipesInfo[-1][0] + self.xGap - self.pipe_width//2) <= (self.player_pos[0] + self.window_size[0]) - self.origin[0] :
            self.spawnNextPipe()
        elif len(self.pipesInfo) <= 2 :
            self.spawnNextPipe()

        #Removing Crossed Pillar
        #player pos - Left End > 0 Ideally
        #But we our origin is 10, it should be
        #player pos - Left End > origin
        if self.player_pos[0] - (self.pipesInfo[0][0] + self.pipe_width//2) >= self.origin[0]:
            self.pipesInfo.pop(0)

        self.gui.update(self.player_pos,self.pipesInfo)

        print(len(self.pipesInfo))

        return "state"

    #Graciously Closing Simulator
    def __del__(self):
        del self.gui
        print(f'Client{self.__address} : GUI Closed')
        print(f'Client{self.__address} : Simualtion Ended')
