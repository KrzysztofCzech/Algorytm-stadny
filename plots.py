from ast import Str
import matplotlib.pyplot as plt
import os
from typing import List
from Agent import Agent



def draw_comparision_agents_plot(Agents_list : List[Agent], name :  Str):
    for agent in Agents_list:
        plt.plot(range(len(agent.Island.get_history_soultion())), agent.Island.get_history_soultion())
    alg1 = Agents_list[0].Island.algorithm
    plt.legend([agent.name for agent in Agents_list])
    plt.title(f"Problem {alg1.problem.get_name()} with {alg1.problem.number_of_variables} variables")
    plt.savefig(os.path.join('figs', f"{name}.jpg"))
    plt.show()

def draw_comparisson_multi_and_single(x_coord_multi, res_multi, x_coord_single , results_single, name: Str):

    plt.plot(x_coord_multi, res_multi)
    plt.plot(x_coord_single, results_single)

    plt.legend(["Socjo", "Single"])
    plt.title(f" Comparison of Multi vs Single")
    plt.savefig(os.path.join('figs', f"{name}.jpg"))
    plt.show()

def boxplot(series, positions, title):
    plt.boxplot(series, positions=positions)
    plt.title(title)
    plt.xticks(positions[::2])
    plt.savefig(os.path.join('figs', f"{title}.jpg"))
    plt.show()


