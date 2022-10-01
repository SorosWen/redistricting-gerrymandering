import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.animation import FuncAnimation
import random
import sys
import math
from . import Agent, District, CalculationMethod as cm
import warnings

class Map:
    def __init__(self, length, width):
        # define the size of the Map.
        self.length = length
        self.width = width

        self.population = length * width
        self.grid = []
        self.summary = {}
        self.districts = []
        self.colorMap = None    # field exclusively for matplotlib so it is easy to show the grid. 
        self.colors = []        # a list containing all the color that agents in this grid would be able to contain. 
        self.method = ""      # the method that we wants for initializinng the map. 
        self.colorPartyNameMapping = []
        self.ani = None
        self.p = None
        self.fig = None 
        
    def initialize(self, method = 'uniform', num = 7, grid = None, colors = []):
        defaultColorList = ['red', 'blue', 'yellow', 'lightgreen', 'pink', 'brown', 'gold']
        self.method = method

        # initialized Agent should never has colorId = 0, since 0 is for white space filler. 
        
        if num > 7 or num < 1: 
            raise ValueError("Argument num has to be an integer between 1 to 7. ")

        if self.method == "customize":
            if colors != [] and len(colors) != num: 
                raise Exception("The specified of colors doesn't match the number of colors passed in. ")
            if colors == []:
                print("Colors are not specified. Will pull colors from the default color list.")
                self.colors = defaultColorList[0:num]
            else:
                self.colors = colors
            if grid == None:
                raise ValueError("Grid is missing under customize mode. ")
            else: 
                self.grid = [[Agent.create_Agent(colorId = grid[i][j], color = self.colors[grid[i][j]-1], x=i, y=j) for j in range(len(grid[0]))] for i in range(len(grid))]
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)

        if method == "naive":
            self.colors = ['tomato']
            self.colorPartyNameMapping = {'tomato':'United Right'}
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            self.grid = [[Agent.create_Agent(1, 'tomato', i, j) for j in range(self.width)] for i in range(self.length)]
            
        if method == "Uniform":
            # initialize color assignment 
            colorResort = ['red', 'gold', 'lightgreen', 'blue', 'yellow', 'pink', 'brown']
            self.colorPartyNameMapping = {'red':"The Left", "gold":"United Democratic", "lightgreen":"Centrist", "yellow":"People's Party", "blue":"Conservative", "pink":"New Hope", "brown":"National"}
            tempColors = []
            for i in range(0, num):
                tempColors.append(colorResort[i])
            self.colors = tempColors
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            # initialize summary
            for i in range(num):
                self.summary[self.colors[i]] = 0
            
            self.grid = []
            for i in range(self.length):
                templ = []
                for j in range(self.width):
                    value = random.uniform(0, 1)
                    cap = 1/num
                    count = 0
                    while (cap <= 1):
                        if value <= cap:
                            templ.append(Agent.create_Agent(count + 1, self.colors[count], i, j))
                            self.summary[self.colors[count]] += 1
                            break
                        else:
                            cap += 1/num
                            count += 1
                self.grid.append(templ)
                
        # Nebraska, enum is set to 2, with one huge concentration of a particular enum. 
        if method == 'Nebraska':
            self.colors = ['tomato', 'royalblue', 'gold']
            self.colorPartyNameMapping = {'tomato':'Republican', 'royalblue':"Democratic", 'gold':"Libertarian"}
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            cityCenter_x = random.randint(0, self.length)
            cityCenter_y = random.randint(0, self.width)
            self.grid = []
            for color in self.colors:
                self.summary[color] = 0
            for i in range(self.length):
                templ = []
                for j in range(self.width):
                    # generate libertarians
                    prob = random.uniform(0, 1)
                    if prob < 0.01:
                        templ.append(Agent.create_Agent(colorId = 3, color = self.colors[2], x=i, y=j))
                        self.summary['gold'] += 1
                    # generate Democrats and Republicans.
                    # the distance between this agent and the city center. 
                    distance = math.sqrt((abs(i - cityCenter_x) ** 2) + (abs(j - cityCenter_y) ** 2))
                    prob = random.uniform(0, 1)
                    lratio = (self.length - distance) / self.length
                    wratio = (self.width - distance) / self.width
                    amplifier = 1.2
                    threshold = lratio * wratio * amplifier
                    if prob < threshold: 
                        templ.append(Agent.create_Agent(colorId = 2, color = self.colors[1], x=i, y=j))
                        self.summary['royalblue'] += 1
                    else:
                        templ.append(Agent.create_Agent(colorId = 1, color = self.colors[0], x=i, y=j))
                        self.summary['tomato'] += 1
                self.grid.append(templ)
            
        # Paris, five parties. Red being far left, purple being far right, palegreen being in the middle. 
        # closer to the city means more likely being toward the left. 
        # further away from the city means more likely to the right. 
        if method == "Warsaw":
            num = 5
            self.colors = ["tomato", "orange", "lightgreen", "royalblue", "mediumorchid"]
            self.colorPartyNameMapping = {"tomato":'Progressive', "orange":"Liberal", "lightgreen":"Centrist", "royalblue":"Conservative", "mediumorchid":"New Hope"}
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            for color in self.colors:
                self.summary[color] = 0
            
            cityCenter_x = random.randint(int(self.length * 0.3), int(self.length * 0.7))
            cityCenter_y = random.randint(int(self.width * 0.3), int(self.width * 0.7))

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
                        templ.append(Agent.create_Agent(colorId = 1, color = self.colors[0], x=i, y=j))
                        
                        self.summary[self.colors[0]] += 1
                    if threshold/2 < prob and prob < 5 * threshold/4:
                        templ.append(Agent.create_Agent(colorId = 2, color = self.colors[1], x=i, y=j))
                        self.summary[self.colors[1]] += 1
                    if 5*threshold/4 < prob and prob < 12 * threshold / 4 :
                        templ.append(Agent.create_Agent(colorId = 3, color = self.colors[2], x=i, y=j))
                        self.summary[self.colors[2]] += 1
                    if 12 * threshold / 4 < prob and prob < 50 * threshold / 4 :
                        templ.append(Agent.create_Agent(colorId = 4, color = self.colors[3], x=i, y=j))
                        self.summary[self.colors[3]] += 1
                    if 50 * threshold / 4 < prob:
                        templ.append(Agent.create_Agent(colorId = 5, color = self.colors[4], x=i, y=j))
                        self.summary[self.colors[4]] += 1
                        
                self.grid.append(templ)
                                  
    def __str__(self):
        return str([[str(self.grid[i][j]) for j in range(self.width)] for i in range(self.length)])

    def showMap(self):
        plt.imshow(self.getColorIds(), cmap = self.colorMap)
        plt.axis('off')
        plt.show()
    
    def drawDistricts(self, numOfDistrict, 
                    gerrymandering = False, favoredColorId = 0, 
                    animate=False, 
                    save=False):
        colorList = self.colors
        self.districts = [District.create_District(self.length, self.width, len(self.colors), ['white']+colorList) for i in range(numOfDistrict)]
        
        # initializing the district centers. 
        districtCenters = []
        for i in range(numOfDistrict):
            foundUniqueCenter = False
            while not foundUniqueCenter: 
                center_x = random.randint(0, self.length)
                center_y = random.randint(0, self.width)
                if (center_x, center_y) not in districtCenters:
                    foundUniqueCenter = True
                    districtCenters.append((center_x, center_y))
        
        # assign each member to a district base on how close it is to each center. 
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
        
        # if we need to animate this process.
        if animate:
            print("Animating district drawing process. Please do not close the animation until the process has ended.")
            fig, ax = plt.subplots()
            self.p = ax
            self.fig = fig
            previousPair = [-1, -1]
            self.ani = FuncAnimation(fig, self.animateDrawDistricts, 
                                    fargs=(previousPair,), interval=1, 
                                    repeat=False, save_count=sys.maxsize)
            
            plt.show()
            return 

        # if we don't need to animate this process
        lastPopulationList = [] 
        while(not self.districtsHasBalancedPopulation()):
            # print("here are the population: ", lastPopulationList)
            populationList = [district.getPopulation() for district in self.districts]
            # stop if district populations are no longer changing. (which should never happen)
            if str(populationList) == str(lastPopulationList):
                warnings.warn("Districting ended due to population no longer changing. This should not happen. Please let us know if you encounter this error.")
                break
            lastPopulationList = populationList.copy()
            # sort districtsId by their population in acending order. 
            ids = [i for i in range(len(self.districts))]
            random.shuffle(ids)
            # constantly balance between two districts until all districts are balanced.  
            for minPointer in range(0, len(self.districts)):
                for maxPointer in range(len(self.districts) - 1, -1, -1):
                    if minPointer != maxPointer: 
                        minId = ids[minPointer]
                        maxId = ids[maxPointer]
                        # only balance these two districts if they have a big population difference. 
                        if abs(self.districts[minId].getPopulation() - self.districts[maxId].getPopulation()) > 1:
                            self.balanceTwoDistrictsIfAdjacent(minId, maxId)    

    def animateDrawDistricts(self, itr, previousPair):
        # print("itr=",itr)
        plt.axis('off')

        if not self.districtsHasBalancedPopulation():            
            # sort districtsId by their population in acending order. 
            ids = [i for i in range(len(self.districts))]
            random.shuffle(ids)
            # start balancing, but we only balance one pair of districts this time. 
            foundTwoAdjacentDistricts = False
            minPointer = 0
            maxPointer = len(self.districts) -1
            giveUp = False
            while(not foundTwoAdjacentDistricts and not giveUp):
                minId = ids[minPointer]
                maxId = ids[maxPointer]
                if minPointer != maxPointer \
                    and self.districts[minId].isAdjacentTo(self.districts[maxId]) \
                    and abs(self.districts[minId].getPopulation() - self.districts[maxId].getPopulation()) > 1 \
                    and not (minId in previousPair and maxId in previousPair):
                    previousPair[0] = minId
                    previousPair[1]= maxId
                    self.balanceTwoDistrictsIfAdjacent(minId, maxId)  
                    foundTwoAdjacentDistricts = True
                else:
                    if (maxPointer > 0):
                        maxPointer -= 1
                    else:
                        maxPointer = len(self.districts) -1
                        minPointer += 1
                        if minPointer >= len(self.districts):
                            giveUp = True
        else:
            self.ani.event_source.stop()
            return

        # plot it 
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
        
        plt.clf()
        plt.imshow([bufferList] + tempGrid, cmap = colorMap)
        plt.text(0, 0, str(itr))
        plt.axis('off')
        
    def showDistrict(self, index):
        self.districts[index].show()
        
    def showAllDistricts(self, method = "grid"):
        # a 2D grid where each cell is a district. 
        if method == 'grid':
            fig, axs = plt.subplots(int(len(self.districts)/6)+1, 6, figsize=(self.length, self.width))
            
            for i in range(len(self.districts)):
                tiles, colorMapOfDistrict = self.districts[i].getIm()
                axs[int(i/6)][i%6].imshow(tiles, cmap = colorMapOfDistrict)
                axs[int(i/6)][i%6].axis('off')
                axs[int(i/6)][i%6].grid(True)
            plt.show()

        # display one map showing all districts with the majority color. 
        if method == 'compact':
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
            plt.axis('off')
            plt.show()

    # displayMethod = summary, flat, arch
    # electoralSystem = majoritarian, parallel, MMP, proportionalRepresentation
    # districtCalculationMethod = FPTP
    # PRCalculationMethod = LargestRemainder, HighestAverage
    # overhangMethod = Allow, notAllowed
    def showParliamentComposition(self, displayMethod = "flat", electoralSystem = 'majoritarian', 
                                districtCalculationMethod = 'FPTP', PRCalculationMethod = 'LargestRemainder', 
                                overhangSeats = "Allow", seatsInParliament = 0, 
                                legend = False, showNumber = False, showTitle=False):
        # in the case of proportional representation. 
        if self.districts == []:
            raise Exception("District are not yet initialized. Cannot show parliament composition using districts.")

        # initialize compositionDict
        compositionDict = {}
        for color in self.colors:
            compositionDict[color] = 0

        # initializing the parliament composition in district form using the specified electoral system. 
        if electoralSystem == 'majoritarian':
            if districtCalculationMethod == "FPTP":
                compositionDict = self.getDistrictsElectionResult(method="FPTP")
            else:
                raise Exception("The calculation method'", districtCalculationMethod ,"' has not yet being implementated.")

        elif electoralSystem == "parallel":
            if seatsInParliament == 0:
                raise Exception("No seats are specified. You need to specify a seat number that is greater than the number of initialized districts.")
            if seatsInParliament <= len(self.districts):
                raise Exception("Not enough seats are specified. You need to specify a seats number that is greater than the number of initialized districts.")
            
            # first get the number of seats allocated for districts. 
            districtMandate = self.getDistrictsElectionResult()
            for color in districtMandate.keys():
                compositionDict[color] += districtMandate[color]
           
            # find the number of seats for PR.
            remainingSeats = seatsInParliament - len(self.districts) 
            
            # get party list result.
            partyListResult = self.getPartyListResult()

            # then get the number of remaining seats allocated for proportional representation. 
            if PRCalculationMethod == 'LargestRemainder':
                seatsAssignedForParallel = cm.LargestRemainder(partyListResult, remainingSeats)
                for party in seatsAssignedForParallel.keys():
                    compositionDict[party] += seatsAssignedForParallel[party]
            else: 
                raise Exception("The calculation method'", PRCalculationMethod ,"' has not yet being implementated.")

        elif electoralSystem == 'MMP':
            if seatsInParliament == 0:
                raise Exception("No seats are specified. You need to specify a seat number that is greater than the number of initialized districts.")
            if seatsInParliament <= len(self.districts):
                raise Exception("Not enough seats are specified. You need to specify a seats number that is greater than the number of initialized districts.")
            
            # District seats assignment 
            if districtCalculationMethod == "FPTP":
                districtMandate = self.getDistrictsElectionResult(method="FPTP")
                for color in districtMandate.keys():
                    compositionDict[color] += districtMandate[color]
            else:
                raise Exception("The calculation method'", districtCalculationMethod ,"' has not yet being implementated.")
            
            # Party Seats Allocation
            partyListResult = {}
            for color in self.colors:
                partyListResult[color] = 0
            for i in range(len(self.districts)):
                districtPartyListResult = self.districts[i].getSummary(percentage=False)
                for colorId in districtPartyListResult.keys():
                    color = self.colors[colorId - 1]
                    partyListResult[color] += districtPartyListResult[colorId]
            # then get the number of remaining seats allocated for proportional representation. 
            if PRCalculationMethod == 'LargestRemainder':
                sumOfVotes = sum(partyListResult.values())
                # division
                quota = 1.0 * sumOfVotes / seatsInParliament
                for color in partyListResult.keys():
                    partyListResult[color] = 1.0 * partyListResult[color] / quota
                # retrieve the integer part and decimal part. 
                intPart = {}
                decimalPart = {}
                for color in partyListResult.keys():
                    intPart[color] = int(partyListResult[color])
                    decimalPart[color] = partyListResult[color] - int(partyListResult[color])

                deservedSeats = {} # the amount of seats a party is rewarded according to party list result. 
                # assign the integer component to deservedSeats. 
                for color in intPart.keys():
                    if color not in deservedSeats.keys():
                        deservedSeats[color] = intPart[color]
                    else:
                        deservedSeats[color] += intPart[color]
                # assign the decimal components. 
                remainingSeats = seatsInParliament - sum(deservedSeats.values())
                for i in range(remainingSeats):
                    colorWithMaxDecimal = max(decimalPart, key=decimalPart.get)
                    if colorWithMaxDecimal not in deservedSeats.keys():
                        deservedSeats[colorWithMaxDecimal] = 1
                    else: 
                        deservedSeats[colorWithMaxDecimal] += 1
                    decimalPart.pop(colorWithMaxDecimal)

                # figuring out what to do with overhanging seats. 
                if overhangSeats == "Allow":
                    # assume if party receive more seats than it alread deserves, 
                    # we just simply not assigning any seat to it. 
                    for color in deservedSeats.keys():
                        if color not in compositionDict.keys():
                            compositionDict[color] = deservedSeats[color]
                        else:
                            if compositionDict[color] < deservedSeats[color]:
                                compositionDict[color] = deservedSeats[color]
                elif overhangSeats == 'notAllowed':
                    compositionDict = deservedSeats.copy()
            elif PRCalculationMethod == "HighestAverage":
                while sum(compositionDict.values()) < seatsInParliament:
                    divDict = {}
                    for color in partyListResult.keys():
                        seatsToColorFromDistrict = 0
                        if color in compositionDict.keys():
                            seatsToColorFromDistrict = compositionDict[color]
                        divDict[color] = 1.0* partyListResult[color]/(1.0 + seatsToColorFromDistrict)
                    colorWithMaxNum = max(divDict, key=divDict.get)
                    compositionDict[colorWithMaxNum] += 1
            else: 
                raise Exception("The calculation method'", PRCalculationMethod ,"' has not yet being implementated.")

        elif electoralSystem == 'proportionalRepresentation':
            if PRCalculationMethod == "LargestRemainder":
                partyListResult = self.getPartyListResult()
                compositionDict = cm.LargestRemainder(partyListResult, seatsInParliament)
            else:
                raise Exception("The method " + PRCalculationMethod + " has not been implemented yet for proportional representation.")

        else:
            raise Exception("The electoral system'", electoralSystem ,"' has not yet being implementated.")

        # retrieve the number of seats used here for displaying the number of seats. 
        sumOfSeats = sum(compositionDict.values())

        ######################## method below is for displaying ##############################
        if displayMethod == 'summary':
            return compositionDict

        # if the number of district is too small, we display them as flat regardless. 
        if sum(compositionDict.values())  <= 5 and displayMethod != 'flat':
            self.showParliamentComposition(displayMethod = 'flat')
            return

        fig, ax = plt.subplots()

        # below are display method.

        if displayMethod == 'flat':
            position = 0
            for color in compositionDict.keys():
                for i in range(compositionDict[color]):
                    ax.add_patch(plt.Circle((position * 10, 0), 3, color=color))
                    position += 1
            ax.set_aspect('equal', adjustable='datalim')
            ax.plot()
            plt.axis('off')
            plt.show()
        
        if displayMethod == 'arch':
            numOfDistricts = sum(compositionDict.values())

            # find the number of layers. 
            numOfLayers = 0
            counter = sum(compositionDict.values())
            itr = 0
            decrement = 16
            while counter > 0:
                counter -= decrement
                decrement += 3
                numOfLayers += 1

            # find the number of sum of total increment of all layers. 
            sumOfIncrement = (0 + 3 * (numOfLayers - 1))*(numOfLayers) / 2
            layerCounters = [0 for i in range(numOfLayers)]
            remainingMembers = sum(compositionDict.values()) - sumOfIncrement

            while remainingMembers > 0 :
                for i in range(numOfLayers):
                    if remainingMembers <= 0:
                        break
                    layerCounters[i] += 1
                    remainingMembers -= 1
            
            temp = 0
            for i in range(numOfLayers):
                layerCounters[i] += temp
                temp += 3

            # how far away the layer is from origin.
            armLength = 8
            # how big each circle should be. 
            radius = 0.5 

            # this section for legend only
            for color in self.colors:
                ax.add_patch(plt.Circle((0, 0), 0, color=color, label=self.colorPartyNameMapping[color]))

            # store a backup of compositionDict for plotting
            compositionDictBackUp = compositionDict.copy()

            # plot the arch
            patches = []
            for i in range(numOfLayers):
                counter = layerCounters[i]
                thisLayerDict = {}

                # decide what need to be displayed in each layer. 
                # if this is not the last layer. 
                if i != numOfLayers - 1: 
                    decimalPoints = {}
                    # check how many of members of each color should be displayed. Preserving decimal points in seperate dictionary.  
                    allocated = 0
                    for color in compositionDict.keys(): 
                        maxMemberOfColorInThisLayer = counter * compositionDict[color] / numOfDistricts
                        thisLayerDict[color] = int(maxMemberOfColorInThisLayer)
                        allocated += int(maxMemberOfColorInThisLayer)
                        if compositionDict[color] != 0 or maxMemberOfColorInThisLayer - int(maxMemberOfColorInThisLayer) < 0.0000000001:
                            decimalPoints[color] = maxMemberOfColorInThisLayer - int(maxMemberOfColorInThisLayer)
                    remainingSeats = counter - allocated

                    # formalize the decimal points so we can assign seats. 
                    totalDecimalPoints =  sum(decimalPoints.values())
                    for k in decimalPoints.keys():
                        decimalPoints[k] = decimalPoints[k] * remainingSeats/totalDecimalPoints

                    for i in range(remainingSeats):
                        colorWithMaxDecimal = max(decimalPoints, key=decimalPoints.get)
                        thisLayerDict[colorWithMaxDecimal] += 1
                        allocated += 1
                        decimalPoints[colorWithMaxDecimal] -= 1
                
                # if this is the last layer. 
                else:
                    thisLayerDict = compositionDict.copy()

                # display
                baseAngle = -90.0
                for color in self.colors:
                    if color not in thisLayerDict.keys(): 
                        continue
                    remainingMemberOfColor = thisLayerDict[color]
                    for j in range(remainingMemberOfColor):
                        if round(baseAngle, 1) == -90.0:
                            obj = plt.Circle((-armLength, 0), radius)
                            patches.append((obj, baseAngle))
                            ax.add_patch(obj)
                        elif round(baseAngle, 1) == 0.0:
                            obj = plt.Circle((0, armLength), radius)
                            patches.append((obj, baseAngle))
                            ax.add_patch(obj)
                        elif round(baseAngle, 1) == 90.0:
                            obj = plt.Circle((armLength, 0), radius)
                            patches.append((obj, baseAngle))
                            ax.add_patch(obj)
                        else: 
                            degree = 90.0 - abs(baseAngle)
                            x = math.cos(math.radians(degree)) * armLength
                            y = math.sin(math.radians(degree)) * armLength
                            if baseAngle < 0.0: 
                                obj = plt.Circle((-x, y), radius)
                                patches.append((obj, baseAngle))
                                ax.add_patch(obj)
                            else: 
                                obj = plt.Circle((x, y), radius)
                                patches.append((obj, baseAngle))
                                ax.add_patch(obj)
                        compositionDict[color] -= 1    # remove the number once displayed. 
                        baseAngle += 180.0 / (counter-1)

                armLength += 1.5
                numOfDistricts -= counter
            
            # since all circles are initialized and patched into the graph accordingly, let's add colors.
            # first sort the circles in ascending order
            patches.sort(key = lambda x: x[1])
            compositionDict = compositionDictBackUp
            count = 0
            for color in compositionDict.keys():
                for i in range(compositionDict[color]):
                    patch, degree = patches[count]
                    patch.set_color(color)
                    count += 1
            
            # display settings. 
            if showNumber:
                ax.text(0, 0, str(sumOfSeats), fontsize=24, ha = 'center')
            if legend:
                ax.legend(loc='upper right', bbox_to_anchor=(1.15,1))
            if showTitle:
                title = ""
                if electoralSystem == 'majoritarian':
                    title = electoralSystem + ": " + districtCalculationMethod
                elif electoralSystem == 'parallel':
                    title = electoralSystem + ": " + districtCalculationMethod + "+" + PRCalculationMethod
                elif electoralSystem == 'MMP':
                    title = electoralSystem + ": " + districtCalculationMethod + "+" + PRCalculationMethod
                elif electoralSystem == 'proportionalRepresentation':
                    title = electoralSystem + ": " + PRCalculationMethod
                ax.set_title(label=title)
            ax.set_aspect('equal', adjustable='datalim')
            ax.plot()
            plt.axis('off')
            plt.show()

    def showDemography(self, percentage=False):
        if percentage:
            tempDict = self.getDemography(percentage=True)
            plt.bar(self.colorPartyNameMapping.values(), tempDict.values(), color=self.summary.keys())
            plt.xlabel("Party Name")
            plt.ylabel("Vote Share")
            plt.show()
        else:
            plt.bar(self.colorPartyNameMapping.values(), self.summary.values(), color=self.summary.keys())
            plt.xlabel("Party Name")
            plt.ylabel("Vote")
            plt.show()

    def getColorIds(self):
        return [[self.grid[i][j].getColorId() for j in range(self.width)] for i in range(self.length)]
    
    def getDemography(self, percentage = False):
        if not percentage:
            return self.summary
        tempDict = self.summary
        sumCount = sum(tempDict.values())
        for i in tempDict:
            tempDict[i] /= sumCount
        return tempDict
        
    def getDistrictMajorityColorId(self, index):
        return self.districts[index].getMajorityColorId()
    
    def getDistrictDemography(self, index):
        return self.districts[index].getSummary(percentage = True)
    
    def getDistrictPopulation(self, index):
        return self.districts[index].getPopulation()
            
    def getDistrictsPopulation(self):
        return [district.getPopulation() for district in self.districts]
        
    def getDistrictsElectionResult(self, method = 'FPTP'):
        seatsAssiged = {}
        for color in self.colors:
            seatsAssiged[color] = 0
        if method == 'FPTP':
            for i in range(len(self.districts)):
                majorityColorId = self.getDistrictMajorityColorId(i) - 1
                majorityColor = self.colors[majorityColorId]
                seatsAssiged[majorityColor] += 1
            return seatsAssiged
        else:
            raise Exception("Method "+ method+" has not been implemented yet.")

    def getPartyListResult(self):
        partyListResult = {}
        for color in self.colors:
            partyListResult[color] = 0
        for i in range(len(self.districts)):
            districtPartyListResult = self.districts[i].getSummary(percentage=False)
            for colorId in districtPartyListResult.keys():
                color = self.colors[colorId - 1]
                if color not in partyListResult.keys():
                    partyListResult[color] = districtPartyListResult[colorId]
                else:
                    partyListResult[color] += districtPartyListResult[colorId]
        return partyListResult

    def districtsHasBalancedPopulation(self):
        sum = 0
        for district in self.districts:
            sum += district.getPopulation()
        average = sum / len(self.districts)
        for district in self.districts:
            if not (district.getPopulation() < average + 5 and average - 5 < district.getPopulation()):
                return False
        return True
    
    # helper function. 
    def balanceTwoDistrictsIfAdjacent(self, minId, maxId):
        if self.districts[minId].getPopulation() > self.districts[maxId].getPopulation():
            temp = minId
            minId = maxId
            maxId = temp
        self.districts[maxId].balanceTwoDistrictsIfAdjacent(self.districts[minId])
    
    # helper
    def districtData(self, index):
        return str(self.districts[index])

    # helper
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
    
    # helper
    def isSafe(self, x, y):
        if (x >= 0 and x < self.length) or not (y >= 0 and y < self.width): 
            return True
        return False
    
def create_Map(length, width):
    return Map(length, width)
