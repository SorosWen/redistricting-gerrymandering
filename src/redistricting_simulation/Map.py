import matplotlib.pyplot as plt
import matplotlib.colors
import random
import numpy as np
import math
import sys
from Agent import Agent
from District import District 

class Map:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.population = length * width
        self.grid = []
        self.dict = {}
        self.districts = None
        self.colorMap = None
        self.colors = None
        self.method = None
        
    def initializeMap(self, method = 'uniform', num = 7, grid = None):
        # initialized Agent should never has colorId = 0, since 0 is for white space filler. 
        self.method = method
        
        if num > 7 or num < 1: 
            raise ValueError("Argument num has to be an integer between 1 to 7. ")
            
        if method == "naive":
            self.colors = ['tomato']
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            self.grid = [[Agent(1, 'tomato', i, j) for j in range(self.width)] for i in range(self.length)]
            
        if method == "uniform":
            # initialize color assignment 
            colorResort = ['red', 'blue', 'yellow', 'lightgreen', 'pink', 'brown', 'gold']
            tempColors = []
            for i in range(0, num):
                tempColors.append(colorResort[i])
            self.colors = tempColors
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            # initialize summary
            for i in range(num):
                self.dict[self.colors[i]] = 0
            
            self.grid = []
            for i in range(self.length):
                templ = []
                for j in range(self.width):
                    value = random.uniform(0, 1)
                    cap = 1/num
                    count = 0
                    while (cap <= 1):
                        if value <= cap:
                            templ.append(Agent(count + 1, self.colors[count], i, j))
                            self.dict[self.colors[count]] += 1
                            break
                        else:
                            cap += 1/num
                            count += 1
                self.grid.append(templ)
                
        # Nebraska, enum is set to 2, with one huge concentration of a particular enum. 
        if method == 'Nebraska':
            self.colors = ['tomato', 'royalblue']
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            cityCenter_x = random.randint(0, self.length)
            cityCenter_y = random.randint(0, self.width)
            self.grid = []
            self.dict['tomato'] = 0
            self.dict['royalblue'] = 0
            for i in range(self.length):
                templ = []
                for j in range(self.width):
                    # the distance between this agent and the city center. 
                    distance = math.sqrt((abs(i - cityCenter_x) ** 2) + (abs(j - cityCenter_y) ** 2))
                    prob = random.uniform(0, 1)
                    lratio = (self.length - distance) / self.length
                    wratio = (self.width - distance) / self.width
                    amplifier = 1.2
                    threshold = lratio * wratio * amplifier

                    if prob < threshold: 
                        templ.append(Agent(colorId = 2, color = self.colors[1], x=i, y=j))
                        self.dict['royalblue'] += 1
                    else:
                        templ.append(Agent(colorId = 1, color = self.colors[0], x=i, y=j))
                        self.dict['tomato'] += 1
                self.grid.append(templ)
            
        # Paris, five parties. Red being far left, purple being far right, palegreen being in the middle. 
        # closer to the city means more likely being toward the left. 
        # further away from the city means more likely to the right. 
        if method == "Warsaw":
            num = 5
            self.colors = ["tomato", "orange", "palegreen", "royalblue", "mediumorchid"]
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            for color in self.colors:
                self.dict[color] = 0
            
            cityCenter_x = random.randint(self.length * 0.3, self.length * 0.7)
            cityCenter_y = random.randint(self.width * 0.3, self.width * 0.7)

            for i in range(self.length):
                templ = []
                for j in range(self.width):
                    # the distance between this agent and the city center. 
                    distance = math.sqrt((abs(i - cityCenter_x) ** 2) + (abs(j - cityCenter_y) ** 2))
                    prob = random.uniform(0, 1)
                    lratio = (self.length - distance) / self.length
                    wratio = (self.width - distance) / self.width
                    amplifier = 1.2
                    threshold = lratio * wratio * amplifier

                    if prob < threshold/2: 
                        templ.append(Agent(colorId = 1, color = self.colors[0], x=i, y=j))
                        self.dict['tomato'] += 1
                    if threshold/2 < prob and prob < 5 * threshold/4:
                        templ.append(Agent(colorId = 2, color = self.colors[1], x=i, y=j))
                        self.dict['orange'] += 1
                    if 5*threshold/4 < prob and prob < 12 * threshold / 4 :
                        templ.append(Agent(colorId = 3, color = self.colors[2], x=i, y=j))
                        self.dict['palegreen'] += 1
                    if 12 * threshold / 4 < prob and prob < 50 * threshold / 4 :
                        templ.append(Agent(colorId = 4, color = self.colors[3], x=i, y=j))
                        self.dict['royalblue'] += 1
                    if 50 * threshold / 4 < prob:
                        templ.append(Agent(colorId = 5, color = self.colors[4], x=i, y=j))
                        self.dict['mediumorchid'] += 1
                        
                self.grid.append(templ)
                        
                    
    def __str__(self):
        return str([[str(self.grid[i][j]) for j in range(self.width)] for i in range(self.length)])

    def displayGrid(self):
        plt.imshow(self.getColorIds(), cmap = self.colorMap)
        plt.show()
    
    def getColorIds(self):
        return [[self.grid[i][j].getColorId() for j in range(self.width)] for i in range(self.length)]
    
    def getSummary(self, percentage = False):
        if not percentage:
            return self.dict
        tempDict = self.dict
        sumCount = sum(tempDict.values())
        for i in tempDict:
            tempDict[i] /= sumCount
        return tempDict

    def drawDistricts(self, numOfDistrict):
        colorList = self.colors
        self.districts = [District(self.length, self.width, len(self.colors), ['white']+colorList) for i in range(numOfDistrict)]
        districtCenters = []
        for i in range(numOfDistrict):
            center_x = random.randint(0, self.length)
            center_y = random.randint(0, self.width)
            districtCenters.append((center_x, center_y))
            
        for i in range(self.length):
            for j in range(self.width):
                minIdx = -1
                minDistance = 999999
                for k in range(len(districtCenters)):
                    (x, y) = districtCenters[k]
                    dist = ((x - i)**2 + (y - j)**2)**0.5
                    if dist < minDistance:
                        minIdx = k
                        minDistance = dist
                self.districts[minIdx].addMember(i, j, self.grid[i][j].getColorId(), check = False)
        
        lastPopulationList = [] 
        while(not self.districtsHasBalancedPopulation()):
            # sort districtsId by their population
            ids = [i for i in range(len(self.districts))]
            populationList = []
            for district in self.districts:
                populationList.append(district.getCount())
            ids = [x for _,x in sorted(zip(populationList,ids))]
            
            if str(populationList) == str(lastPopulationList):
                break
            else:
                lastPopulationList = populationList
                    
            for minPointer in range(0, len(self.districts)):
                for maxPointer in range(0, len(self.districts)):
                    minId = ids[minPointer]
                    maxId = ids[maxPointer]
                    if self.districts[minId].getCount() > self.districts[maxId].getCount():
                        temp = minId
                        minId = maxId
                        maxId = temp
                        
                    self.balanceTwoDistrictsIfAdjacent(minId, maxId)    
        
    def districtsHasBalancedPopulation(self):
        sum = 0
        for district in self.districts:
            sum += district.getCount()
        average = sum / len(self.districts)
        diff = 0
        for district in self.districts:
            diff += abs(district.getCount() - average)
        if diff >= 0.05 * self.population:
            return False
        return True
    
    def balanceTwoDistrictsIfAdjacent(self, minId, maxId):
        self.districts[maxId].balanceTwoDistrictsIfAdjacent(self.districts[minId])
        
    def showDistrict(self, index):
        self.districts[index].show()
        
    def showAllDistricts(self):
        fig, axs = plt.subplots(1, len(self.districts), figsize=(self.length, self.width))
        for i in range(len(self.districts)):
            tiles, colorMapOfDistrict = self.districts[i].getIm()
            axs[i].imshow(tiles, cmap = colorMapOfDistrict)
        plt.show()
        
    def getDistrictSummary(self, index):
        return self.districts[index].getSummary(percentage = True)
    
    def getDistrictCount(self, index):
        return self.districts[index].getCount()
    
    def showDistrictsResult(self, method = "flat", sort=True):
        if method == 'district':
            tempGrid = [[0 for j in range(self.width)] for i in range(self.length) ]
            for district in self.districts:
                majorityId = district.getMajorityColorId()
                districtTiles = district.tiles
                for i in range(district.length):
                    for j in range(district.width):
                        if districtTiles[i][j] > 0:
                            if district.tileIsOnEdge(i, j):
                                tempGrid[i][j] = 0
                            else:
                                tempGrid[i][j] = majorityId
            bufferList = []
            for i in range(self.width):
                bufferList.append(i % len(['white']+self.colors))
            colorMap = matplotlib.colors.ListedColormap(['white'] + self.colors)
            plt.imshow([bufferList] + tempGrid, cmap = colorMap)
            plt.show()
            
        if method == 'flat':
            if sort:
                fig, ax = plt.subplots()
                tempDict = {}
                for i in range(len(self.districts)):
                    majorityColorId = self.getDistrictMajorityColorId(i) - 1
                    majorityColor = self.colors[majorityColorId]
                    if majorityColor not in tempDict.keys():
                        tempDict[majorityColor] = 1
                    else:
                        tempDict[majorityColor] += 1
                position = 0
                for color in tempDict.keys():
                    for i in range(tempDict[color]):
                        ax.add_patch(plt.Circle((position * 10, 0), 3, color=color))
                        position += 1
                ax.set_aspect('equal', adjustable='datalim')
                ax.plot()
                plt.show()
            else: 
                fig, ax = plt.subplots()
                for i in range(len(self.districts)):
                    # the returned majorityId is int >= 1. 0 indicate 0 which is space filler. 
                    majorityColorId = self.getDistrictMajorityColorId(i)
                    # because the majorityId is >= 1, 
                    color = None
                    for j in range(len(self.colors)):
                        if majorityColorId-1 == j:
                            color = self.colors[j]
                            break
                    ax.add_patch(plt.Circle((i * 10, 0), 3, color=color))
                ax.set_aspect('equal', adjustable='datalim')
                ax.plot()
                plt.show()

    def getDistrictMajorityColorId(self, index):
        return self.districts[index].getMajorityColorId()
        
    def districtData(self, index):
        return str(self.districts[index])

    def tileIsOnEdge(self, x, y):
        if not self.isSafe(x, y):
            return False
        
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
        if count == 2:
            return False
        return True
    
    def isSafe(self, x, y):
        if (x >= 0 and x < self.length) or not (y >= 0 and y < self.width): 
            return True
        return False