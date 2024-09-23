import unittest
import sys
sys.path.insert(0, '../src')
from electoralSimulation import CalculationMethod as cm
from electoralSimulation import Agent

class TestMap(unittest.TestCase):
    def test_FPTP(self):
        candidateVotes = {'McCarthy':120, 'Pelosi':110, 'Harley':150, 'Baker':100} 
        winner = cm.FPTP(candidateVotes)
        self.assertEqual(winner, "Harley")
    
    def test_LargestRemainder(self):
        partyListResult = {'Party1':1000, 'Party2':1200, 'Party3':1300}
        totalSeats = 100
        assignedSeats = cm.LargestRemainder(partyListResult, totalSeats)
        self.assertEqual(assignedSeats, {'Party1': 29, 'Party2': 34, 'Party3': 37})

    def test_HighestAverage_DHondt(self):
        partyListResult = {'Party1':47000, 'Party2':16000, 'Party3':15900, 
                            'Party4':12000, 'Party5':6000, 'Party6':3100}
        totalSeats = 10
        assignedSeats = cm.HighestAverage(partyListResult, totalSeats, divisor="D'Hondt")
        self.assertEqual(assignedSeats, {'Party1': 5, 'Party2': 2, 'Party3': 2, 'Party4':1, 
                                        'Party5':0, 'Party6':0})

    def test_HighestAverage_Webster(self):
        partyListResult = {'Party1':47000, 'Party2':16000, 'Party3':15900, 
                            'Party4':12000, 'Party5':6000, 'Party6':3100}
        totalSeats = 10
        assignedSeats = cm.HighestAverage(partyListResult, totalSeats, divisor="Webster")
        self.assertEqual(assignedSeats, {'Party1': 4, 'Party2': 2, 'Party3': 2, 'Party4':1, 
                                        'Party5':1, 'Party6':0})
                                    
    def test_HighestAverage_HuntingtonHill(self):
        partyListResult = {'Party1':47000, 'Party2':16000, 'Party3':15900, 
                            'Party4':12000, 'Party5':6000, 'Party6':3100}
        totalSeats = 10
        assignedSeats = cm.HighestAverage(partyListResult, totalSeats, divisor="Huntington–Hill", quota='Droop')
        self.assertEqual(assignedSeats, {'Party1': 5, 'Party2': 2, 'Party3': 2, 'Party4':1, 
                                        'Party5':0, 'Party6':0})

    def test_HighestAverage_Adams(self):
        partyListResult = {'Party1':47000, 'Party2':16000, 'Party3':15900, 
                            'Party4':12000, 'Party5':6000, 'Party6':3100}
        totalSeats = 10
        assignedSeats = cm.HighestAverage(partyListResult, totalSeats, divisor="Adams", quota='Droop')
        self.assertEqual(assignedSeats, {'Party1': 4, 'Party2': 2, 'Party3': 2, 'Party4':2, 
                                        'Party5':0, 'Party6':0})

    def test_RankChoiceVoting_OneAchieveMajority(self):
        agent1 = Agent.create_Agent(x=1, y=1, choices=["A", "B", "C"])
        agent2 = Agent.create_Agent(x=1, y=1, choices=["B", "A", "C"])
        agent3 = Agent.create_Agent(x=1, y=1, choices=["A", "D", "A"])
        agent4 = Agent.create_Agent(x=1, y=1, choices=["B", "D", "C"])
        agent5 = Agent.create_Agent(x=1, y=1, choices=["C", "A", "B"])
        agents = [agent1, agent2, agent3, agent4, agent5]
        winner = cm.RankChoiceVoting(agents)
        self.assertEqual(winner, "A")

if __name__ == '__main__':
    unittest.main()