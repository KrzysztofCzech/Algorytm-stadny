from typing import List
from statistics import mean
from jmetal.core.solution import Solution
import os
import numpy as np

def prepare_array(array, sampling):
    return [array[0]]+ array[::sampling] 
class RunData:
    def __init__(self):
        self.x_coor_multi = np.array([])
        self.results_multi = np.array([])
        self.x_coor_single = np.array([])
        self.results_single = np.array([])

    def add_data(self, x_coor_multi, results_multi, x_coor_single, results_single, sampling_iter, no_agents):
        if self.x_coor_multi.any():
            self.x_coor_multi = np.vstack((self.x_coor_multi, np.array(prepare_array(x_coor_multi, sampling_iter))))
            self.results_multi = np.vstack((self.results_multi, np.array(prepare_array(results_multi, sampling_iter))))
            self.x_coor_single = np.vstack((self.x_coor_single, np.array(prepare_array(x_coor_single, sampling_iter * no_agents))))
            self.results_single = np.vstack((self.results_single, np.array(prepare_array(results_single, sampling_iter * no_agents))))
        else:
            self.x_coor_multi = np.array(prepare_array(x_coor_multi, sampling_iter))
            self.results_multi = np.array(prepare_array(results_multi, sampling_iter))
            self.x_coor_single = np.array(prepare_array(x_coor_single, sampling_iter * no_agents))
            self.results_single = np.array(prepare_array(results_single, sampling_iter * no_agents))

def mean_of_solutions(solutions : List[Solution]):
    return mean([solution.objectives[0] for solution in solutions])

def create_folder(path):
    try: 
        os.mkdir(path)
        return True
    except FileExistsError: 
        return True
    except Exception as e:
        return False


    

def save_hisory(history : RunData, name : str):
    if(create_folder("data")):
        path =  os.join("data", name)
        if(create_folder(os.join("data", name))):
            save_np_arr(history.results_multi, os.join(path, "results_multi"))
            save_np_arr(history.results_single, os.join(path, "results_single"))
            save_np_arr(history.x_coor_single, os.join(path, "x_coor_single"))
            save_np_arr(history.x_coor_multi, os.join(path, "x_coor_multi"))

def save_np_arr(array : np.array, path: str):
    np.save(np.array, path)

