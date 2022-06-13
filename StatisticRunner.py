from concurrent.futures import Executor
from dataclasses import dataclass
from msilib.schema import Class
from tracemalloc import Statistic
from typing import List
from Executor import MultiAgentRunner
import numpy as np

@dataclass
class RunData:
    x_coor_multi : List(int)
    results_multi : List(float)
    x_coor_single : List(int)
    results_single : List(float)

class StatisticRunner:
    def __init__(self, MultiAgentRunner: MultiAgentRunner):
        self.Executor = MultiAgentRunner
        self.history = np.array([])

    def run_an_collect_data(self, no_runs : int):
        for i in range(no_runs):
            self.Executor.run()
            data = RunData(self.Executor.get_results())
            np.append(self.history, [data]) 
            self.Executor.initalize()


