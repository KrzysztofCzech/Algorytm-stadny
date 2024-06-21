from enum import Enum
import logging
from communication.operators import crossover
from agent.base_agent import BaseAgent
from utils.utils import mean_of_solutions
from primitives.primitiveTypes import *


class AttitudeType(Enum):
    GOOD = 0
    MEDIUM = 1
    BAD = 2


class CommunicationCrossover(CommunicationType):

    def __init__(self, operator):
        super()
        self.operator = operator

    def communicate(self, agent1, agent2):
        new_population = agent2.transfer_data(agent1.name)
        solutions_old = agent1.get_solutions()
        mean_old = mean_of_solutions(solutions_old)
        mean_new = mean_of_solutions(new_population)
        if mean_new < mean_old:
            new_population = crossover(solutions_old, new_population, self.operator)
            agent1.Island.update_solutions(new_population)
            solutions_new = agent1.get_solutions()
            mean_updated = mean_of_solutions(solutions_new)
            if mean_updated < mean_old:
                agent1.get_trust_memory().update_trust(agent1.name, agent2.name, 1)
                return True
        return False
    
    def __str__(self) -> str:
        return "Crossover"


class CommunicationMigration(CommunicationType):
    def communicate(self, agent1, agent2):
        new_population = agent2.transfer_data(agent1.name)[0]
        agent1.Island.update_solutions([new_population])
        return True


class CommunicationWithMutation(CommunicationType):

    def __init__(self, operator, mutation_type):
        super()
        self.operator = operator
        self.mutation_type = mutation_type

    def communicate(self, agent1: BaseAgent, agent2: BaseAgent):
        new_population = agent2.transfer_data(agent1.name)
        solutions_old = agent1.get_solutions()
        mean_old = mean_of_solutions(solutions_old)
        mean_new = mean_of_solutions(new_population)
        if (mean_new - mean_old) < abs(mean_old):
            new_population = self.mutation_type(solutions_old, new_population, self.operator,
                                                agent1.get_trust_memory().get_trust_value(agent2.name))
            agent1.Island.update_solutions(new_population)

            solutions_new = agent1.get_solutions()
            mean_updated = mean_of_solutions(solutions_new)
            if mean_updated < mean_old:
                agent1.get_trust_memory().update_trust(agent1.name, agent2.name, 1)
                return True
        else:
            agent1.get_trust_memory().update_trust(agent1.name, agent2.name, -1)
        return False
    
        
    def __str__(self) -> str:
        return "Mutation"


def get_selector(attidute: AttitudeType):
    return {AttitudeType.GOOD: lambda num, list_sol: list_sol[0: num],
            AttitudeType.MEDIUM: lambda num, list_sol: list_sol[(len(list_sol) - num) // 2: (len(list_sol) + num) // 2],
            AttitudeType.BAD: lambda num, list_sol: list_sol[-num:]
            }[attidute]
