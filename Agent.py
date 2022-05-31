from ast import Str
from Island import Island
from communication import AttiduteType, get_selector
from statistics import mean
from jmetal.core.solution import FloatSolution
from typing import List


def mean_of_solutions(solutions : List[FloatSolution]):
    return mean([solution.objectives[0] for solution in solutions])

class Agent():
    def __init__ (self,Island:Island, name: Str, attidute : AttiduteType):
        self.Island = Island
        self.name = name
        self.trust_dict = {}
        self.attidute = attidute


    def run(self, iterations):
        self.Island.run(iterations)

    def get_result(self):
        return self.Island.algorithm.get_result()

    def get_solution(self):
        return self.Island.get_solutions()

    def transfer_data(self, name_other):
        trust_level = self.check_trust(name_other)
        selector = get_selector(self.attidute)
        return selector(trust_level, self.get_solution())


    def communicate(self, obj):
        
        new_population = obj.transfer_data(self.name)
        solutions_old = self.get_solution()
        mean_old = mean_of_solutions(solutions_old)
        mean_new = mean_of_solutions(new_population)
        if mean_new < mean_old:
            self.Island.update_solutions(new_population)
            solutions_new = self.get_solution()
            mean_update = mean_of_solutions(solutions_new)
            if mean_update < mean_old:
                self.update_trust(obj.name, 1)






    def get_num_of_iteration(self):
        return len(self.Island.get_history_soultion())

    def check_trust(self, name_other) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        
        return self.trust_dict[name_other]

    def update_trust(self, name_other: Str, val: int) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        self.trust_dict[name_other] += val




    

