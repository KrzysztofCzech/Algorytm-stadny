
import random
from agent.agent import Agent
from typing import List
from utils.plots import draw_comparision_agents_plot, draw_comparisson_multi_and_single
import logging


class MultiAgentRunner:

    def __init__(
        self,
        agents: List[Agent],
        agent_single: Agent
    ):
        self.__agents = agents
        self._agent_single = agent_single

    def get_agents(self):
        return self.__agents

    def initalize(self):
        for agent in self.__agents:
            agent.initalize()
        self._agent_single.initalize()

    
    def add_Agent(self, agent: Agent) -> None:
        self.__agents.append(agent)

    def run_cycle(self, cycle_iterations : int) -> None:
        for agent in self.__agents:
            agent.run(cycle_iterations)

    def communicate(self, number_of_communications):
        for agent in self.__agents:
            for agent2 in random.sample(self.__agents, number_of_communications):
                agent.communicate(agent2)


    def run(self, cycles : int, cycle_iter: int, num_of_comm:int):
        for i in range(cycles):
            self.run_cycle(cycle_iter)
            self.communicate(num_of_comm)

        self.run_comparison()
        self.plot_results()
        
    def plot_results(self):
        problem = self.__agents[0].Island.algorithm.problem
        x_coord_multi, results_multi, x_coord_single , results_single = self.get_results()
        draw_comparision_agents_plot(self.__agents, name = "Agent comaprison in multi-agent system ")
        draw_comparisson_multi_and_single(x_coord_multi, results_multi, x_coord_single , results_single, name = f"Single agent and multi agent system comparison {problem.get_name()} {problem.number_of_variables} variables")


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
        

        
        