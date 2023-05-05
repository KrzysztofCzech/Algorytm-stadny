import random
from agent.agent import Agent
from typing import List
from settings.settings import AgentConfigData
from utils.plots import draw_comparison_agents_plot, draw_comparison_multi_and_single, draw_debug_plots_agents, \
    draw_debug_plots_summary, draw_histogram_of_communication
from agent.island import PopulationsData
import numpy as np
from agent.observer import ProgressBarCycleObserver
import logging
import time

from utils.utils import RunData


def calc_spread_and_std(all_solutions):
    spread = max(max([[sol.objectives[0] for sol in sol_row] for sol_row in all_solutions])) - min(
        min([[sol.objectives[0] for sol in sol_row] for sol_row in all_solutions]))
    solution_array = np.array([[sol.variables for sol in sol_row] for sol_row in all_solutions])
    std = np.mean(np.std(solution_array, axis=0))
    means_sol = np.mean(solution_array, axis=0)
    return spread, std, means_sol


class MultiAgentRunner:

    def __init__(
            self,
            agents: List[Agent],
            name:str,
    ):
        self.modify_agent_method = None
        self.__agents = agents
        self.algorithm_data = []
        self.communication_history = []
        self.debug = False
        self.modify_agent_during_run = False
        self._deleted_agents = []
        self.observer_multi = ProgressBarCycleObserver(max=1)
        self.observer_single = ProgressBarCycleObserver(max=1)
        self.history: RunData = RunData()
        self.config: AgentConfigData = None
        self.name: str = name

    def get_agents(self):
        return self.__agents

    def set_agent_modification(self, enable, method):
        self.modify_agent_during_run = enable
        self.modify_agent_method = method

    def set_debug(self, debug: bool):
        self.debug = debug

    def initialize(self):
        for agent in self.__agents:
            agent.initialize(self.observer_multi)

    def add_Agent(self, agent: Agent) -> None:
        self.__agents.append(agent)

    def run_cycle(self, cycle_iterations: int) -> None:
        for agent in self.__agents:
            agent.run(cycle_iterations)

    def add_history_data(self, x_coor_multi, results_multi, sampling):
        self.history.add_data(x_coor_multi, results_multi, sampling)

    def set_config(self, config):
        self.config = config

    def get_history(self):
        return self.history

    def communicate(self, number_of_communications):
        for agent in self.__agents:
            for agent2 in random.sample(self.__agents, number_of_communications):
                if agent == agent2:
                    continue
                solutions = [agent.Island.algorithm.solutions, agent2.Island.algorithm.solutions]
                spread, std, means_sol = calc_spread_and_std(solutions)

                res = agent.communicate(agent2)
                population = PopulationsData(solution_spread=spread, solution_std=std, solution_mean=means_sol,
                                             result=res)
                self.communication_history.append(population)
                if self.modify_agent_during_run and std < 0.3 and res == False and spread < 10:
                    deleted = self.modify_agent_method(agent2, agent)
                    if deleted:
                        self._deleted_agents.extend(agent2)
                        self.__agents.remove(agent2)
                    break

    def set_observer(self, iterations):
        self.observer_multi = ProgressBarCycleObserver(max=iterations)
        self.observer_single = ProgressBarCycleObserver(max=iterations)

    def run(self, cycles: int, cycle_iter: int, num_of_comm: int, run_comparison=True, plot_all=True):

        for i in range(cycles):
            self.run_cycle(cycle_iter)
            self.collect_data()
            self.communicate(num_of_comm)
            self.collect_data()

        time1 = time.time()

    def plot_results(self, cycle_iter, x_ticks_compparison, results_compparison, comparison_type, executor_name):
        problem = self.__agents[0].Island.algorithm.problem
        describe_string = f"{problem.get_name()}, {problem.number_of_variables} variables,"
        x_coord_multi, results_multi = self.get_results()
        draw_comparison_agents_plot(self.__agents, name=f"{describe_string} agents comparison " )
        draw_comparison_multi_and_single(x_coord_multi, results_multi, x_ticks_compparison, results_compparison,
                                         describe_string + " algorithm comparison", comparison_type, executor_name)
        #draw_debug_plots_agents(self.__agents, name=describe_string)
        #draw_debug_plots_summary(self.algorithm_data, self.__agents, name=describe_string, cycle_iter=cycle_iter)
        draw_histogram_of_communication(self.communication_history)

    def get_results(self):
        results = self.__agents[0].Island.get_history_solution()
        x_ticks = list(range(1, len(results) + 1))

        # get the best solution for iteration from agents over time assuming equal number of iterations
        for agent in self.__agents[1:]:
            temp = agent.Island.get_history_solution()

            for i in range(len(temp)):
                results[i] = min(results[i], temp[i])
                x_ticks[i] += i
        return x_ticks, results

    def collect_data(self):
        all_islands = [agent.Island for agent in self.__agents]
        all_solutions = [island.algorithm.solutions for island in all_islands]

        spread, std, means_sol = calc_spread_and_std(all_solutions)
        population = PopulationsData(solution_spread=spread, solution_std=std, solution_mean=means_sol)
        self.algorithm_data.append(population)
