import re
from typing import List

from runners.single import MultiAgentRunner
import numpy as np
from utils.utils import list_to_dict
from utils.plots import boxplot, boxplot_comparison
from utils.utils import RunData, NumpyArrayEncoder
import json
import logging
import os
from time import strftime
from agent.agent import Agent
import time


class StatisticRunner:
    def __init__(self):
        self.single_comparison: MultiAgentRunner = None
        self.Executors: List[MultiAgentRunner] = []
        self.debug = False
        self.communication_number = 1
        self.all_iterations = 1
        self.communication_frequency = 50
        self.no_runs = 3
        self.island_comparison: MultiAgentRunner = None

    def add_Executor(self, Executor: MultiAgentRunner):
        self.Executors.append(Executor)

    def set_single_agent(self, runner: MultiAgentRunner):
        self.single_comparison = runner

    def set_island_comparion(self, runner: MultiAgentRunner):
        self.island_comparison = runner

    def set_debug(self, debug: bool):
        self.debug = debug
        for Executor in self.Executors:
            Executor.set_debug(debug)
  
    def run_an_collect_data(self):
        if self.single_comparison is not None:
            for i in range(self.no_runs):
                time1 = time.time()
                cycles = int(self.all_iterations / self.communication_frequency / len(self.single_comparison.get_agents()))
                self.single_comparison.initialize()
                self.single_comparison.run(cycles, self.communication_frequency, 0)
                logging.info(f"Single comparison finished in {(time.time() - time1) / 60}")
                self.single_comparison.add_history_data(*self.single_comparison.get_results(), 1)

        if self.island_comparison is not None:
            for i in range(self.no_runs):
                self.run_island_comparison()

        for Executor in self.Executors:
            Executor.set_observer(self.all_iterations)
            cycles = int(self.all_iterations / self.communication_frequency / len(Executor.get_agents()))
            for i in range(self.no_runs):
                time1 = time.time()
                Executor.initialize()
                Executor.run(cycles, self.communication_frequency, self.communication_number)
                Executor.add_history_data(*Executor.get_results(), len(Executor.get_agents()))
                logging.info(f"Run {i} out of {self.no_runs}")
                logging.info(f"Socjo comparison finished in {(time.time() - time1) / 60}")
                self.plot_comparison(Executor)
    
    def save_data(self, executor: MultiAgentRunner, path_to_results, save_config = False):
        data = {}
        for key, val in executor.get_history().__dict__.items():
            data[key] = json.dumps(val, cls=NumpyArrayEncoder)  # use dump() to write array into file
        name = re.sub(r'[\W_]', "", executor.name)
        path_to_folder = os.path.join(path_to_results, name )
        os.mkdir(path_to_folder)
        with open(os.path.join(path_to_folder, "results.json"), "w") as f:
            f.write(json.dumps(data))

        if save_config:
            config = executor.config
            config_dict = {"noAgents":   config.noAgents, "num_of_communication": self.communication_number,
                        "problem_size": config.problem.number_of_variables, "problem": config.problem.get_name(), 
                        "trust_start": config.start_trust, "trust_type": str(config.trust_type),
                        "communication_type": str(config.communicationType), "communication_frequency": self.communication_frequency, 
                        "oparator": config.communicationType.operator.__name__, "intensity": config.communicationType.mutation_type.__name__, "modify_agents": executor.modify_agent_during_run,
                        "modify_agent_function" : executor.modify_agent_metod_name}

            with open(os.path.join(path_to_folder, "config.json"), "w") as f:
                f.write(json.dumps(config_dict))

    def save_progres(self):
        folder_name = strftime("%Y-%m-%d %H%M%S")
        path_to_results = os.path.join("..", "figs", folder_name)
        os.mkdir(path_to_results)
        for executor in self.Executors:
            self.save_data(executor, path_to_results, True)

        self.save_data(self.single_comparison, path_to_results)
        self.save_data(self.island_comparison, path_to_results)


    def plot_comparison(self,executor: MultiAgentRunner):
        executor.plot_results(self.communication_frequency, *self.single_comparison.get_results(),
                                "Single comparison", executor.name)
        executor.plot_results(self.communication_frequency, *self.island_comparison.get_results(),
                                "Island comparison", executor.name)

    def run_island_comparison(self):
        time1 = time.time()
        cycles = int(self.all_iterations / self.communication_frequency / len(self.island_comparison.get_agents()))
        self.island_comparison.initialize()
        self.island_comparison.run(cycles, self.communication_frequency, self.communication_number)
        logging.info(f"Island comparison finished in {(time.time() - time1) / 60}")
        self.island_comparison.add_history_data(*self.island_comparison.get_results(), len(self.island_comparison.get_agents()))
 