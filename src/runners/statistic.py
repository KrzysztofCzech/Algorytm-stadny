
from runners.single import MultiAgentRunner
import numpy as np
from utils.plots import boxplot, boxplot_comparison
from utils.utils import RunData, NumpyArrayEncoder
import json
import logging
import os
from time import strftime
from agent.agent import Agent
import time



    

class StatisticRunner:
    def __init__(self, MultiAgentRunner: MultiAgentRunner):
        self.Executors = [MultiAgentRunner]
        self.history = [RunData()]
        self.debug = False
        self.communication_number = 1
        self.all_iterations = 1 
        self.communication_frequency = 50
        self.no_runs = 3
        self.single_comparison = None
        self.island_comparison =None
    
    def add_Executor(self, Executor: MultiAgentRunner):
        self.Executors.extend(Executor)

    def set_single_agent(self, agent :Agent):
        self.single_comparison = agent

    def set_single_agent(self, runner :MultiAgentRunner):
        self.island_comparison = runner        

    def set_debug(self, debug: bool):
        self.debug = debug
        for Executor in self.Executors:
            Executor.set_debug(debug)

    def run_an_collect_data(self):
        for idx, Executor in enumerate(self.Executors):
            Executor.set_observer(self.all_iterations)
            cycles=int(self.all_iterations/self.communication_frequency/len(Executor.get_agents()))
            for i in range(self.no_runs):
                Executor.initalize()
                Executor.run(cycles, self.communication_frequency, self.communication_number)
                self.history[idx].add_data(*Executor.get_results(),1000 , len(Executor.get_agents()))
                logging.info(f"Run {i} out of {self.no_runs}")           

        if self.single_comparison is not None:
            time1 = time.time()
            self.single_comparison.run(self.all_iterations)
            logging.info(f"Single comparison finished in {(time.time() - time1)/60}")

        if self.island_comparison is not None:
            self.run_island_comparison()


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
        


    def run_island_comparison(self):
        time1 = time.time()
        cycles=int(self.all_iterations/self.communication_frequency/len(self.island_comparison.get_agents()))
        self.island_comparison.run(cycles, self.communication_frequency, self.communication_number)
        logging.info(f"Island comparison finished in {(time.time() - time1)/60}")
