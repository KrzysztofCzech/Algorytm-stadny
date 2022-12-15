import math
import random

from jmetal.core.problem import  FloatProblem
from jmetal.core.solution import FloatSolution

class Griewank(FloatProblem):

    def __init__(self, number_of_variables: int = 10):
        super(Griewank, self).__init__()
        self.number_of_objectives = 1
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['f(x)']

        self.lower_bound = [-500 for _ in range(number_of_variables)]
        self.upper_bound = [500 for _ in range(number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        a = 4000.0
        result = 1
        x = solution.variables
        temp =1 
        for i in range(solution.number_of_variables):
            result += (x[i] * x[i])/a
            temp*= math.cos(x[i]/(i+1)*math.sqrt(i+1))
        result-=temp
        solution.objectives[0] = result

        return solution

    def get_name(self) -> str:
        return 'Griewank'
