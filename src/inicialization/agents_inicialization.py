from agent.algorithm import EvolutionAlgoritm
from jmetal.operator import SBXCrossover, PolynomialMutation, BinaryTournamentSelection, BitFlipMutation
from jmetal.problem.singleobjective.unconstrained import Rastrigin, Sphere
from jmetal.util.termination_criterion import StoppingByEvaluations
from agent.island import Island
from agent.agent import Agent
from communication.types import AttiduteType, CommunicationWithMutation
from communication.operators import average_operator
from settings import ConfigData


def create_agents_float_solution(config : ConfigData):
    Agents =  []
    for i in range(0,config.noAgents):
        Island1 = Island(algorithm=EvolutionAlgoritm(
        problem=config.problem, 
        population_size=15,
        offspring_population_size= 30,
        mutation=PolynomialMutation(probability=0.0005 , distribution_index=30),
        selection= BinaryTournamentSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=10000000)))
        Island1.start()
        Agents.append(Agent(Island1, name= f"Agent{i}", attidute= AttiduteType( 2), communication_type=config.commuincationType))

    i = config.noAgents//2

    Island2 = Island(algorithm=EvolutionAlgoritm(
    problem=config.problem, 
    population_size=15 ,
    offspring_population_size= 30,
    mutation=PolynomialMutation(probability=0.0005 , distribution_index=40),
    selection= BinaryTournamentSelection(),
    termination_criterion=StoppingByEvaluations(max_evaluations=10000000)))
    Island2.start()
    Agent_Reference = Agent(Island2, name= f"Agent single", attidute= AttiduteType(1), communication_type=config.commuincationType)

    return Agents, Agent_Reference



def create_agents_binary_solution(no_agents, problem, communication_type):
    Agents =  []
    for i in range(0,no_agents):
        Island1 = Island(algorithm=EvolutionAlgoritm(
        problem=problem, 
        population_size=100 -1*i,
        offspring_population_size= 150 -3*i,
        mutation=BitFlipMutation(probability=0.5 + 0.03*i / problem.number_of_variables),
        selection= BinaryTournamentSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=100000)))
        Island1.start()
        Agents.append(Agent(Island1, name= f"Agent{i}", attidute= AttiduteType(i % 3), communication_type=communication_type))

    i = no_agents//2

    Island2 = Island(algorithm=EvolutionAlgoritm(
    problem=problem, 
    population_size=100 -1*i,
    offspring_population_size= 150 -3*i,
    mutation=BitFlipMutation(probability=0.5 + 0.03*i / problem.number_of_variables),
    selection= BinaryTournamentSelection(),
    termination_criterion=StoppingByEvaluations(max_evaluations=100000)))
    Island2.start()
    Agent_Reference = Agent(Island2, name= f"Agent single", attidute= AttiduteType(1), communication_type=CommunicationWithMutation(operator=average_operator))

    return Agents, Agent_Reference