import matplotlib.pyplot as plt
import os
from typing import List
from agent.agent import Agent
from time import strftime


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


