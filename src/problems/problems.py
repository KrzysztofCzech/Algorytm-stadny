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
        tmp =1 
        for i in range(solution.number_of_variables):
            result += (x[i] * x[i])/a
            tmp*= math.cos(x[i]/(i+1)*math.sqrt(i+1))
        result-=tmp
        solution.objectives[0] = result

        return solution

    def get_name(self) -> str:
        return 'Griewank'

class Ackley(FloatProblem):

    def __init__(self, number_of_variables: int = 10):
        super(Ackley, self).__init__()
        self.number_of_objectives = 1
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['f(x)']

        self.lower_bound = [-50 for _ in range(number_of_variables)]
        self.upper_bound = [50 for _ in range(number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        a = 20.0
        b = 0.2
        c = 2*math.pi
        x = solution.variables
        sum_squares = 0
        sum_cos = 0
        for i in range(solution.number_of_variables):
            sum_squares += (x[i] * x[i])
            sum_cos += math.cos(x[i]*c)  
        solution.objectives[0] = -a*math.exp(-b*math.sqrt(sum_squares/self.number_of_variables)) - math.exp(sum_cos/self.number_of_variables) +a + math.exp(1)
        return solution

    def get_name(self) -> str:
        return 'Ackley'
