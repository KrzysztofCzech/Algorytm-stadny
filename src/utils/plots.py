import matplotlib.pyplot as plt
import os
from typing import List
from agent.agent import Agent
from time import strftime
from agent.island import PopulationsData


def draw_comparision_agents_plot(Agents_list : List[Agent], name :  str):
    for agent in Agents_list:
        plt.plot(range(len(agent.Island.get_history_soultion())), agent.Island.get_history_soultion())
    alg1 = Agents_list[0].Island.algorithm
    plt.legend([agent.name for agent in Agents_list])
    plt.title(f"Problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.xlabel("Number of iterations")
    plt.ylabel("Objective value")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"{name}_{date}).jpg"))
    plt.show()

def draw_comparisson_multi_and_single(x_coord_multi, res_multi, x_coord_single , results_single, name: str):

    plt.plot(x_coord_multi, res_multi)
    plt.plot(x_coord_single, results_single)

    plt.legend(["Socjo", "Single"])
    plt.title(f" Comparison of Multi vs Single")
    plt.xlabel("Number of iterations")
    plt.ylabel("Objective value")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"{name}_{date}.jpg"))
    plt.show()

def boxplot(series, positions, title):
    plt.boxplot(series, positions=positions)
    plt.title(title)
    plt.xlabel("Number of iterations")
    plt.ylabel("Objective value")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"{title}_{date}.jpg"))
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
    plt.yscale('log')
    plt.xlabel("Number of iterations")
    plt.ylabel("Standard deviation of population")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Standard deviation {name}_{date}).jpg"))

    plt.figure(2)
    alg1 = Agents_list[0].Island.algorithm
    plt.legend([agent.name for agent in Agents_list])
    plt.title(f"Spread of population problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.xlabel("Number of iterations")
    plt.ylabel("Spread")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Spread of population {name}_{date}).jpg"))
    plt.show()


def draw_debug_plots_summary(algorithm_data: List[PopulationsData], Agents_list:List[Agent], name :  str):
    solutions_std = []
    solutions_spread = []

    for el in algorithm_data:
        solutions_std.append(el.solution_std)
        solutions_spread.append(el.solution_spread)
    
    plt.figure(1)
    plt.plot(range(len(solutions_std)), solutions_std)
    alg1 = Agents_list[0].Island.algorithm
    plt.title(f"Std of all population problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.yscale('log')
    plt.xlabel("Number of iterations")
    plt.ylabel("Standard deviation of population")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Standard deviation {name}_{date}).jpg"))

    plt.figure(2)
    plt.plot(range(len(solutions_spread)), solutions_spread)
    alg1 = Agents_list[0].Island.algorithm
    plt.title(f"Spread of all population problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.xlabel("Number of iterations")
    plt.ylabel("Spread")
    date = strftime("%Y-%m-%d %H%M%S")
    plt.savefig(os.path.join('../figs', f"Spread of population {name}_{date}).jpg"))
    plt.show()
