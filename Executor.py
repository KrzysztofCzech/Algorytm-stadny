from dataclasses import dataclass
from itertools import cycle

from random import randint
from Agent import Agent
from typing import List, Optional
from plots import draw_comparision_agents_plot, draw_comparisson_multi_and_single

class MultiAgentRunner:

    def __init__(
        self,
        agents: List[Agent],
        agent_single: Agent
    ):
        self.__agents = agents
        self._agent_single = agent_single
    
    def add_Agent(self, agent: Agent) -> None:
        self.__agents.append(agent)

    def run_cycle(self, cycle_iterations : int) -> None:
        for agent in self.__agents:
            agent.run(cycle_iterations)

    def communicate(self, number_of_communications):
        for agent in self.__agents:
            for i in range(number_of_communications):
                agent.communicate(self.__agents[randint(0,len(self.__agents)-1)])


    def run(self, cycles : int, num_of_comm : int, cycle_iter: int):
        for i in range(cycles):
            print(f"cycle {i}")
            self.run_cycle(cycle_iter)
            self.communicate(num_of_comm)
        
        print("Running comparison")
        self.run_comparison()

        self.plot_results()
        
    def plot_results(self):
        draw_comparision_agents_plot(self.__agents, name = "Wykres porównania działania agentów")
        draw_comparisson_multi_and_single(self.__agents, self._agent_single, name = "Socjo Multi Comparison")


    def run_comparison(self):
        all_iterations = sum([agent.get_num_of_iteration() for agent in self.__agents])
        self._agent_single.run(all_iterations)
        

        
        