from typing import List
from statistics import mean
from jmetal.core.solution import FloatSolution

def mean_of_solutions(solutions : List[FloatSolution]):
    return mean([solution.objectives[0] for solution in solutions])