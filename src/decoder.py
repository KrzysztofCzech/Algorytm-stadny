from jmetal.problem.singleobjective.unconstrained import Rastrigin

from communication.types import CommunicationWithMutation, CommunicationCrossover, CommunicationWithMutation_temp1, CommunicationWithMutation_temp2
from jmetal.operator import SBXCrossover
from communication.operators import swap_operator, average_operator

def decode_problem(problem_name, problem_size):
    return {"Rastrigin" : Rastrigin(problem_size) }[problem_name]

def decode_operator(operator):
    return {"swap" : swap_operator,
    "average": average_operator }[operator]
    
def decode_communication(type, operator):
    return {"mutation" : CommunicationWithMutation(decode_operator(operator)),
    "crossover": CommunicationCrossover(operator=SBXCrossover(probability=0.04)),
    "temp1": CommunicationWithMutation_temp1(decode_operator(operator)),
    "temp2": CommunicationWithMutation_temp2(decode_operator(operator))}[type]
