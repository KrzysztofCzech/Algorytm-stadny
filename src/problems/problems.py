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

        self.lower_bound = [-100 for _ in range(number_of_variables)]
        self.upper_bound = [100 for _ in range(number_of_variables)]

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

class ExpandedShaffer(FloatProblem):

    def __init__(self, number_of_variables: int = 10):
        super(ExpandedShaffer, self).__init__()
        self.number_of_objectives = 1
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['f(x)']

        self.lower_bound = [-100 for _ in range(number_of_variables)]
        self.upper_bound = [100 for _ in range(number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def g(self, sum_x2_y2):
        up = math.pow(math.sin(math.sqrt(sum_x2_y2)),2 ) - 0.5
        down = math.pow(1 + 0.001*(sum_x2_y2),2)
        return up/down

    def evaluate(self, solution: FloatSolution) -> FloatSolution:

        x = solution.variables
        sum = 0 
        for i in range(solution.number_of_variables):
            sum += self.g(x[i]**2 + x[(i+1)% solution.number_of_variables]**2)
        solution.objectives[0] = sum
        return solution

    def get_name(self) -> str:
        return 'ExpandedShaffer'

class LenardJohnesMinimumEnergyCluster(FloatProblem):

    def __init__(self, number_of_variables: int = 10):
        super(LenardJohnesMinimumEnergyCluster, self).__init__()
        self.number_of_objectives = 1
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['f(x)']

        self.lower_bound = [-20 for _ in range(number_of_variables)]
        self.upper_bound = [20 for _ in range(number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def d(self, i , j, variables):
        sum_k  = 0
        for k in range(3):
            
            sum_k += math.pow(variables[3 * i + k - 2] - variables[3*j+k-2], 2)
        return math.pow(sum_k,3)


    def evaluate(self, solution: FloatSolution) -> FloatSolution:

        x = solution.variables
        sum = 12.7120622568
        sum_j = 0
        for i in range((solution.number_of_variables-2)//3):
            for j in range(i+1, self.number_of_variables//3):
                d_tmp = self.d(i,j,x)
                sum_j += (1/math.pow(d_tmp,2)) - 2/d_tmp
            sum  += sum_j
        solution.objectives[0] = sum
        return solution

    def get_name(self) -> str:
        return 'LenardJohnesMinimumEnergyCluster'


class BentCigar(FloatProblem):

    def __init__(self, number_of_variables: int = 10):
        super(BentCigar, self).__init__()
        self.number_of_objectives = 1
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['f(x)']

        self.lower_bound = [-100 for _ in range(number_of_variables)]
        self.upper_bound = [100 for _ in range(number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound



    def evaluate(self, solution: FloatSolution) -> FloatSolution:

        x = solution.variables
        sum =0
        for i in range(1,solution.number_of_variables):
            sum  += x[i] * x[i]
        solution.objectives[0] = sum *  10**6 + x[0]*x[0]
        return solution

    def get_name(self) -> str:
        return 'BentCigar'

class Discus(FloatProblem):

    def __init__(self, number_of_variables: int = 10):
        super(Discus, self).__init__()
        self.number_of_objectives = 1
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['f(x)']

        self.lower_bound = [-100 for _ in range(number_of_variables)]
        self.upper_bound = [100 for _ in range(number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound



    def evaluate(self, solution: FloatSolution) -> FloatSolution:

        x = solution.variables
        sum =0
        for i in range(1,solution.number_of_variables):
            sum  += x[i] * x[i]
        solution.objectives[0] = sum +  10**6 * x[0]*x[0]
        return solution

    def get_name(self) -> str:
        return 'Discus'