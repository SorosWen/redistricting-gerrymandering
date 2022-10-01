# Create instance of grid.
class Agent:
    def __init__(self, colorId, color, x, y):
        if colorId == None: 
            raise Exception("Agent is initialized with colorId = None. ")
        if color == None: 
            raise Exception("Agent is initialized with color = None. ")
        if x == None or y == None: 
            raise Exception("Agent is initialized without complete coordinate. ")
        self.color = color
        self.colorId = colorId
        self.x = x
        self.y = y
        
    def __str__(self):
        return "Agent: Color = {} | colorId = {} | x, y = ({}, {})".format(self.color, self.colorId, self.x, self.y)
    
    def getX(self):
        return self.x
    def getY(self): 
        return self.y
    def getCoord(self):
        return (self.x, self.y)
    def getColorId(self):
        return self.colorId
    def getColor(self):
        return self.color
    
    def setX(self, newX):
        self.x = newX
    def setY(self, newY):
        self.y = newY
    def setCoord(self, newX, newY):
        self.x = newX
        self.y = newY

def create_Agent(colorId, color, x, y):
    return Agent(colorId, color, x, y)
