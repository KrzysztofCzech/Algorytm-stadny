from enum import Enum

from communication.operators import crossover, mutation
from utils.utils import mean_of_solutions
class AttiduteType(Enum):
    GOOD = 0
    MEDIUM = 1
    BAD = 2


class CommunicationType():

    def comunnicate(self, agent1, agent2):
        raise NotImplementedError()

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
                agent1.update_trust(agent2.name, 1)


class CommunicationWithMutation(CommunicationType):
    
    def __init__(self, operator):
        self.operator = operator

    def comunnicate(self, agent1, agent2):
        best_fitness = agent1.Island.algorithm.solutions[0].objectives[0]
        best_fitness1 = min([sol.objectives[0] for sol in agent1.Island.algorithm.solutions])
        new_population = agent2.transfer_data(agent1.name)
        solutions_old = agent1.get_solutions()
        mean_old = mean_of_solutions(solutions_old)
        mean_new = mean_of_solutions(new_population)
        if mean_new < mean_old:
            new_population = mutation(solutions_old, new_population, self.operator, agent1.get_trust(agent2.name))
            agent1.Island.update_solutions(new_population)
            best_fitness2 = agent1.Island.algorithm.solutions[0].objectives[0]
            if best_fitness2 > best_fitness:
                print('fail 1')
            if best_fitness2 > best_fitness1:
                print('fail 2')

            solutions_new = agent1.get_solutions()
            mean_updated = mean_of_solutions(solutions_new)
            if mean_updated < mean_old:
                agent1.update_trust(agent2.name, 1)



def get_selector(attidute :  AttiduteType):
    return {AttiduteType.GOOD : lambda num, list : list[0: num], 
            AttiduteType.MEDIUM : lambda num, list : list[(len(list) - num)//2 : (len(list) + num)//2], 
            AttiduteType.BAD : lambda num, list : list[-num :]
    }[attidute]








