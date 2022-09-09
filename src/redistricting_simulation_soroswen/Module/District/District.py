import matplotlib.pyplot as plt
import matplotlib.colors
import random
import numpy as np
import math
import sys
from Agent import Agent
from Map import Map

class District:
    def __init__(self, length, width, numOfColor, colorList):
        self.length = length # x
        self.width = width # y
        self.tiles = [[0 for j in range(self.width)] for i in range(self.length)]
        self.count = 0
        self.summary = dict()
        self.numOfColor = numOfColor
        self.colorList = colorList
        
    def addMember(self, x, y, colorId, check = True):
        if not check or self.newMemberIsPhysicallyContinuous(self, x, y):
            self.tiles[x][y] = colorId
            self.count +=1 
            if colorId not in self.summary:
                self.summary[colorId] = 1
            else: 
                self.summary[colorId] += 1
            return True
        else:
            return False
        
    def newMemberIsPhysicallyContinous(self, x, y):
        if not (x >= 0 and x < self.length) or not (y >= 0 and y < self.width): 
            return False
        if (x + 1 < self.length and self.tiles[x + 1][y] >= 1):
            return True
        if (x - 1 >= 0 and self.tiles[x-1][y] >= 1):
            return True
        if (y + 1 < self.width and self.tiles[x][y+1] >= 1):
            return True
        if (y-1 >= 0 and self.tiles[x][y-1] >= 1):
            return True
        return False
        
    def isPhysicallyContinuous(self):
        visited = [[False for j in range(self.width)]for i in range(self.length)]
        AlreadyReachedOneIsland = False
        for x in range(self.length):
            for y in range(self.width):
                # once we reached one island, we trigger DFS. All cells inside the island should be marked as visited. 
                # After that, if we reach another cell > 0 and not visited it yet, it means we reached another island, we return False. 
                if self.tiles[x][y] > 0 and not visited[x][y]:
                    if AlreadyReachedOneIsland:
                        return False
                    else:
                        AlreadyReachedOneIsland = True
                        self.DFS(x, y, visited)
        return True
    
    def DFS(self, x, y, visited):
        rowNbr = [-1, 0, 0, 1]
        colNbr = [0, -1, 1, 0]
        
        visited[x][y] = True
        
        for k in range(4):
            if self.isSafe(x + rowNbr[k], y + colNbr[k]) \
                and not visited[x + rowNbr[k]][y + colNbr[k]] \
                and self.tiles[x + rowNbr[k]][y + colNbr[k]] > 0:
                self.DFS(x + rowNbr[k], y + colNbr[k], visited)
    
    def isSafe(self, x, y):
        if x >= 0 and x < self.length and y >= 0 and y < self.width:
            return True
        return False
                    

    def ejectMember(self, x, y):
        if (x < 0 or x > self.length or y < 0 or y > self.width):
            return None
        
        if self.tiles[x][y] == 0:
            return None
        else: 
            temp = self.tiles[x][y]
            self.tiles[x][y] = 0
            if self.isPhysicallyContinuous():
                return temp
            else:
                self.tiles[x][y] = temp
                return None
    
    def show(self):
        actualColorList = []
        # +1 because the summary will always contain only non-white color, but the white color is still important. 
        for i in range(len(self.summary) + 1):
            actualColorList.append(self.colorList[i])
        bufferList = [] 
        for i in range(self.width):
            bufferList.append(i % len(self.colorList))
        plt.imshow([bufferList] + self.tiles, cmap=matplotlib.colors.ListedColormap(self.colorList))
        plt.show()
        
    def getIm(self):
        actualColorList = []
        for i in range(len(self.summary) + 1):
            actualColorList.append(self.colorList[i])
        return self.tiles, matplotlib.colors.ListedColormap(actualColorList)
    
    def getSummary(self, percentage = False):
        if not percentage:
            return self.summary
        else:
            tempDict = self.summary
            sumCount = sum(tempDict.values())
            for i in tempDict:
                tempDict[i] /= sumCount
            return tempDict
    
    def balanceTwoDistrictsIfAdjacent(self, district2, method = "compact"):
        # method 1: sequantial merge. 
        if method == 'extreme':
            for i in range(self.length):
                for j in range(self.width):
                    # if population of two districts are even
                    if self.getCount() <=  district2.getCount():
                        return
                    if random.uniform(0, 1) < 0.2 and self.tiles[i][j] != 0 and district2.newMemberIsPhysicallyContinous(i, j):
                        tempColorId = self.tiles[i][j]
                        self.tiles[i][j] = 0
                        if (self.isPhysicallyContinuous()):
                            self.count -= 1 
                            self.summary[tempColorId] -= 1
                            district2.addMember(i, j, tempColorId, False)
                        else:
                            self.tiles[i][j] = tempColorId
    
        # method 2: adjacent cell merge first. 
        # each time, pick out all the tiles that are adjacent to the other district.
        if method == 'compact':
            itr = 0
            while(self.getCount() > district2.getCount()):
                itr += 1

                adjacentTiles = set()

                for i in range(self.length):
                    for j in range(self.width):
                        # pick out all the cells here that is adjacent that is the other district. 
                        if self.tiles[i][j] != 0 and district2.newMemberIsPhysicallyContinous(i, j):
                            adjacentTiles.add((i, j))

                # if no tiles are adjacent, we break out of the loop. 
                if (len(adjacentTiles) == 0):
                    break

                succeededCount = 0
                while(self.getCount() > district2.getCount() and len(adjacentTiles) > 0):
                    # we add this tile if after removing it we are still physically continuous. 
                    x, y = adjacentTiles.pop()        
                    tempColorId = self.tiles[x][y]
                    self.tiles[x][y] = 0
                    if (self.isPhysicallyContinuous()):
                        self.count -= 1
                        self.summary[tempColorId] -= 1
                        district2.addMember(x, y, tempColorId, check=False)
                        succeededCount += 1
                    else:
                        self.tiles[x][y] = tempColorId
                # if none of the adjacent tiles can be given out, break
                if succeededCount == 0:
                    break

    def jointDisplay(self, district):
        jointTiles = [[0 for j in range(self.width)] for i in range(self.length)]
        for i in range(self.length):
            for j in range(self.width):
                if self.tiles[i][j] != 0:
                    jointTiles[i][j] = 1
                if district.tiles[i][j] != 0:
                    jointTiles[i][j] = 2
                actualColorList = []
        plt.imshow(jointTiles, cmap=matplotlib.colors.ListedColormap(self.colorList))
        plt.show()
        
    def getCount(self):
        return self.count
    
    def tileIsOnEdge(self, x, y):
        if not (x >= 0 and x < self.length) or not (y >= 0 and y < self.width): 
            return False
        # right
        count = 0
        if (x + 1 < self.length and self.tiles[x + 1][y] >= 1):
            count += 1
        # left
        if (x - 1 >= 0 and self.tiles[x-1][y] >= 1):
            count += 1
        # down
        if (y + 1 < self.width and self.tiles[x][y+1] >= 1):
            count += 1
        # up
        if (y-1 >= 0 and self.tiles[x][y-1] >= 1):
            count += 1
        if count == 4:
            return False
        return True
    
    def getMajorityColorId(self):
        max_value = max(self.summary.values())
        max_key = max(self.summary, key=self.summary.get)
        return max_key
    
    def __str__(self):
        return str([[self.tiles[i][j] for j in range(self.width)] for i in range(self.length)])