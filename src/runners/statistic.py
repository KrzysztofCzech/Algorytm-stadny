
from runners.single import MultiAgentRunner
import numpy as np
from utils.plots import boxplot
from utils.utils import RunData, NumpyArrayEncoder
import json
import logging



    

class StatisticRunner:
    def __init__(self, MultiAgentRunner: MultiAgentRunner):
        self.Executor = MultiAgentRunner
        self.history = RunData()

    def run_an_collect_data(self, no_runs : int,cycles, cycle_iter, num_of_comm):
        for i in range(no_runs):
            self.Executor.initalize()
            self.Executor.run(cycles, cycle_iter, num_of_comm)
            self.history.add_data(*self.Executor.get_results(),2 , len(self.Executor.get_agents()))
            self.save_progres("results")

    def save_progres(self, filename = None):
        data = {}

        for key, val in self.history.__dict__.items():
            data[key] = json.dumps(val, cls=NumpyArrayEncoder)  # use dump() to write array into file
        logging.info("endoced" )
        logging.info(data )


    def plot(self):
        boxplot(self.history.results_multi, self.history.x_coor_multi[0,:], "Multi-Agent System resuts")
        boxplot(self.history.results_single, self.history.x_coor_single[0,:], "Single-Agent System results")
        boxplot(self.history.results_single - self.history.results_multi, self.history.x_coor_single[0,:], "Diffence beetween Single-Agent and Multi-Agent")
        


