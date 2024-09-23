# Create instance of grid.
class Agent:
    # colorId: the id of the color that this agent belongs to. 
    # color: the actual color that this agent belongs to. 
    # x, y: the x & y coordinate of the agent. 
    # choices: a list of colorIds: the first, second, third, ..., choices of the agent. 
    def __init__(self, x, y, choices = []):
        if choices == []: 
            raise Exception("Agent is initialized with no political preference. ")
        if x == None or y == None: 
            raise Exception("Agent is initialized without complete coordinate. ")
        self.choices = choices.copy()
        self.x = x
        self.y = y

    def __str__(self):
        return "Agent: Choices = {} | x, y = ({}, {})".format(self.choices[0], self.x, self.y)
    
    def getX(self):
        return self.x
    def getY(self): 
        return self.y
    def getCoord(self):
        return (self.x, self.y)
    def getColorId(self):
        return self.choices[0]
    def getFirstChoice(self):
        return self.choices[0]
    def getChoiceAtPosition(self, choiceId: int):
        if choiceId < 0 or choiceId >= len(self.choices):
            raise Exception("The agent doesn't choice #", choiceId)
        return self.choices[choiceId]
    def getChoices(self):
        return self.choices
    
    def setX(self, newX):
        self.x = newX
    def setY(self, newY):
        self.y = newY
    def setCoord(self, newX, newY):
        self.x = newX
        self.y = newY
    def setChoiceAtPosition(self, choiceId:int, newValue):
        if choiceId < 0 or choiceId >= len(self.choices):
            raise Exception("The agent doesn't have choice #", choiceId)
        self.choices[choiceId] = None
        if newValue in self.choices:
            raise Exception("The agent already has this choice at other preference level.")
        self.choices[choiceId] = newValue
    def setChoices(self, choices):
        self.choices = choices.copy()

def create_Agent(x, y, choices):
    return Agent(x, y, choices)
