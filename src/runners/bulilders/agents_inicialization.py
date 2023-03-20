from agent.algorithm import EvolutionAlgoritm
from jmetal.operator import PolynomialMutation, BinaryTournamentSelection,SBXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from agent.island import Island
from agent.agent import Agent
from communication.types import AttiduteType
from settings.settings import AgentConfigData


def create_agents_all_equal(config : AgentConfigData):
    Agents =  []
    for i in range(0,config.noAgents):
        Island1 = Island(algorithm=EvolutionAlgoritm(
        problem=config.problem, 
        population_size=config.population_size,
        offspring_population_size= config.offspring_population,
        mutation=PolynomialMutation(probability=0.0005 , distribution_index=40  ),
        selection= BinaryTournamentSelection(),
        crossover=SBXCrossover(probability=0.005),
        termination_criterion=StoppingByEvaluations(max_evaluations=10000000)))
        Island1.start()
        Agents.append(Agent(Island1, name= f"Agent{i}", attidute= AttiduteType( 2), communication_type=config.commuincationType, trust_type=config.trust_type))

    i = config.noAgents//2

    Island2 = Island(algorithm=EvolutionAlgoritm(
    problem=config.problem, 
    population_size=config.population_size,
    offspring_population_size= config.offspring_population,
    mutation=PolynomialMutation(probability=0.0005 , distribution_index=40),
    selection= BinaryTournamentSelection(),
    crossover=SBXCrossover(probability=0.005),
    termination_criterion=StoppingByEvaluations(max_evaluations=1000000000)))
    Island2.start()
    Agent_Reference = Agent(Island2, name= f"Agent single", attidute= AttiduteType(1), communication_type=config.commuincationType, trust_type=config.trust_type)

    return Agents, Agent_Reference


def create_agents_different_probability(config : AgentConfigData, factor : float):
    Agents =  []
    for i in range(0,config.noAgents):
        Island1 = Island(algorithm=EvolutionAlgoritm(
        problem=config.problem, 
        population_size=config.population_size,
        offspring_population_size= config.offspring_population,
        mutation=PolynomialMutation(probability=0.0005 * (factor*i + 1) , distribution_index=40  ),
        selection= BinaryTournamentSelection(),
        crossover=SBXCrossover(probability=0.005 * (factor * i +1)),
        termination_criterion=StoppingByEvaluations(max_evaluations=10000000)))
        Island1.start()
        Agents.append(Agent(Island1, name= f"Agent{i}", attidute= AttiduteType( 2), communication_type=config.commuincationType, trust_type=config.trust_type))

    i = config.noAgents//2

    Island2 = Island(algorithm=EvolutionAlgoritm(
    problem=config.problem, 
    population_size=config.population_size,
    offspring_population_size= config.offspring_population,
    mutation=PolynomialMutation(probability=0.0005 , distribution_index=40),
    selection= BinaryTournamentSelection(),
    crossover=SBXCrossover(probability=0.005),
    termination_criterion=StoppingByEvaluations(max_evaluations=1000000000)))
    Island2.start()
    Agent_Reference = Agent(Island2, name= f"Agent single", attidute= AttiduteType(1), communication_type=config.commuincationType, trust_type=config.trust_type)

    return Agents, Agent_Reference

