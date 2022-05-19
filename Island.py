from dataclasses import dataclass
import random
from jmetal import logging 
from jmetal.algorithm.singleobjective.evolution_strategy import EvolutionStrategy
from jmetal.util.solution import get_non_dominated_solutions

from Evolutionary_algorithm import S

@dataclass
class PopulationsData:
    solution_spread : float    
    

logger = logging.getLogger(__name__)
class Island():
    def __init__(self, algorithm : EvolutionStrategy) -> None:
        self.algorithm = algorithm
        self.history_solution = []
        self.history_population = []

    def start(self,seed):
        random.seed(seed)
        self.algorithm.solutions = self.algorithm.create_initial_solutions()
        self.algorithm.solutions = self.algorithm.evaluate(self.algorithm.solutions)

        self.algorithm.init_progress()

    
    def run(self,iterations):
        for i in range(0,iterations):
            self.algorithm.step()
            self.algorithm.update_progress()
            self.update_history()

            
    def get_algorithm(self):
        return self.algorithm

    def update_history(self):
        best_fitness = self.algorithm.solutions[0].objectives[0]
        self.history_solution.append(best_fitness)
        
        spread = max([sol.objectives[0] for sol in self.algorithm.solutions]) -  min([sol.objectives[0] for sol in self.algorithm.solutions])
        populationData = PopulationsData(solution_spread= spread)
        self.history_population.append(populationData)

    def get_history_soultion(self):
        return self.history_solution

    def get_solutions(self):
        return self.algorithm.solutions

    def update_solutions(self, new_solutions):
        mating_population = self.algorithm.selection(self.algorithm.solutions + new_solutions)
        offspring_population = self.algorithm.reproduction(mating_population)
        offspring_population = self.algorithm.evaluate(offspring_population)

        self.algorithm.solutions = self.algorithm.replacement(self.algorithm.solutions + new_solutions, offspring_population)
        
        self.update_history()
        