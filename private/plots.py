import os
from dataclasses import dataclass
import json
from matplotlib import pyplot as plt
from json import JSONEncoder, JSONDecoder
import numpy as np

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class NumpyArrayDecoder(JSONDecoder):
    def default(self, obj):
        return np.ndarray(JSONDecoder.decode(obj))


base_path = os.path.join('..', "figs")

dirs = filter(os.path.isdir, [os.path.join(base_path, path) for path in os.listdir(base_path)] )

RESULT_STR = "results.json"
CONFIG_STR = "config.json"

@dataclass
class config:
    noAgents : int
    problem: str
    problem_size: int
    num_of_communication: int

    def __hash__(self) -> int:
        return hash(self.noAgents) + hash(self.problem) + hash(self.problem_size) + hash(self.num_of_communication)


data_dict = {}
RASTRIGIN = "Rastrigin"
ACKLEY = "Ackley"
GRINEWANK = "Griewank"
problem_name = ACKLEY
for dir in dirs:
    with open(os.path.join(dir, CONFIG_STR), "r") as faaa:
        global config1
        config1 = config(**json.load(faaa))
    
    with open(os.path.join(dir, RESULT_STR), "r") as results:
        global data1
        data1 = json.load(results, cls= NumpyArrayDecoder)
    data_dict[config1] = data1

keys5 = list(filter(lambda x : x.noAgents == 5 and x.problem == problem_name, data_dict.keys()))
keys10 = list(filter(lambda x : x.noAgents == 10 and x.problem == problem_name, data_dict.keys()))

legend_list = []
def draw_comparisson_multi_and_single(x_coor_multi, results_multi, x_coor_single , results_single, legend: str):

    results_multi = np.mean(results_multi,axis=0)
    results_single = np.mean(results_single,axis=0)
    x_coor_single = np.mean(x_coor_single,axis=0)
    x_coor_multi = np.mean(x_coor_multi,axis=0)

    plt.plot(x_coor_multi[:90], results_multi[:90], "r")
    plt.plot(x_coor_single[:90], results_single[:90], "g--")

    plt.title(f"Problem {problem_name} size 100")
    plt.xlabel("Number of iterations of evolutionary algorithm")
    plt.ylabel("Objective value")
    legend_list.extend(legend)
    #plt.savefig(os.path.join('../figs', f"{name}_{date}.png"))
    #plt.show()

for _, one_data  in data_dict.items():
    for key, val in one_data.items():
        val = val[2:-2].split("], [")
        val = [[float(item) for item in el.split(", ")] for el in val]
        val = np.array([np.array(numbers) for numbers in val])
        one_data[key] = val 

draw_comparisson_multi_and_single(**data_dict[keys5[0]], legend=[f"{keys5[0].noAgents} agents in system", f"Single agent in system"])
def add_plot(x_coor_multi, results_multi,x_coor_single , results_single, legend, line):
    results_multi = np.mean(results_multi,axis=0)
    x_coor_multi = np.mean(x_coor_multi,axis=0)

    plt.plot(x_coor_multi[:46], results_multi[:46], line)
    legend_list.extend(legend)


add_plot(**data_dict[keys10[0]], legend=[f"{keys10[0].noAgents} agents in system "], line = "b-.")
plt.legend(legend_list)
plt.show()

for key, val in data_dict.items():
    print(f"Agents {key.noAgents} Communication {key.num_of_communication} coor {val['x_coor_multi'][0][::20]} , res {val['results_multi'][0][::20]}")

print(f"Agents 1 Communication 0 coor {data_dict[keys5[0]]['x_coor_single'][0][::20]} , res {val['results_single'][0][::20]}")
