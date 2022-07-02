from enum import Enum
from abc import ABC, abstractmethod
from types import NotImplementedType
from Utils import mean_of_solutions

class AttiduteType(Enum):
    GOOD = 0
    MEDIUM = 1
    BAD = 2


class CommunicationType():

    def comunnicate(self, agent1, agent2):
        raise NotImplementedError()

class CommunicationBasic(CommunicationType):
    
    def __init__(self):
        pass

    def comunnicate(self, agent1, agent2):
        new_population = agent2.transfer_data(agent1.name)
        solutions_old = agent1.get_solution()
        mean_old = mean_of_solutions(solutions_old)
        mean_new = mean_of_solutions(new_population)
        if mean_new < mean_old:
            agent1.Island.update_solutions(new_population)
            solutions_new = agent1.get_solution()
            mean_updated = mean_of_solutions(solutions_new)
            if mean_updated < mean_old:
                agent1.update_trust(agent2.name, 1)




def get_selector(attidute :  AttiduteType):
    return {AttiduteType.GOOD : lambda num, list : list[0: num], 
            AttiduteType.MEDIUM : lambda num, list : list[(len(list) - num)//2 : (len(list) + num)//2], 
            AttiduteType.BAD : lambda num, list : list[-num :]
    }[attidute]






