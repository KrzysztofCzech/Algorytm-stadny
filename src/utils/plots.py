import matplotlib.pyplot as plt
import os
from typing import List
from agent.agent import Agent
from time import strftime
from agent.island import PopulationsData
import numpy as np


def draw_comparision_agents_plot(Agents_list : List[Agent], name :  str):
    for agent in Agents_list:
        plt.plot(range(len(agent.Island.get_history_soultion())), agent.Island.get_history_soultion())
    alg1 = Agents_list[0].Island.algorithm
    plt.legend([agent.name for agent in Agents_list])
    plt.title(f"Problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.xlabel("Number of iterations")
    plt.ylabel("Objective value")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"{name}_{date}).png"))
    plt.show()

def draw_comparisson_multi_and_single(x_coord_multi, res_multi, x_coord_single , results_single, name: str):

    plt.plot(x_coord_multi, res_multi)
    plt.plot(x_coord_single, results_single)

    plt.legend(["Socjo", "Single"])
    plt.title(f" Comparison of Multi vs Single")
    plt.xlabel("Number of iterations")
    plt.ylabel("Objective value")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"{name}_{date}.png"))
    plt.show()

def boxplot(series, positions, title):
    plt.boxplot(series, positions=positions)
    plt.title(title)
    plt.xlabel("Number of iterations")
    plt.ylabel("Objective value")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"{title}_{date}.png"))
    plt.show()

def draw_debug_plots_agents(Agents_list : List[Agent], name :  str):
    plt.figure(1)
    plt.figure(2)
    for agent in Agents_list:
        agent_solutions_std = []
        agent_solutions_spread = []
        popultaion_history = agent.get_island_history()
        for el in popultaion_history:
            agent_solutions_std.append(el.solution_std)
            agent_solutions_spread.append(el.solution_spread)
        
        plt.figure(1)
        plt.plot(range(len(agent_solutions_std)), agent_solutions_std)
        plt.figure(2)
        plt.plot(range(len(agent_solutions_spread)), agent_solutions_spread)

    plt.figure(1)
    alg1 = Agents_list[0].Island.algorithm
    plt.legend([agent.name for agent in Agents_list])
    plt.title(f"Std of population problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.xlabel("Number of iterations")
    plt.ylabel("Standard deviation of population")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Standard deviation {name}_{date}).png"))

    plt.figure(2)
    alg1 = Agents_list[0].Island.algorithm
    plt.legend([agent.name for agent in Agents_list])
    plt.title(f"Spread of population problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.xlabel("Number of iterations")
    plt.ylabel("Spread")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Spread of population {name}_{date}).png"))
    plt.show()


def draw_debug_plots_summary(algorithm_data: List[PopulationsData], Agents_list:List[Agent], name :  str, cycle_iter:int):
    solutions_std = []
    solutions_spread = []

    for el in algorithm_data:
        solutions_std.append(el.solution_std)
        solutions_spread.append(el.solution_spread)
    
    plt.figure(1)
    plt.plot([i*cycle_iter for i in range(len(solutions_std))], solutions_std)
    alg1 = Agents_list[0].Island.algorithm
    plt.title(f"Std of all population problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.xlabel("Number of iterations")
    plt.ylabel("Standard deviation of population")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Standard deviation {name}_{date}).png"))

    plt.figure(2)
    plt.plot([i*cycle_iter for i in range(len(solutions_spread))], solutions_spread)
    alg1 = Agents_list[0].Island.algorithm
    plt.title(f"Spread of all population problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.xlabel("Number of iterations")
    plt.ylabel("Spread")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Spread of population {name}_{date}).png"))
    plt.show()


def draw_histogram_of_communication(communication_hisotry : List[PopulationsData]):
    solutions_std = []
    solutions_spread = []

    for popultaion in communication_hisotry:
        solutions_spread.append(popultaion.solution_spread)
        solutions_std.append(popultaion.solution_std)

    solutions_spread = np.array(solutions_spread)
    solutions_std = np.array(solutions_std)
    plt.hist(solutions_std, bins=200)  
    plt.ylabel('Probability')
    plt.xlabel('Std of 2 polutions duting algotithm')
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Std of 2 polutions duting algotithm {date}.png"))
    plt.show()

    plt.hist(solutions_spread, bins=200)  
    plt.ylabel('Probability')
    plt.xlabel('Spread of 2 polutions duting algotithm')
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Spread of 2 polutions duting algotithm {date}.png"))
    plt.show()