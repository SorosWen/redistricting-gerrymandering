import sys
import unittest
import time
import matplotlib.pyplot as plt
sys.path.insert(0, '../src')
from redistricting_simulation import Map

class TestMap(unittest.TestCase):
    # def test_getColorIds(self):
    #     map = Map.create_Map(2,2)
    #     map.initialize(method='customize', num=4, grid = [[1, 2], [3, 4]])
    #     self.assertEqual(map.getColorIds(), [[1, 2], [3, 4]], "The grid under customization mode is not identical.")

    # def test_showMap(self):
    #     map = Map.create_Map(50, 50)
    #     map.initialize(method="Warsaw")
    #     self.assertTrue(True)
    
    # def test_drawDistricts(self):
    #     map = Map.create_Map(50, 50)
    #     map.initialize(method="Warsaw")
    #     map.drawDistricts(2)
    #     # map.showAllDistricts()
    #     self.assertTrue(True)

    # def test_extremeMap(self):
    #     map = Map.create_Map(100, 100)
    #     map.initialize(method="Warsaw")
    #     print(map.getDemography())
    #     map.drawDistricts(27)
    #     # map.showAllDistricts()
    #     # map.showAllDistricts()
    #     # map.showParliamentComposition()
    #     print(map.getDistrictsPopulation())
    #     self.assertTrue(True)
    
    # def test_districRedrawing(self):
    #     map = Map.create_Map(200, 100)
    #     map.initialize(method="Uniform")
    #     print("Demography:", map.getDemography())
    #     for i in range(3):
    #         map.drawDistricts(10)
    #         print("ParliamentComposition:", map.showParliamentComposition(displayMethod='summary'))
    #     self.assertTrue(True)

    # def test_DistrictsDisplay(self):
    #     map = Map.create_Map(100, 120)
    #     map.initialize(method="Indiana")
    #     map.drawDistricts(numOfDistrict=10)
    #     for i in range(10):
    #         map.showDistrict(i)

    def test_AllUseCases(self):
        map = Map.create_Map(120, 150, method="Indiana")
        
        map.showMap()
        map.showDemography()
        map.showDemography(percentage=True)
        print("Demography:", map.getDemography(), map.getDemography(percentage=True))
        
        timeMark = time.time()
        map.drawDistricts(numOfDistrict=40)
        print("Time spent on drawing district:", time.time()-timeMark)
        
        map.showAllDistricts(method="grid")

        seats = 199

        map.showParliamentComposition(electoralSystem = "majoritarian", 
                                    districtCalculationMethod='FPTP', 
                                    showTitle=True)
        map.showParliamentComposition(electoralSystem = "majoritarian", 
                                    districtCalculationMethod='RankChoiceVoting', 
                                    showTitle=True)

        map.showParliamentComposition(electoralSystem = "parallel", 
                                    districtCalculationMethod='FPTP', PRCalculationMethod="LargestRemainder", 
                                    seatsInParliament = seats, showTitle=True)
        map.showParliamentComposition(electoralSystem = "parallel", 
                                    districtCalculationMethod='RankChoiceVoting', PRCalculationMethod="LargestRemainder", 
                                    seatsInParliament = seats, showTitle=True)
        map.showParliamentComposition(electoralSystem = "parallel", 
                                    districtCalculationMethod='FPTP', PRCalculationMethod="HighestAverage", 
                                    seatsInParliament = seats, showTitle=True)

        map.showParliamentComposition(electoralSystem = "MMP", 
                                    districtCalculationMethod='FPTP', PRCalculationMethod="LargestRemainder", 
                                    allowOverhangSeats = True, 
                                    seatsInParliament = seats, showTitle=True)
        map.showParliamentComposition(electoralSystem = "MMP", 
                                    districtCalculationMethod='RankChoiceVoting', PRCalculationMethod="HighestAverage", 
                                    allowOverhangSeats = True, 
                                    seatsInParliament = seats, showTitle=True)

        map.showParliamentComposition(electoralSystem = "proportionalRepresentation", 
                                    PRCalculationMethod="LargestRemainder", 
                                    seatsInParliament = seats, showTitle=True)

if __name__ == '__main__':
    unittest.main()