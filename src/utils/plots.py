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

    def historgram_from_data(data, bins, xlabel, ylabel, title):
        plt.hist(data, bins=bins)  
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        date = strftime("%Y-%m-%d %H%M%S")
        plt.title(title)
        plt.savefig(os.path.join('../figs', f"{title} {date}.png"))
        plt.show()
    solutions_std = []
    solutions_spread = []
    solutions_std_true = []
    solutions_spread_true = []
    solutions_std_false = []
    solutions_spread_false = []

    for popultaion in communication_hisotry:
        solutions_spread.append(popultaion.solution_spread)
        solutions_std.append(popultaion.solution_std)

        if popultaion.result == True:

            solutions_spread_true.append(popultaion.solution_spread)
            solutions_std_true.append(popultaion.solution_std)

        else:
            solutions_spread_false.append(popultaion.solution_spread)
            solutions_std_false.append(popultaion.solution_std)



    solutions_spread = np.array(solutions_spread)
    solutions_std = np.array(solutions_std)

    historgram_from_data(solutions_std, 200, 'Std of 2 populations duting algotithm', 'Amount of communication', 'Std of 2 populations duting algotithm')
    historgram_from_data(solutions_spread, 200, 'Spread of 2 populations duting algotithm', 'Amount of communication', 'Spread of 2 populations duting algotithm')

    solutions_spread_true = np.array(solutions_spread_true)
    solutions_std_true = np.array(solutions_std_true)

    historgram_from_data(solutions_std_true, 200, 'Std of 2 populations duting algotithm', 'Amount of communication', 'Positive communication')
    historgram_from_data(solutions_spread_true, 200, 'Spread of 2 populations duting algotithm', 'Amount of communication', 'Positive communication')

    solutions_spread_false = np.array(solutions_spread_false)
    solutions_std_false = np.array(solutions_std_false)

    historgram_from_data(solutions_std_false, 200, 'Std of 2 populations duting algotithm', 'Amount of communication', 'Negative communication')
    historgram_from_data(solutions_spread_false, 200, 'Spread of 2 populations duting algotithm', 'Amount of communication', 'Negative communication')


