from dataclasses import dataclass
import random
from jmetal import logging
from agent.algorithm import EvolutionAlgorithm, S
import numpy as np
from copy import deepcopy
from typing import List


@dataclass
class PopulationsData:
    solution_spread: float
    solution_std: float
    solution_mean: np.array
    result: bool = None


logger = logging.getLogger(__name__)


class Island:
    def __init__(self, algorithm: EvolutionAlgorithm) -> None:
        self.algorithm = algorithm
        self.history_solution = []
        self.history_population = []
        self.populationData = None

    def clear_data_and_start(self):
        self.history_solution = []
        self.history_population = []
        self.start()

    def start(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.algorithm.solutions = self.algorithm.evaluate(self.algorithm.create_initial_solutions())
        self.algorithm.init_progress()

        self.history_population = []
        self.history_solution = []

    def restart_from_random_place(self):
        self.algorithm.solutions = self.algorithm.evaluate(self.algorithm.create_initial_solutions())

    def run(self, iterations):
        for i in range(0, iterations):
            if self.algorithm.stopping_condition_is_met():
                break
            self.algorithm.step()
            self.update_history()
            self.algorithm.update_progress(1)

    def get_algorithm(self):
        return self.algorithm

    def update_history(self):
        best_fitness = self.algorithm.solutions[0].objectives[0]
        self.history_solution.append(best_fitness)

        spread = max([sol.objectives[0] for sol in self.algorithm.solutions]) - min(
            [sol.objectives[0] for sol in self.algorithm.solutions])
        solution_array = np.array([sol.variables for sol in self.algorithm.solutions])

        std = np.mean(np.std(solution_array, axis=0))
        means_sol = np.mean(solution_array, axis=0)
        self.populationData = PopulationsData(solution_spread=spread, solution_std=std, solution_mean=means_sol)
        self.history_population.append(self.populationData)

    def get_history_solution(self):
        return self.history_solution

    def get_solutions(self):
        return deepcopy(self.algorithm.solutions)

    def update_solutions(self, new_population):
        offspring_population = self.algorithm.evaluate(new_population)
        self.algorithm.solutions = self.algorithm.replacement(self.algorithm.solutions, offspring_population)


    def get_population_data(self) -> List[PopulationsData]:
        return self.history_population

    def get_last_population_data(self):
        return self.populationData
