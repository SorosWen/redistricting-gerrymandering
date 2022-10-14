import sys
import unittest
sys.path.append('../src')
from redistricting_simulation import Agent

class TestAgent(unittest.TestCase):
    def test_getCoord(self):
        # test getCoord()
        agent = Agent.create_Agent(19, 15, [1])
        self.assertEqual(agent.getCoord(), (19, 15), "Agent coordinate should be (19, 15).")
    def test_getColorId(self):
        # test getColorId
        agent = Agent.create_Agent(19, 15, [1])
        self.assertEqual(agent.getColorId(), 1, "Agent colorId should be 1. ")
    def test_getFirstChoice(self):
        agent = Agent.create_Agent(19, 15, ["A", "B", "C"])
        self.assertEqual(agent.getFirstChoice(), "A", "Agent first choice should be A. ")
    def test_getChoiceAtPosition_1(self):
        agent = Agent.create_Agent(19, 15, ["A", "B", "C"])
        self.assertEqual(agent.getChoiceAtPosition(0), "A", "Agent first choice should be A. ")
    def test_getChoiceAtPosition_2(self):
        agent = Agent.create_Agent(19, 15, ["A", "B", "C"])
        self.assertEqual(agent.getChoiceAtPosition(1), "B", "Agent second choice should be B. ")
    def test_getChoiceAtPosition_3(self):
        agent = Agent.create_Agent(19, 15, ["A", "B", "C"])
        self.assertEqual(agent.getChoiceAtPosition(2), "C", "Agent third choice should be C. ")

    def test_setXsetY(self):
        # test setting coordinate
        agent = Agent.create_Agent(19, 15, [1])
        agent.setX(25)
        agent.setY(29)
        self.assertEqual(agent.getCoord(), (25, 29), "Agent coordinate should be (25, 29).")
    def test_setCoord(self):
        agent = Agent.create_Agent(19, 15, [1])
        agent.setCoord(100, 100)
        self.assertEqual(agent.getCoord(), (100, 100), "Agent coordinate should be (100, 100).")
    def test_setChoices(self):
        agent = Agent.create_Agent(19, 15, ["A"])
        agent.setChoices(["A", "B", "C"])
        self.assertEqual(agent.getFirstChoice(), "A", "Agent first choice should be A. ")
        self.assertEqual(agent.getChoiceAtPosition(0), "A", "Agent first choice should be A. ")
        self.assertEqual(agent.getChoiceAtPosition(1), "B", "Agent second choice should be B. ")
        self.assertEqual(agent.getChoiceAtPosition(2), "C", "Agent third choice should be C. ")
    def test_setChoiceAtPosition(self):
        agent = Agent.create_Agent(19, 15, ["A"])
        agent.setChoiceAtPosition(0, "B")
        self.assertEqual(agent.getFirstChoice(), "B", "Agent first choice should be B. ")
    def test_setChoiceAtPosition_OutOfRange(self):
        agent = Agent.create_Agent(19, 15, ["A"])
        try:
            agent.setChoiceAtPosition(1, "B")
        except:
            self.assertTrue(True)
            return
        self.assertTrue(False, "setChoiceAtPosition() is expected to fail due to index out of range but succeeded instead.")

if __name__ == '__main__':
    unittest.main()