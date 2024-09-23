class Precinct:
    def __init__(self, name="", 
                agents=set(), 
                neighbors = set(), 
                neighsInDisrtrict = set()):
        if name == "":
            raise Exception("Precinct name cannot be null or empty.")
        
        self.name = name
        self.agents = agents
        self.neighbors = neighbors
        self.neighborsInDistrict = neighsInDisrtrict
        self.population = len(agents)
        self.demography = {}
        self.districtId = -1
        self.population = 0
        for agent in agents:
            firstChoice = agent.getFirstChoice()
            if firstChoice not in self.demography.keys():
                self.demography[firstChoice] = 1
            else:
                self.demography[firstChoice] += 1
    
    def addNeighbor(self, newNeighbor):
        self.neighbors.add(newNeighbor)
    
    def addNeighbors(self, neighbors=set()):
        self.neighbors = self.neighbors.union(neighbors)
    
    def addAgents(self, agents=set()):
        self.agents = self.agents.union(agents)
        for agent in agents:
            firstChoice = agent.getFirstChoice()
            if firstChoice not in self.demography.keys():
                self.demography[firstChoice] = 1
            else:
                self.demography[firstChoice] += 1
    
    def moveToNewDistrict(self, district):
        self.neighborsInDistrict = district.precincts.union(self.neighbors)
        self.districtId = district.id
    
    def isAssignedToADistrict(self):
        if self.districtId != -1:
            return True
        return False
    
    def getDistrictId(self):
        return self.districtId

    def getName(self):
        return self.name

    def changeName(self, name):
        self.name = name

    def getNeighbors(self):
        return self.neighbors
    
    def getNeighborsInDistrict(self):
        return self.neighborsInDistrict
    
    def getDemography(self, percentage=False):
        if percentage:
            tempDict = {}
            for party in self.demography.keys():
                tempDict[party] = self.demography[party]/sum(self.demography.values())
            return tempDict
        else:
            return self.demography.copy()
    
    def updateDemography(self):
        self.demography = {}
        for agent in self.agents:
            firstChoice = agent.getFirstChoice()
            if firstChoice in self.demography.keys():
                self.demography[firstChoice] = 1
            else:
                self.demography[firstChoice] += 1

def create_precinct(name="", agents=set(), 
                    neighbors = set(), 
                    neighsInDisrtrict = set()):
    return Precinct(name, agents, neighbors, neighsInDisrtrict)