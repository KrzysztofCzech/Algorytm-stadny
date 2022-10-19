from dataclasses import dataclass
import random
from jmetal import logging 
from agent.algorithm import EvolutionAlgoritm, S

from copy import deepcopy

@dataclass
class PopulationsData:
    solution_spread : float    
    

logger = logging.getLogger(__name__)
class Island():
    def __init__(self, algorithm : EvolutionAlgoritm) -> None:
        self.algorithm = algorithm
        self.history_solution = []
        self.history_population = []

    def clear_data_and_start(self):
        self.history_solution = []
        self.history_population = []
        self.start()

    def start(self,seed =None):
        if seed is not None:
            random.seed(seed)
        self.algorithm.solutions = self.algorithm.create_initial_solutions()
        self.algorithm.solutions = self.algorithm.evaluate(self.algorithm.solutions)

        self.algorithm.init_progress()

        self.history_population = []
        self.history_solution = []

    
    def run(self,iterations):
        for i in range(0,iterations):
            self.algorithm.step()
            self.algorithm.update_progress()
            self.update_history()

            
    def get_algorithm(self):
        return self.algorithm

    def update_history(self):
        best_fitness = self.algorithm.solutions[0].objectives[0]
        if len(self.history_population) and self.history_solution[-1] < best_fitness:
            print(len(self.history_population))
        self.history_solution.append(best_fitness)
        
        spread = max([sol.objectives[0] for sol in self.algorithm.solutions]) -  min([sol.objectives[0] for sol in self.algorithm.solutions])
        populationData = PopulationsData(solution_spread= spread)
        self.history_population.append(populationData)

    def get_history_soultion(self):
        return self.history_solution

    def get_solutions(self):
        return deepcopy(self.algorithm.solutions)

    def update_solutions(self, new_population):
        best =  min([sol.objectives[0] for sol in self.algorithm.solutions])
        offspring_population = self.algorithm.evaluate(new_population)
        best1 =  min([sol.objectives[0] for sol in self.algorithm.solutions])

        self.algorithm.solutions = self.algorithm.replacement(self.algorithm.solutions, offspring_population)
        best2 =  min([sol.objectives[0] for sol in self.algorithm.solutions])
        if best2  >best:
            print("not working 2222")
            print(f"best1 {best1}")
            print(f"best2 {best2}")
            print(f"best {best}")

        if best2  >best1:
            print("not working 3333")
            print(f"best1 {best1}")
            print(f"best2 {best2}")
            print(f"best {best}")

        