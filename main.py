from Evolutionary_algorithm import EvolutionAlgoritm
from jmetal.operator import SBXCrossover, PolynomialMutation, BinaryTournamentSelection
from jmetal.problem.singleobjective.unconstrained import Rastrigin
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from Island import Island
from random import randint
from Agent import Agent
from typing import List
import matplotlib.pyplot as plt
import time
import os


def draw_comparision_plot(Agents_list):
    for agent in Agents_list:
        plt.plot(range(len(agent.Island.get_history_soultion())), agent.Island.get_history_soultion())
    alg1 = Agents_list[0].Island.algorithm
    plt.legend([agent.Island.algorithm.get_name() for agent in Agents_list])
    plt.title(f"Problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.savefig(os.path.join('figs', f"{alg1.problem.get_name()}_{alg1.get_name()}_{alg1.get_name()}_history_{time.time()}.jpg"))
    plt.show()

if __name__ == "__main__":


    problem = Rastrigin(number_of_variables = 150)


    Agents =  []
    for i in range(0,9):
        Island1 = Island(algorithm=EvolutionAlgoritm(
        problem=problem, 
        population_size=30 -2*i,
        offspring_population_size= 100 -3*i,
        mutation=PolynomialMutation(probability=0.5 + 0.01*i / problem.number_of_variables, distribution_index=20 -i),
        crossover= SBXCrossover(probability=0.01 * i + 0.01),
        selection= BinaryTournamentSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=100000)))
        Island1.start(i*20+ 2332)
        Agents.append(Agent(Island1))
        
    print('Iterations')

    for agent in Agents:
        agent.run(1000)

    print('Communications')

    for idx, agent in enumerate(Agents):
        agent.communicate(Agents[randint(0,len(Agents)-1)])

    print('Iterations')
    for agent in Agents:
        agent.run(500)

    print('Communications')
    
    for idx, agent in enumerate(Agents):
        agent.communicate(Agents[randint(0,len(Agents)-1)])

    print('Iterations')
    for agent in Agents:
        agent.run(500)


    front = Island1.algorithm.get_result()

    draw_comparision_plot(Agents[3:9])
