from typing import List
from statistics import mean
from jmetal.core.solution import Solution
import os
import numpy as np
from json import JSONEncoder

from agent.island import PopulationsData


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def prepare_array(array, sampling):
    return np.array(array[::sampling] + [array[-1]])


class RunData:
    def __init__(self):
        self.x_ticks = np.array([])
        self.results = np.array([])

    def add_data(self, x_coor_multi, results_multi, sampling):
        if self.x_ticks.any():
            self.x_ticks = np.vstack((self.x_ticks, prepare_array(x_coor_multi, sampling)))
            self.results = np.vstack((self.results, prepare_array(results_multi, sampling)))

        else:
            self.x_ticks = prepare_array(x_coor_multi, sampling)
            self.results = prepare_array(results_multi, sampling)


def mean_of_solutions(solutions: List[Solution]):
    return mean([solution.objectives[0] for solution in solutions])


def create_folder(path):
    try:
        os.mkdir(path)
        return True
    except FileExistsError:
        return True
    except Exception:
        return False


def save_history(history: RunData, name: str):
    if create_folder("data"):
        path = os.join("data", name)
        if create_folder(os.join("data", name)):
            save_np_arr(history.results, os.join(path, "results_multi"))
            save_np_arr(history.results_single, os.join(path, "results_single"))
            save_np_arr(history.x_coor_single, os.join(path, "x_coor_single"))
            save_np_arr(history.x_ticks, os.join(path, "x_coor_multi"))


def save_np_arr(array: np.array, path: str):
    np.save(array, path)

def list_to_dict(population_list : List[PopulationsData]):
    population1 = population_list[0]
    data = population1.__dict__
    for key in data.keys():
        data[key] = []

    for population in population_list:
        temp = population.__dict__
        for key in data.keys():
            data[key].extend(temp[key])

    for key, val in data.items():
        data[key] = np.array(val)

    return data