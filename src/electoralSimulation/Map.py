import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import random
import sys
import math
import numpy as np
from . import Agent, District
from . import CalculationMethod as cm
import warnings
from io import BytesIO
import base64

class Map:
    def __init__(self, length, width, method, num = 7, grid = None, colors = []):
        if length <= 0 or width <= 0: 
            raise Exception("Length and width must be a positive integer.")
        if length >= 200 or width >= 200:
            print("Beware if length or width exceeds 200, the computation required would be substatially large.")
        
        # define the size of the Map.
        self.length = length
        self.width = width

        self.grid = []
        self.summary = {}
        self.districts = []
        self.colors = []        # a list containing all the color that agents in this grid would be able to contain. 
        self.colorMap = None    # field exclusively for matplotlib so it is easy to show the grid. 
        self.colorPartyNameMapping = []
        
        # parameters below are for animating the districting process. 
        self.ani = None
        self.p = None
        self.fig = None 

        self.initialize(method=method, num=num, grid=grid, colors=colors)
        
    def initialize(self, method = 'Uniform', num = 7, 
                    grid = None, colors = []):
        defaultColorList = ['red', 'blue', 'yellow', 'lightgreen', 'pink', 'brown', 'gold']

        # initialized Agent should never has colorId = 0, since 0 is for white space filler. 
        
        if num > 7 or num < 1: 
            raise ValueError("Argument num has to be an integer between 1 to 7. Current version only support at most 7 different political parties.")

        if method == "customize":
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
                self.grid = [[Agent.create_Agent(choices=[grid[i][j]], x=i, y=j) for j in range(len(grid[0]))] for i in range(len(grid))]
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)

        if method == "Uniform":
            # initialize color assignment 
            colorResort = ['red', 'gold', 'lightgreen', 'blue', 'yellow', 'pink', 'brown']
            self.colorPartyNameMapping = {'red':"The Left", "gold":"United Democratic", 
                                            "lightgreen":"Centrist", "yellow":"People's Party", 
                                            "blue":"Conservative", "pink":"Far Right", "brown":"National"}
            tempColors = []
            for i in range(0, num):
                tempColors.append(colorResort[i])
            self.colors = tempColors
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            # initialize summary
            for color in self.colors:
                self.summary[color] = 0
            
            # initializing the grid. 
            self.grid = []
            for i in range(self.length):
                tempList = []
                for j in range(self.width):
                    value = random.uniform(0, 1)
                    cap = 1/num
                    count = 0
                    while (cap <= 1):
                        if value <= cap:
                            # append first choice. 
                            choices = [count + 1]
                            temp = random.random()
                            # append second and third choice for rank choice voting.
                            if temp < 0.5:
                                if count > 0:
                                    choices.append(count)
                                if count + 2 <= len(self.colors):
                                    choices.append(count + 2)
                            else:
                                if count + 2 <= len(self.colors):
                                    choices.append(count + 2)
                                if count > 0:
                                    choices.append(count)
                            # create agent using initialized choices.
                            tempList.append(Agent.create_Agent(choices=choices, x=i, y=j))
                            self.summary[self.colors[count]] += 1
                            break
                        else:
                            cap += 1/num
                            count += 1
                self.grid.append(tempList)
            return 
                
        # Indiana, only 3 parties. 
        if method == 'Indiana':
            self.colors = ['red', 'blue', 'gold']
            self.colorPartyNameMapping = {'red':'Republican', 'blue':"Democratic", 'gold':"Libertarian"}
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            # cityCenter_x = random.randint(0, self.length)
            # cityCenter_y = random.randint(0, self.width)
            cityCenter_x = self.length / 2
            cityCenter_y = self.width / 2
            self.grid = []
            for color in self.colors:
                self.summary[color] = 0
            for i in range(self.length):
                tempList = []
                for j in range(self.width):
                    # generate libertarians
                    prob = random.uniform(0, 1)
                    if prob < 0.02:
                        # initialize ranked choices. 
                        choices = [3]
                        temp = random.uniform(0, 1)
                        if temp < 0.45:
                            choices.append(1)
                        elif 0.45 <= temp and temp < 0.5:
                            choices.append(2)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary['gold'] += 1
                    # generate Democrats and Republicans.
                    # the distance between this agent and the city center. 
                    distance = math.sqrt((abs(i - cityCenter_x) ** 2) + (abs(j - cityCenter_y) ** 2))
                    lratio = (self.length - distance) / self.length
                    wratio = (self.width - distance) / self.width
                    amplifier = 1.0
                    threshold = lratio * wratio * amplifier

                    prob = random.uniform(0, 1)
                    if prob < threshold: 
                        choices = [2]
                        temp = random.uniform(0, 1)
                        if temp < 0.13:
                            choices.append(1)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary['blue'] += 1
                    else:
                        choices = [1]
                        temp = random.uniform(0, 1)
                        if temp < 0.2:
                            choices.append(2)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary['red'] += 1
                self.grid.append(tempList)
            
        # Warsaw, five parties. Red being far left, purple being far right, palegreen being in the middle. 
        # closer to the city means more likely being toward the left. 
        # further away from the city means more likely to the right. 
        if method == "Warsaw":
            self.colors = ["tomato", "orange", "lightgreen", "royalblue", "mediumorchid"]
            self.colorPartyNameMapping = {"tomato":'Progressive', "orange":"Liberal", "lightgreen":"Centrist", "royalblue":"Conservative", "mediumorchid":"New Hope"}
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            portions = [0.5, 1.2, 3.0, 12.5]
            
            for color in self.colors:
                self.summary[color] = 0
            
            cityCenter_x = random.randint(int(self.length * 0.3), int(self.length * 0.7))
            cityCenter_y = random.randint(int(self.width * 0.3), int(self.width * 0.7))

            for i in range(self.length):
                tempList = []
                for j in range(self.width):
                    # the distance between this agent and the city center. 
                    distance = math.sqrt((abs(i - cityCenter_x) ** 2) + (abs(j - cityCenter_y) ** 2))
                    lratio = (self.length - distance) / self.length
                    wratio = (self.width - distance) / self.width
                    amplifier = 1.0
                    threshold = lratio * wratio * amplifier

                    prob = random.uniform(0, 1)
                    choices = []
                    if prob < threshold*portions[0]:
                        choices.append(1)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(2)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[0]] += 1
                    elif threshold*portions[0] < prob and prob < threshold*portions[1]:
                        choices.append(2)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(1)
                            choices.append(3)
                        else:
                            choices.append(3)
                            choices.append(1)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[1]] += 1
                    elif threshold*portions[1] < prob and prob < threshold*portions[2] :
                        choices.append(3)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(2)
                            choices.append(4)
                        else:
                            choices.append(4)
                            choices.append(2)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[2]] += 1
                    elif threshold*portions[2] < prob and prob < threshold*portions[3] :
                        choices.append(4)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(3)
                            choices.append(5)
                        else:
                            choices.append(5)
                            choices.append(3)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[3]] += 1
                    elif threshold*portions[3] < prob:
                        choices.append(5)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(4)
                        tempList.append(Agent.create_Agent(choices = [5], x=i, y=j))
                        self.summary[self.colors[4]] += 1
                        
                self.grid.append(tempList)

        if method == "Hungary":
            self.colors = ["tomato", "forestgreen", "purple", 
                            "dodgerblue", "orange", "turquoise"]
            self.colorPartyNameMapping = {"tomato":'Socialist Party', "forestgreen":"Green Party", 
                                            "purple":"Momentum Movement", "dodgerblue":"Democratic Coalition", 
                                            "orange":"Fidesz", "turquoise":"Jobbik"}
            self.colorMap = matplotlib.colors.ListedColormap(self.colors)
            
            for color in self.colors:
                self.summary[color] = 0
            
            cityCenter_x = random.randint(int(self.length * 0.45), int(self.length * 0.65))
            cityCenter_y = random.randint(int(self.width * 0.45), int(self.width * 0.65))

            for i in range(self.length):
                tempList = []
                for j in range(self.width):
                    # the distance between this agent and the city center. 
                    distance = math.sqrt((abs(i - cityCenter_x) ** 2) + (abs(j - cityCenter_y) ** 2))
                    maxPointToCenterDistance = math.sqrt(max(cityCenter_x, self.length - cityCenter_x)**2 + max(cityCenter_y, self.width - cityCenter_y)**2)
                    ratio = (maxPointToCenterDistance - distance)/maxPointToCenterDistance

                    t = ratio
                    portions = []
                    try: 
                        if (t > 0):
                            portions.append((t**4.0-t**7)/(t-t**7).real)
                            portions.append((t**3.1-t**7)/(t-t**7).real)
                            portions.append((t**2.9-t**7)/(t-t**7).real)
                            portions.append((t**2.6-t**7)/(t-t**7).real)
                            portions.append((t**0.27-t**7)/(t**0.01-t**7).real)
                        else: 
                            portions = [0, 0, 0, 0, 0]
                    except:
                        portions = [0, 0, 0, 0, 0]

                    prob = random.uniform(0, 1)
                    choices = []
                    if prob < portions[0]:
                        choices.append(1)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(2)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[0]] += 1
                    elif portions[0] < prob and prob < portions[1]:
                        choices.append(2)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(1)
                            choices.append(3)
                        else:
                            choices.append(3)
                            choices.append(1)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[1]] += 1
                    elif portions[1] < prob and prob < portions[2] :
                        choices.append(3)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(2)
                            choices.append(4)
                        else:
                            choices.append(4)
                            choices.append(2)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[2]] += 1
                    elif portions[2] < prob and prob < portions[3] :
                        choices.append(4)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(3)
                            choices.append(5)
                        else:
                            choices.append(5)
                            choices.append(3)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[3]] += 1
                    elif portions[3] < prob and prob < portions[4]:
                        choices.append(5)
                        if random.uniform(0, 1) < 0.5:
                            choices.append(4)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[4]] += 1
                    elif portions[4] < prob: 
                        choices.append(6)
                        tempList.append(Agent.create_Agent(choices = choices, x=i, y=j))
                        self.summary[self.colors[5]] += 1

                self.grid.append(tempList)

    def showMap(self):
        plt.imshow(self.getColorIds(), cmap = self.colorMap)
        plt.axis('off')
        plt.show()
    
    def saveMap(self):
        plt.imshow(self.getColorIds(), cmap = self.colorMap)
        plt.axis('off')
        plt.savefig("map.png", bbox_inches='tight')

    def getMapForDjango(self):
        plt.switch_backend('AGG')
        plt.title('Map')
        plt.imshow(self.getColorIds(), cmap = self.colorMap)
        plt.tight_layout()

        # get graph
        buffer=BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()
        
        return graph
    
    def showDistrict(self, index):
        self.districts[index].show()

    def drawDistricts(self, numOfDistrict, animate=False):
        if numOfDistrict <= 1:
            raise Exception("The number of districts is invalid. Must have at least 2 districts.")
        if numOfDistrict > self.length*self.width/2:
            raise Exception("The number of districts are too large. The district number must be smaller than length * width / 2.")

        self.districts = [District.create_District(length=self.length, width=self.width, colorList=['white']+self.colors.copy()) for i in range(numOfDistrict)]
        
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
                self.districts[minIdx].addMember(x=i, y=j, agent=self.grid[i][j], check=False)
        
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
            majorityId = district.getWinnerColorId()
            for i in range(district.length):
                for j in range(district.width):
                    if district.tiles[i][j] != None:
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

    def showAllDistricts(self, method = 'compact'):
        if (len(self.districts) == 0):
            raise Exception("Districts have not been initialized.")
        # a 2D grid where each cell is a district. 
        if method == 'grid':
            fig, axs = plt.subplots(int(len(self.districts)/6)+1, 
                                    min(6, len(self.districts)), 
                                    figsize=(self.length, self.width))

            if (len(self.districts) <= 6):
                for i in range(len(self.districts)):
                    tiles, colorMapOfDistrict = self.districts[i].getIm()
                    axs[i].imshow(tiles, cmap = colorMapOfDistrict)
                    axs[i].set_title("District "+ str(i+1))
                    axs[i].axis('off')
                    axs[i].grid(True)
            else:
                for i in range((int(len(self.districts)/6)+1) * 6):
                    if i < len(self.districts):
                        tiles, colorMapOfDistrict = self.districts[i].getIm()
                        axs[int(i/6), i%6].imshow(tiles, cmap = colorMapOfDistrict)
                        axs[int(i/6), i%6].set_title("District "+ str(i+1))
                        axs[int(i/6), i%6].axis('off')
                        axs[int(i/6), i%6].grid(True)
                    else:
                        axs[int(i/6), i%6].axis('off')
            plt.tight_layout()
            plt.show()
            return

        # display one map showing all districts with the majority color. 
        elif method == 'winner':
            tempGrid = [[0 for j in range(self.width)] for i in range(self.length) ]
            for district in self.districts:
                majorityId = district.getWinnerColorId()
                for i in range(district.length):
                    for j in range(district.width):
                        if district.tiles[i][j] != None:
                            tempGrid[i][j] = majorityId
            bufferList = []
            for i in range(self.width):
                bufferList.append(i % len(['white']+self.colors))
            colorMap = matplotlib.colors.ListedColormap(['white'] + self.colors)
            plt.imshow([bufferList] + tempGrid, cmap = colorMap)
            plt.axis('off')
            plt.show()
        
        elif method == "compact":
            tempGrid = [[0 for j in range(self.width)] for i in range(self.length) ]
            id = 1
            for district in self.districts:
                for i in range(district.length):
                    for j in range(district.width):
                        if district.tiles[i][j] != None:
                            tempGrid[i][j] = id
                id += 1
            plt.imshow(tempGrid, cmap='hsv')
            plt.axis('off')
            plt.show()

    def showDistrictsElectionResult(self, color="", method='heatmap'):
        if len(self.districts) == 0:
            raise Exception("Districts have not been initialized.")
        
        if method=="heatmap":
            if color not in self.colors:
                raise Exception(color, "doesn't exist in this map.")

            colors = ['white', color]
            nodes = [0.0, 1.0]
            cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))
            data = np.zeros((self.length, self.width), dtype=np.double)
            for district in self.districts:
                percentage = district.getPartyResult(color)
                for i in range(district.length):
                    for j in range(district.width):
                        if district.tiles[i][j] != None:
                            data[self.length -1 -i][j] = percentage
            psm = plt.pcolormesh(data, cmap=cmap, rasterized=True, vmin=0.0, vmax=1.0)
            plt.axis('off')
            plt.colorbar(psm)
            plt.show()

        elif method=="bar":
            bars = {}
            for color in self.colors:
                bars[color] = []

            for district in self.districts:
                districtSummary = district.getSummary(percentage=True)
                for i in range(len(self.colors)):
                    colorId = i+1
                    if colorId not in districtSummary.keys():
                        districtSummary[colorId] = 0.0

                for colorId in districtSummary.keys():
                    bars[self.colors[colorId-1]].append(districtSummary[colorId])
            
            barWidth = 0.8/len(self.colors)
            br = np.arange(len(self.districts))

            for color in self.colors:
                plt.bar(br, bars[color], color=color, width = barWidth,
                        label=self.colorPartyNameMapping[color])
                br = [x + barWidth for x in br]
            plt.xticks([r + barWidth for r in range(len(self.districts))],
                        [str(i+1) for i in range(len(self.districts))])
            plt.xlabel("Districts")
            plt.legend()
            plt.show()

    """
    Below are supported value for each variable
    * displayMethod = summary, arch
    * electoralSystem = majoritarian, parallel, MMP, proportionalRepresentation
    * districtCalculationMethod = FPTP, RankChoiceVoting
    * PRCalculationMethod = LargestRemainder, HighestAverage
    * overhangMethod = Allow, notAllowed
    """
    def showParliamentComposition(self, electoralSystem = 'majoritarian', 
                                districtCalculationMethod = 'FPTP', PRCalculationMethod = 'LargestRemainder', 
                                allowOverhangSeats = True, seatsInParliament = 0, 
                                displayMethod = "arch", legend = True, showNumber = True, showTitle=False, 
                                divisor = "D'Hondt", quota = "None", threshold = 1):
        # in the case of proportional representation. 
        if self.districts == []:
            raise Exception("District are not yet initialized. Cannot show parliament composition using districts.")

        # initialize compositionDict
        compositionDict = {}
        for color in self.colors:
            compositionDict[color] = 0

        # initializing the parliament composition in district form using the specified electoral system. 
        if electoralSystem == 'majoritarian':
            compositionDict = self.getDistrictsElectionResult(method=districtCalculationMethod)

        elif electoralSystem == "parallel":
            if seatsInParliament <= 0:
                raise Exception("Specified seat number is invalid. You need to specify a seat number that is greater than the number of initialized districts.")
            if seatsInParliament <= len(self.districts):
                raise Exception("Not enough seats are specified. You need to specify a seats number that is greater than the number of initialized districts.")
            
            # first get the number of seats allocated for districts. 
            districtMandate = self.getDistrictsElectionResult(method=districtCalculationMethod)
            for color in districtMandate.keys():
                compositionDict[color] += districtMandate[color]
           
            # get party list result.
            partyListResult = self.getPartyListResult()

            # Get the number of remaining seats allocated for proportional representation. 
            seatsAssignedForPR = self.getPRSeatsAssignment(method = PRCalculationMethod, partyListResult = partyListResult, 
                                                                seatsAssigned = len(self.districts), seatsToBeAssigned = seatsInParliament - len(self.districts), assignedSeats = compositionDict)
            for party in seatsAssignedForPR.keys():
                compositionDict[party] += seatsAssignedForPR[party]

        elif electoralSystem == 'MMP':
            if seatsInParliament == 0:
                raise Exception("No seats are specified. You need to specify a seat number that is greater than the number of initialized districts.")
            if seatsInParliament <= len(self.districts):
                raise Exception("Not enough seats are specified. You need to specify a seats number that is greater than the number of initialized districts.")
            
            # District seats assignment 
            districtMandate = self.getDistrictsElectionResult(method=districtCalculationMethod)
            for color in districtMandate.keys():
                compositionDict[color] += districtMandate[color]
            
            # Get Party List Result
            partyListResult = self.getPartyListResult()

            # Get the number of remaining seats allocated for proportional representation. 
            proportionalSeatsAssignment = self.getPRSeatsAssignment(
                                    method = PRCalculationMethod, 
                                    partyListResult = partyListResult, 
                                    seatsAssigned = len(self.districts), 
                                    seatsToBeAssigned = seatsInParliament - len(self.districts), 
                                    assignedSeats = compositionDict, 
                                    divisor = divisor, 
                                    quota = quota, 
                                    threshold = threshold, 
                                    allowOverhang=allowOverhangSeats); 
            
            for color in proportionalSeatsAssignment.keys():
                compositionDict[color] += proportionalSeatsAssignment[color]

        elif electoralSystem == 'proportionalRepresentation':
            if seatsInParliament < len(self.districts) or seatsInParliament == 0:
                raise Exception("The number of seats specified is invalid.") 
            partyListResult = self.getPartyListResult()
            compositionDict = self.getPRSeatsAssignment(
                                    method = PRCalculationMethod, 
                                    partyListResult = partyListResult, 
                                    seatsAssigned = 0, 
                                    seatsToBeAssigned = seatsInParliament, 
                                    assignedSeats = {}, 
                                    divisor = divisor, 
                                    quota = quota, 
                                    threshold = threshold, 
                                    allowOverhang=allowOverhangSeats); 

        else:
            raise Exception("The electoral system'", electoralSystem ,"' has not yet being implementated.")

        # retrieve the number of seats used here for displaying the number of seats. 
        sumOfSeats = sum(compositionDict.values())

        ######################## method below is for displaying ##############################
        if displayMethod == 'summary':
            return compositionDict

        if displayMethod == 'arch':
            fig, ax = plt.subplots()
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
        if self.grid == []:
            raise Exception("Map has not been initialized yet.")
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
        return self.districts[index].getWinnerColorId()
    
    def getDistrictDemography(self, index, percentage = True):
        return self.districts[index].getSummary(percentage)
    
    def getDistrictPopulation(self, index):
        return self.districts[index].getPopulation()
            
    def getDistrictsPopulation(self):
        return [district.getPopulation() for district in self.districts]
        
    # method = FPTP, RankChoiceVoting
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
        elif method == "RankChoiceVoting":
            for i in range(len(self.districts)):
                agents = self.districts[i].getAgents()
                winnerId = cm.RankChoiceVoting(agents) - 1
                winnerParty = self.colors[winnerId]
                seatsAssiged[winnerParty] += 1
            return seatsAssiged
        else:
            raise Exception("Method "+ method + " has not been implemented yet.")
    
    def getPRSeatsAssignment(self, method = "LargestRemainder", 
                                    partyListResult = {}, 
                                    seatsAssigned = 0, 
                                    seatsToBeAssigned = 0, 
                                    assignedSeats = {}, 
                                    divisor = "D'Hondt", 
                                    quota = "None", 
                                    threshold = 1, 
                                    allowOverhang=False):
        if method == "LargestRemainder":
            return cm.LargestRemainder(partyListResult, seatsToBeAssigned)
        elif method == "HighestAverage":
            return cm.HighestAverage(partyListResultOrigin = partyListResult, 
                                    totalSeats = seatsAssigned + seatsToBeAssigned, 
                                    assignedSeatsOrigin = assignedSeats, 
                                    divisor = divisor, 
                                    quota = quota, 
                                    threshold = threshold, 
                                    allowOverhang=allowOverhang)
        else: 
            raise Exception("The PR calculation method'", method ,"' has not yet being implementated.")

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
    
    def getColors(self):
        return self.colors
    
    def getParties(self):
        return list(self.colorPartyNameMapping.keys())

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
    
def create_Map(length, width, method='Uniform', num=7, grid=None, colors=[]):
    return Map(length, width, method, num, grid, colors)
