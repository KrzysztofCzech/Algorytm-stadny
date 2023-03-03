
from runners.single import MultiAgentRunner
import numpy as np
from utils.plots import boxplot, boxplot_comparison
from utils.utils import RunData, NumpyArrayEncoder
import json
import logging
from jmetal.util.observer import ProgressBarObserver
import os
from time import strftime




    

class StatisticRunner:
    def __init__(self, MultiAgentRunner: MultiAgentRunner):
        self.Executor = MultiAgentRunner
        self.history = RunData()
        self.debug = False

    def set_debug(self, debug: bool):
        self.debug = debug
        self.Executor.set_debug(debug)

    def run_an_collect_data(self, no_runs : int,cycles, cycle_iter, num_of_comm):
        for i in range(no_runs):
            self.Executor.initalize()
            self.Executor.run(cycles, cycle_iter, num_of_comm)
            self.history.add_data(*self.Executor.get_results(),50 , len(self.Executor.get_agents()))
            logging.info(f"Run {i} out of {no_runs}")            

    def save_progres(self, config, num_of_comm, filename = None,):
        data = {}

        for key, val in self.history.__dict__.items():
            data[key] = json.dumps(val, cls=NumpyArrayEncoder)  # use dump() to write array into file
        logging.info("endoced" )
        logging.info(data )
        folder_name = strftime("%Y-%m-%d %H%M%S")
        path_to_folder = os.path.join("..","figs",folder_name)
        os.mkdir(path_to_folder)

        with open (os.path.join(path_to_folder,"results.json"), "w") as f:
            f.write(json.dumps(data))
        config_dict = {}
        config_dict["noAgents"] = config.noAgents
        config_dict["num_of_communication"] =  num_of_comm
        config_dict["problem_size"] = config.problem.number_of_variables
        config_dict["problem"] = config.problem.get_name()
        
        with open (os.path.join(path_to_folder,"config.json"), "w") as f:
            f.write(json.dumps(config_dict))




    def plot(self):
        boxplot(self.history.results_multi, self.history.x_coor_multi[0,:], "Multi-Agent System resuts")
        boxplot(self.history.results_single, self.history.x_coor_single[0,:], "Single-Agent System results")
        boxplot(self.history.results_single - self.history.results_multi, self.history.x_coor_single[0,:], "Diffence beetween Single-Agent and Multi-Agent")
        boxplot_comparison(self.history.results_multi, self.history.x_coor_multi[0,:],  self.history.results_single, self.history.x_coor_single[0,:], "Diffence beetween Single-Agent and Multi-Agent")
        


