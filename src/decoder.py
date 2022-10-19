from jmetal.problem.singleobjective.unconstrained import Rastrigin

from communication.types import CommunicationWithMutation
from communication.operators import swap_operator

def decode_problem(problem_name, problem_size):
    return {"Rastrigin" : Rastrigin(problem_size) }[problem_name]

def decode_operator(operator):
    return {"swap" : swap_operator }[operator]
    
def decode_communication(type, operator):
    return {"communication_with_mutation" : CommunicationWithMutation(decode_operator(operator)) }[type]
