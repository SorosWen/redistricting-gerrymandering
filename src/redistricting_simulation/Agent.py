# Create instance of grid.
class Agent:
    def __init__(self, colorId, color, x, y):
        self.color = color
        self.colorId = colorId
        self.x = x
        self.y = y
        
    def __str__(self):
        return str(self.colorId)
    
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