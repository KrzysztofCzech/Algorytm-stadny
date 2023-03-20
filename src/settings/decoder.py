from jmetal.problem.singleobjective.unconstrained import Rastrigin
from problems.problems import Griewank, Ackley, ExpandedShaffer, LenardJohnesMinimumEnergyCluster, BentCigar, Discus

from communication.types import CommunicationWithMutation, CommunicationCrossover
from jmetal.operator import SBXCrossover
from communication.operators import swap_operator, average_operator, mutation_many_many_variables, mutation_many_one_variable, mutation_one_many_variables
from trust.base_trust import NaiveTrust, GlobalTrust
from settings.enumStrings import trustMembers



def decode_problem(problem_name, problem_size):
    return {"Rastrigin" : Rastrigin(problem_size),
            "Griewank": Griewank(problem_size),
            "Ackley": Ackley(problem_size),
            "EnergyCluster":  LenardJohnesMinimumEnergyCluster(problem_size),
            "BentCigar":  BentCigar(problem_size),
            "Discus":  Discus(problem_size),
            "ExpandedShaffer": ExpandedShaffer(problem_size)}[problem_name]

def decode_operator(operator):
    return {"swap" : swap_operator,
    "average": average_operator }[operator]
    
def decode_communication(type, operator):
    return {"mutation_one_many" : CommunicationWithMutation(decode_operator(operator), mutation_one_many_variables ),
    "crossover": CommunicationCrossover(operator=SBXCrossover(probability=0.04)),
    "mutation_many_one": CommunicationWithMutation(decode_operator(operator), mutation_many_one_variable),
    "mutation_many_many": CommunicationWithMutation(decode_operator(operator), mutation_many_many_variables)}[type]

def decode_trust(trust):
    return {"naive" : NaiveTrust(trust[trustMembers.START], trust[trustMembers.MAX]),
            "global":  GlobalTrust(trust[trustMembers.START], trust[trustMembers.MAX])}[trust[trustMembers.TYPE]]
 