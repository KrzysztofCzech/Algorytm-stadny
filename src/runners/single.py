
import random
from agent.agent import Agent
from typing import List
from utils.plots import draw_comparision_agents_plot, draw_comparisson_multi_and_single, draw_debug_plots_agents, draw_debug_plots_summary, draw_histogram_of_communication
from agent.island import PopulationsData
import numpy as np
from jmetal.util.observer import ProgressBarObserver
import logging
import time 

def calc_spread_and_std(all_solutions):
    spread = max(max([[sol.objectives[0] for sol in sol_row] for sol_row in all_solutions])) -  min(min([[sol.objectives[0] for sol in sol_row] for sol_row in all_solutions]))
    solution_array  = np.array([[sol.variables for sol in sol_row] for sol_row in all_solutions])
    std = np.mean(np.std(solution_array, axis=0))
    means_sol = np.mean(solution_array, axis=0)
    return spread, std, means_sol

class MultiAgentRunner:

    def __init__(
        self,
        agents: List[Agent],
        agent_single: Agent,
        max_iterations: int
    ):
        self.__agents = agents
        self._agent_single = agent_single
        self.algorithm_data = []
        self.comunication_history = []
        self.observer_multi = ProgressBarObserver(max=max_iterations)
        self.observer_single = ProgressBarObserver(max=max_iterations)

    def get_agents(self):
        return self.__agents

    def initalize(self):
        
        for agent in self.__agents:
            agent.initalize(self.observer_multi)
        self._agent_single.initalize(self.observer_single)

    
    def add_Agent(self, agent: Agent) -> None:
        self.__agents.append(agent)

    def run_cycle(self, cycle_iterations : int) -> None:
        for agent in self.__agents:
            agent.run(cycle_iterations)

    def communicate(self, number_of_communications):
        for agent in self.__agents:
            for agent2 in random.sample(self.__agents, number_of_communications):
                if agent == agent2:
                    continue
                soultions = [agent.Island.algorithm.solutions, agent2.Island.algorithm.solutions]
                spread, std, means_sol = calc_spread_and_std(soultions)
                
                res = agent.communicate(agent2)
                population = PopulationsData(solution_spread= spread, solution_std=std, solution_mean=means_sol, result= res)
                self.comunication_history.append(population)      




    def run(self, cycles : int, cycle_iter: int, num_of_comm:int):
        logging.info("Socjo started")
        time1 = time.time()
        for i in range(cycles):
            for j in range(cycle_iter):
                self.run_cycle(1)
                self.collect_data()

            self.communicate(num_of_comm)
            self.collect_data()


        logging.info(f"Socjo finished in {(time.time() - time1)/60}")
        time1 = time.time()
        self.run_comparison()
        logging.info(f"comparison finished in {(time.time() - time1)/60}")
        time1 = time.time()
        self.plot_results(1)
        logging.info(f"plotting finished in {(time.time() - time1)/60}")
        

        
    def plot_results(self, cycle_iter):
        problem = self.__agents[0].Island.algorithm.problem
        describe_string = f"{problem.get_name()} {problem.number_of_variables} variables no agents {len(self.__agents)}"
        x_coord_multi, results_multi, x_coord_single , results_single = self.get_results()
        logging.info(f"best socjo {results_multi[-1]} best single {results_single[-1]}")
        draw_comparision_agents_plot(self.__agents, name = f"Agent comaprison Problem" + describe_string)
        draw_debug_plots_agents(self.__agents, name = describe_string)
        draw_debug_plots_summary(self.algorithm_data,self.__agents, name = describe_string, cycle_iter = cycle_iter)
        draw_comparisson_multi_and_single(x_coord_multi, results_multi, x_coord_single , results_single, name = f"Single agent and multi agent system comparison" + describe_string)
        draw_histogram_of_communication(self.comunication_history)

    def run_comparison(self):
        all_iterations = sum([agent.get_num_of_iteration() for agent in self.__agents])
        self._agent_single.run(all_iterations)

    def get_results(self):
        res_multi = self.__agents[0].Island.get_history_soultion()
        x_coord_multi = list(range(1, len(res_multi)+1))

        #get best solution for iteration from agents over time assuming equal number of iterations
        for agent in self.__agents[1:]:
            temp = agent.Island.get_history_soultion()
        
            for i in range(len(temp)):
                res_multi[i] = min(res_multi[i], temp[i])
                x_coord_multi[i] += i
        return x_coord_multi, res_multi, list(range(len(self._agent_single.Island.get_history_soultion()))), self._agent_single.Island.get_history_soultion()

    def collect_data(self):
        all_islands = [agent.Island for agent in self.__agents]
        all_solutions = [island.algorithm.solutions for island  in all_islands]

        spread, std, means_sol = calc_spread_and_std(all_solutions)
        population = PopulationsData(solution_spread= spread, solution_std=std, solution_mean=means_sol)
        self.algorithm_data.append(population)      

        
        