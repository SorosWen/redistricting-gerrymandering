class Precinct:
    def __init__(self, name, neighbors = set(), neighInDisrtrict = set()):
        self.neighbors = set()
        self.votes = {}
        self.agents = set()
        self.neighbors = neighbors
        self.neighborsInDistrict = neighInDisrtrict
    
    def addNeighbor(self, newNeighbor):
        self.neighbors.add(newNeighbor)
    
    def moveToNewDistrict(self, newNeighbors):
        self.neighborsInDistrict = newNeighbors; 
    
    def getNeighbors(self):
        return self.neighbors
    
    def getNeighborsInDistrict(self):
        return self.neighborsInDistrict
    
    