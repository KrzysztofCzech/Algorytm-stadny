from Evolutionary_algorithm import EvolutionAlgoritm
from jmetal.operator import SBXCrossover, PolynomialMutation, BinaryTournamentSelection
from jmetal.problem.singleobjective.unconstrained import Rastrigin, Sphere
from jmetal.util.termination_criterion import StoppingByEvaluations
from Island import Island
from Agent import Agent
from communication import AttiduteType
from communication import CommuncationWithMutation
from communication_operators import average_operator


def create_agents_float_solution(no_agents, problem, communication_type):
    Agents =  []
    for i in range(0,no_agents):
        Island1 = Island(algorithm=EvolutionAlgoritm(
        problem=problem, 
        population_size=50 -1*i,
        offspring_population_size= 100 -3*i,
        mutation=PolynomialMutation(probability=0.5 + 0.03*i / problem.number_of_variables, distribution_index=20 +i),
        crossover= SBXCrossover(probability=0.04 * i + 0.01),
        selection= BinaryTournamentSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=100000)))
        Island1.start()
        Agents.append(Agent(Island1, name= f"Agent{i}", attidute= AttiduteType(i % 3), communication_type=communication_type))

    i = no_agents//2

    Island2 = Island(algorithm=EvolutionAlgoritm(
    problem=problem, 
    population_size=50 -1*i,
    offspring_population_size= 100 -3*i,
    mutation=PolynomialMutation(probability=0.5 + 0.03*i / problem.number_of_variables, distribution_index=20 +i),
    crossover= SBXCrossover(probability=0.04 * i + 0.01),
    selection= BinaryTournamentSelection(),
    termination_criterion=StoppingByEvaluations(max_evaluations=100000)))
    Island2.start()
    Agent_Reference = Agent(Island2, name= f"Agent single", attidute= AttiduteType(1), communication_type=CommuncationWithMutation(operator=average_operator))

    return Agents, Agent_Reference



def create_agents_binary_solution(no_agents):
    pass