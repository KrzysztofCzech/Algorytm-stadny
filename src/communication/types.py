from enum import Enum
import logging
from communication.operators import crossover
from agent.base_agent import BaseAgent
from utils.utils import mean_of_solutions
from  primitives.primitiveTypes import *
class AttiduteType(Enum):
    GOOD = 0
    MEDIUM = 1
    BAD = 2




class CommunicationCrossover(CommunicationType):
    
    def __init__(self, operator):
        self.crossover_operator = operator

    def comunnicate(self, agent1, agent2):
        new_population = agent2.transfer_data(agent1.name)
        solutions_old = agent1.get_solutions()
        mean_old = mean_of_solutions(solutions_old)
        mean_new = mean_of_solutions(new_population)
        if mean_new < mean_old:
            new_population = crossover(solutions_old, new_population, self.crossover_operator)
            agent1.Island.update_solutions(new_population)
            solutions_new = agent1.get_solutions()
            mean_updated = mean_of_solutions(solutions_new)
            if mean_updated < mean_old:
                agent1.get_trust_memory().update_trust(agent1.name,agent2.name, 1)
                return True
        return False

class CommunicationWithMutation(CommunicationType):
    
    def __init__(self, operator, mutation_type):
        self.operator = operator
        self.mutation_type = mutation_type

    def comunnicate(self, agent1 : BaseAgent , agent2: BaseAgent):
        new_population = agent2.transfer_data(agent1.name)
        solutions_old = agent1.get_solutions()
        mean_old = mean_of_solutions(solutions_old)
        mean_new = mean_of_solutions(new_population)
        if (mean_new- mean_old) < abs(mean_old):
            new_population = self.mutation_type(solutions_old, new_population, self.operator, agent1.get_trust_memory().get_trust_value(agent2.name))
            agent1.Island.update_solutions(new_population)

            solutions_new = agent1.get_solutions()
            mean_updated = mean_of_solutions(solutions_new)
            if mean_updated < mean_old:
                agent1.get_trust_memory().update_trust(agent1.name,agent2.name, 1)
                return True            
        else:
            agent1.get_trust_memory().update_trust(agent1.name,agent2.name, -1)   
        return False



def get_selector(attidute :  AttiduteType):
    return {AttiduteType.GOOD : lambda num, list : list[0: num], 
            AttiduteType.MEDIUM : lambda num, list : list[(len(list) - num)//2 : (len(list) + num)//2], 
            AttiduteType.BAD : lambda num, list : list[-num :]
    }[attidute]








