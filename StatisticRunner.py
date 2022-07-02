from typing import List
from Executor import MultiAgentRunner
import numpy as np
from plots import boxplot
from typing import List

class RunData:
    def __init__(self):
        self.x_coor_multi = np.array([])
        self.results_multi = np.array([])
        self.x_coor_single = np.array([])
        self.results_single = np.array([])

    def add_data(self, x_coor_multi, results_multi, x_coor_single, results_single, sampling_iter, no_agents):
        if self.x_coor_multi.any():
            self.x_coor_multi = np.vstack((self.x_coor_multi, np.array(list(x_coor_multi)[::sampling_iter])))
            self.results_multi = np.vstack((self.results_multi, np.array(results_multi[::sampling_iter])))
            self.x_coor_single = np.vstack((self.x_coor_single, np.array(x_coor_single[::sampling_iter*no_agents])))
            self.results_single = np.vstack((self.results_single, np.array(results_single[::sampling_iter* no_agents])))
        else:
            self.x_coor_multi = np.array(x_coor_multi[::sampling_iter])
            self.results_multi = np.array(results_multi[::sampling_iter])
            self.x_coor_single = np.array(x_coor_single[::sampling_iter*no_agents])
            self.results_single = np.array(results_single[::sampling_iter* no_agents])



    

class StatisticRunner:
    def __init__(self, MultiAgentRunner: MultiAgentRunner):
        self.Executor = MultiAgentRunner
        self.history = RunData()

    def run_an_collect_data(self, no_runs : int,cycles, cycle_iter, num_of_comm):
        for i in range(no_runs):
            self.Executor.initalize()
            self.Executor.run(cycles, cycle_iter, num_of_comm)
            self.history.add_data(*self.Executor.get_results(),int((cycles * cycle_iter)/100), len(self.Executor.get_agents()))


    
    def plot(self):
        boxplot(self.history.results_multi, self.history.x_coor_multi[0,:], "Statistic results multi")
        boxplot(self.history.results_single, self.history.x_coor_single[0,:], "Statistic results single")
        


