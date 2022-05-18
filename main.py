from jmetal.algorithm.singleobjective.evolution_strategy import EvolutionStrategy
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.problem.singleobjective.unconstrained import Rastrigin
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from Island import Island
from random import randint
from Agent import Agent

import matplotlib.pyplot as plt
import time
import os


def draw_comparision_plot(Isl_list):
    for Isl in Isl_list:
        plt.plot(range(len(Isl.get_history_soultion())), Isl.get_history_soultion())
    alg1 = Isl_list[0].algorithm
    plt.legend([Isl.algorithm.get_name() for Isl in Isl_list])
    plt.title(f"Problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.savefig(os.path.join('figs', f"{alg1.problem.get_name()}_{alg1.get_name()}_{alg1.get_name()}_history_{time.time()}.jpg"))
    plt.show()

problem = Rastrigin(number_of_variables = 100)


algorithm = EvolutionStrategy(
    problem=problem, 
    mu=30,
    lambda_= 100,
    elitist = True,
    mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
    termination_criterion=StoppingByEvaluations(max_evaluations=100000)
)

Agents = []
for i in range(0,10):
    Island1 = Island(algorithm=EvolutionStrategy(
    problem=problem, 
    mu=30 + i,
    lambda_= 100 - i,
    elitist = True,
    mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
    termination_criterion=StoppingByEvaluations(max_evaluations=100000)))
    Island1.start(i*20+ 2332)
    Agents.append(Agent(Island1))
    

for agent in Agents:
    agent.run(500)

for idx, agent in enumerate(Agents):
    agent.Island.algorithm.solutions = agent.Island.algorithm.replacement(agent.Island.algorithm.solutions, Agents[(idx+3)%len(Agents)].migrate(5)) 


for agent in Agents:
    agent.run(500)


front = Island1.algorithm.get_result()

draw_comparision_plot([agent.Island for agent in Agents])
