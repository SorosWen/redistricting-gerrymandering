import sys
import unittest
sys.path.insert(0, '../src')
from electoralSimulation import Precinct, Agent

class TestPrecinct(unittest.TestCase):
    def test_getName(self):
        name = "Middlesex"
        precinct = Precinct.create_precinct(name=name)
        self.assertEqual(precinct.getName(), name)

    def test_getNeighbors(self):
        name = "Middlesex"
        Agent1 = Agent.create_Agent(0, 0, ['Democrat', 'Republican'])
        Agent2 = Agent.create_Agent(0, 0, ['Democrat', 'Republican'])
        Agent3 = Agent.create_Agent(0, 0, ['Democrat', 'Republican'])
        agents = [Agent1, Agent2, Agent3]
        precinct = Precinct.create_precinct(name=name, agents=agents)
        
        for agent in precinct.agents:
            self.assertEqual(agent.getFirstChoice(), 'Democrat')
            self.assertEqual(agent.getChoiceAtPosition(1), 'Republican')

    def test_getDemography(self):
        name = "Middlesex"
        Agent1 = Agent.create_Agent(0, 0, ['Democrat', 'Republican'])
        Agent2 = Agent.create_Agent(0, 0, ['Democrat', 'Republican'])
        Agent3 = Agent.create_Agent(0, 0, ['Democrat', 'Republican'])
        agents = [Agent1, Agent2, Agent3]
        precinct = Precinct.create_precinct(name=name, agents=agents)
        
        self.assertEqual(precinct.getDemography(), {'Democrat':3})
if __name__ == '__main__':
    unittest.main()