import collections
import matplotlib.pyplot as plt
import matplotlib.colors
from functools import reduce
from operator import add
from . import District

class District:
    def __init__(self, length, width, colorList):
        # define the size of the District. 
        self.length = length 
        self.width = width 
        self.tiles = [[None for j in range(self.width)] for i in range(self.length)]
        self.population = 0
        self.colorList = colorList
        self.summary = dict()
        for i in range(len(self.colorList)-1):
            self.summary[i+1] = 0

        # parameter for uninitialized funcionality. 
        self.precincts = set()
        
    def addMember(self, x, y, agent, check = True):
        if not check or self.newMemberIsPhysicallyContinuous(self, x, y):
            self.tiles[x][y] = agent
            self.population +=1 
            firstChoice = agent.getFirstChoice()
            if firstChoice not in self.summary:
                self.summary[firstChoice] = 1
            else: 
                self.summary[firstChoice] += 1
            return True
        else:
            return False
        
    def newMemberIsPhysicallyContinuous(self, x, y):
        if not (x >= 0 and x < self.length) or not (y >= 0 and y < self.width): 
            return False
        if (x + 1 < self.length and self.tiles[x + 1][y] != None):
            return True
        if (x - 1 >= 0 and self.tiles[x-1][y] != None):
            return True
        if (y + 1 < self.width and self.tiles[x][y+1] != None):
            return True
        if (y-1 >= 0 and self.tiles[x][y-1] != None):
            return True
        return False
    
    # check if district is self continuous. 
    def isPhysicallyContinuous(self, x = None, y = None):
        # optimization. Early stopping if possible. 
        if x != None and y != None: 
            if (x >= 0 and x < self.length) or (y >= 0 and y < self.width): 
                circularList = []                
                # top left corner
                if (x - 1 >= 0 and y - 1 >= 0):
                    if self.tiles[x-1][y-1] != None:
                        circularList.append(1)
                    else:
                        circularList.append(0)
                # top 
                if (x-1 >= 0):
                    if self.tiles[x-1][y] != None:
                        circularList.append(1)
                    else:
                        circularList.append(0)
                # top right corder
                if (x - 1 >= 0 and y + 1 < self.width):
                    if self.tiles[x-1][y+1] != None:
                        circularList.append(1)
                    else:
                        circularList.append(0)
                # right
                if (y + 1 < self.width):
                    if self.tiles[x][y+1] != None:
                        circularList.append(1)
                    else:
                        circularList.append(0)
                # bottom right: 
                if (x + 1 < self.length and y+1 < self.width):
                    if self.tiles[x+1][y+1] != None:
                        circularList.append(1)
                    else:
                        circularList.append(0)
                # down
                if (x + 1 < self.length):
                    if self.tiles[x+1][y] != None:
                        circularList.append(1)
                    else:
                        circularList.append(0)
                # bottom left corner
                if (x + 1 < self.length and y - 1 >= 0):
                    if self.tiles[x+1][y-1] != None:
                        circularList.append(1)
                    else:
                        circularList.append(0)
                # left
                if (y-1>= 0):
                    if self.tiles[x][y-1] != None:
                        circularList.append(1)
                    else:
                        circularList.append(0)

                # if circularList is all 0, meaning this is the only member remain of this district. 
                if sum(circularList) == 0:
                    return False
                # if the circularList is not on an edge. 
                elif len(circularList) != 5:
                    startOf1, endOf1, startOf0, endOf0 = -1, -1, -1, -1
                    lastId = len(circularList) - 1
                    curId = 0
                    count = 0
                    while(True):
                        if circularList[curId] != circularList[lastId]:
                            if circularList[curId] == 0:
                                if startOf0 == -1:
                                    startOf0 = curId
                                elif startOf0 != -1 and curId != startOf0:
                                    break
                                if endOf1 == -1:
                                    endOf1 = lastId
                                elif endOf1 != -1 and lastId != endOf1:
                                    break
                            else:
                                if startOf1 == -1:
                                    startOf1 = curId
                                elif startOf1 != -1 and curId != startOf1:
                                    break
                                if endOf0 == -1:
                                    endOf0 = lastId
                                elif endOf0 != -1 and lastId != endOf0:
                                    break
                        # increment the index. 
                        lastId = curId
                        curId += 1
                        if curId >= len(circularList):
                            curId = 0
                        # if we have traverse the circular list twice and still don't seen any inconsistency, 
                        # then the removel of the member must have not affect the physical continuity of the district. 
                        # Return true. 
                        if count > len(circularList) + 1:
                            return True
                        # increment count
                        count += 1
            
        # BFS approach 
        visited = set()
        islandsCount = 0
        for i in range(self.length):
            for j in range(self.width):
                if self.tiles[i][j] != None and (i, j) not in visited:
                    if islandsCount >= 1:
                        return False
                    self.BFS((i, j), visited)
                    islandsCount += 1
        return True

    def BFS(self, tuple, visited):
        q = collections.deque()
        visited.add(tuple)
        q.append(tuple)
        while(q):
            i, j = q.popleft()
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            for xr, yr in directions:
                xcord = xr + i
                ycord = yr + j
                if (xcord >= 0 and xcord < self.length 
                    and ycord >= 0 and ycord < self.width 
                    and self.tiles[xcord][ycord] != None
                    and (xcord, ycord) not in visited):
                    q.append((xcord, ycord))
                    visited.add((xcord, ycord))
                    
    def isSafe(self, x, y):
        if x >= 0 and x < self.length and y >= 0 and y < self.width:
            return True
        return False
                    
    def ejectMember(self, x, y):
        if (x < 0 or x > self.length or y < 0 or y > self.width):
            return None
        
        if self.tiles[x][y] == None:
            return None
        else: 
            tempAgent = self.tiles[x][y]
            self.tiles[x][y] = None
            if self.isPhysicallyContinuous(x=x, y=y):
                firstChoice = tempAgent.getFirstChoice()
                self.summary[firstChoice] -= 1
                return tempAgent
            else:
                self.tiles[x][y] = tempAgent
                return None
    
    def show(self):
        actualColorList = []
        # +1 because the summary will always contain only non-white color, but the white color is still important. 
        for i in range(len(self.summary) + 1):
            actualColorList.append(self.colorList[i])
        bufferList = [] 
        for i in range(self.width):
            bufferList.append(i % len(self.colorList))
        mapTiles = self.getTileInColorIds()
        plt.imshow([bufferList] + mapTiles, cmap=matplotlib.colors.ListedColormap(self.colorList))
        plt.show()
        
    def getIm(self):
        mapTiles = self.getTileInColorIds()
        return mapTiles, matplotlib.colors.ListedColormap(self.colorList)
    
    def getSummary(self, percentage = False):
        if not percentage:
            return self.summary
        else:
            tempDict = self.summary
            sumCount = sum(tempDict.values())
            for i in tempDict:
                tempDict[i] /= sumCount
            return tempDict
    
    def isAdjacentTo(self, district2):
        for i in range(self.length):
            for j in range(self.width):
                if self.tiles[i][j] != None and district2.newMemberIsPhysicallyContinuous(i, j):
                    return True
        return False

    def balanceTwoDistrictsIfAdjacent(self, district2, method = "compact"):
        # method 1: adjacent cell merge first. 
        # each time, pick out all the tiles that are adjacent to the other district.
        if method == 'compact':
            itr = 0
            while(self.getPopulation() > district2.getPopulation()):
                itr += 1

                adjacentTiles = set()

                for i in range(self.length):
                    for j in range(self.width):
                        # pick out all the cells here that is adjacent to the other district. 
                        if self.tiles[i][j] != None and district2.newMemberIsPhysicallyContinuous(i, j):
                            adjacentTiles.add((i, j))

                # if no tiles are adjacent, we break out of the loop. 
                if (len(adjacentTiles) == 0):
                    break

                succeededCount = 0
                while(self.getPopulation() > district2.getPopulation() and len(adjacentTiles) > 0):
                    # we add this tile if after removing it we are still physically continuous. 
                    x, y = adjacentTiles.pop()
                    tempAgent = self.tiles[x][y]
                    self.tiles[x][y] = None
                    if (self.isPhysicallyContinuous(x=x, y=y)):
                        self.population -= 1
                        self.summary[tempAgent.getFirstChoice()] -= 1
                        district2.addMember(x, y, tempAgent, check=False)
                        succeededCount += 1
                    else:
                        self.tiles[x][y] = tempAgent

                # if none of the adjacent tiles can be merged to the other district, break
                if succeededCount == 0:
                    break
        
    def getPopulation(self):
        return self.population
    
    def getAgents(self, flat=True):
        if flat:
            return reduce(add, self.tiles)
        else:
            return self.tiles
    
    def tileIsOnEdge(self, x, y):
        if not (x >= 0 and x < self.length) or not (y >= 0 and y < self.width): 
            return False
        threshold = 4
        count = 0
        # right
        if (x + 1 < self.length):
            if (self.tiles[x + 1][y] != None):
                count += 1
        else:
            threshold -= 1

        # left
        if (x - 1 >= 0):
            if (self.tiles[x-1][y] != None):
                count += 1
        else:
            threshold -= 1

        # down
        if (y + 1 < self.width):
            if (self.tiles[x][y+1] != None):
                count += 1
        else:
            threshold -= 1

        # up
        if (y-1 >= 0):
            if (self.tiles[x][y-1] != None):
                count += 1
        else:
            threshold -= 1
        if count < threshold:
            return True
        return False
    
    # method : FPTP
    def getWinnerColorId(self, method="FPTP"):
        if method == "FPTP":
            max_key = max(self.summary, key=self.summary.get)
            return max_key
        # elif method == "RankChoiceVoting": 
    
    def getTileInColorIds(self):
        return [[self.tiles[i][j].getFirstChoice() \
                        if self.tiles[i][j] != None \
                        else 0 \
                    for j in range(self.width)] \
                    for i in range(self.length)]

    def getPartyResult(self, color):
        if color not in self.colorList:
            raise Exception("Color not in colorlist.")
        colorId = self.colorList.index(color)
        return self.summary[colorId]/sum(self.summary.values())

    def __str__(self):
        return str(self.getTileInColorIds())

def create_District(length, width, colorList):
    return District(length=length, width=width, colorList=colorList)