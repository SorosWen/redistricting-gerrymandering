import sys
import unittest
sys.path.append('../src')
from redistricting_simulation import Agent

class TestAgent(unittest.TestCase):
    def test_getCoord(self):
        # test getCoord()
        agent = Agent.create_Agent(1, "red", 19, 15)
        self.assertEqual(agent.getCoord(), (19, 15), "Agent coordinate should be (19, 15).")
    def test_getColor(self):
        # test getColor()
        agent = Agent.create_Agent(1, "red", 19, 15)
        self.assertEqual(agent.getColor(), "red", "Agent color should be 'red'.")
    def test_getColorId(self):
        # test getColorId
        agent = Agent.create_Agent(1, "red", 19, 15)
        self.assertEqual(agent.getColorId(), 1, "Agent colorId should be 1. ")

    def test_setXsetY(self):
        # test setting coordinate
        agent = Agent.create_Agent(1, "red", 19, 15)
        agent.setX(25)
        agent.setY(29)
        self.assertEqual(agent.getCoord(), (25, 29), "Agent coordinate should be (25, 29).")

    def test_setCoord(self):
        agent = Agent.create_Agent(1, "red", 19, 15)
        agent.setCoord(100, 100)
        self.assertEqual(agent.getCoord(), (100, 100), "Agent coordinate should be (100, 100).")

if __name__ == '__main__':
    unittest.main()