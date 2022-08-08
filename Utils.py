from typing import List
from statistics import mean
from jmetal.core.solution import Solution


def mean_of_solutions(solutions : List[Solution]):
    return mean([solution.objectives[0] for solution in solutions])

