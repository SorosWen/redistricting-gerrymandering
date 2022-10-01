import sys
import unittest
import time
import matplotlib.pyplot as plt
import matplotlib.colors
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
    #     map.showMap()
    #     self.assertTrue(True)
    
    # def test_drawDistricts(self):
    #     map = Map.create_Map(50, 50)
    #     map.initialize(method="Warsaw")
    #     map.drawDistricts(2)
    #     # map.showMap()
    #     # map.showAllDistricts()
    #     map.showAllDistricts(method="compact")
    #     self.assertTrue(True)

    # def test_extremeMap(self):
    #     map = Map.create_Map(100, 100)
    #     map.initialize(method="Warsaw")
    #     print(map.getDemography())
    #     map.showMap()
    #     map.drawDistricts(27)
    #     map.showAllDistricts(method='grid')
    #     map.showAllDistricts(method="compact")
    #     map.showParliamentComposition(method='arch')
    #     print(map.getDistrictsPopulation())
    #     self.assertTrue(True)
    
    # def test_districtDrawing(self):
    #     map = Map.create_Map(200, 100)
    #     map.initialize(method="Uniform")
    #     map.showMap()
    #     print("Demography:", map.getDemography())
    #     for i in range(3):
    #         map.drawDistricts(47)
    #         print("ParliamentComposition:", map.showParliamentComposition(method='summary'))
    #         map.showParliamentComposition(method='arch', legend = True, showNumber=True)
    #     self.assertTrue(True)

    def test_Parallel(self):
        timeMark = time.time()
        map = Map.create_Map(150, 170)
        map.initialize(method="Warsaw")
        print("Map creation Duration: ", time.time() - timeMark)
        
        map.showMap()
        map.showDemography()
        map.showDemography(percentage=True)
        print("Demography:", map.getDemography(), map.getDemography(percentage=True))
        
        timeMark = time.time()
        map.drawDistricts(31, animate=True)
        print("Time spent on drawing district:", time.time()-timeMark)
        
        # map.showAllDistricts(method = 'compact')

        # map.showParliamentComposition(displayMethod='arch', electoralSystem = "majoritarian", 
        #                             districtCalculationMethod='FPTP', 
        #                             legend = True, showNumber=True, showTitle=True)
        # map.showParliamentComposition(displayMethod='arch', electoralSystem = "parallel", 
        #                             districtCalculationMethod='FPTP', PRCalculationMethod="LargestRemainder", 
        #                             seatsInParliament = 61, legend = True, showNumber=True, showTitle=True)
        # map.showParliamentComposition(displayMethod='arch', electoralSystem = "MMP", 
        #                             districtCalculationMethod='FPTP', PRCalculationMethod="LargestRemainder", 
        #                             overhangSeats = 'Allow', 
        #                             seatsInParliament = 61, legend = True, showNumber=True, showTitle=True)
        # map.showParliamentComposition(displayMethod='arch', electoralSystem = "proportionalRepresentation", 
        #                             PRCalculationMethod="LargestRemainder", 
        #                             seatsInParliament = 61, legend = True, showNumber=True, showTitle=True)

if __name__ == '__main__':
    unittest.main()