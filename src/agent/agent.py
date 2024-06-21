from agent.island import Island, PopulationsData
from communication.types import AttitudeType, get_selector
from agent.base_agent import BaseAgent
from trust.base_trust import Trust
from typing import List
from primitives.primitiveTypes import CommunicationType
import numpy as np


def probability_generator(own, other):
    if own == other:
        res = own * 2
    else:
        res = own + (own - other) * 1.3
    return np.clip(a_min=0.00001, a_max=0.1, a=res)


class Agent(BaseAgent):
    def __init__(self, island: Island, name: str, attitude: AttitudeType, communication_type: CommunicationType,
                 trust_type: Trust):
        super().__init__(island, name, attitude, communication_type)
        self.trust_memory = trust_type

    def initialize(self, observer):
        self.Island.clear_data_and_start()
        self.trust_memory.trust_dict = {}
        self.Island.algorithm.observable.register(observer)

    def run(self, iterations):
        self.Island.run(iterations)

    def get_result(self):
        return self.Island.algorithm.get_result()

    def get_solutions(self):
        return self.Island.get_solutions()

    def set_communication_type(self, communication_type: CommunicationType):
        self.communication = communication_type
        return self

    def transfer_data(self, name_other):
        trust_level = self.check_trust(name_other)
        selector = get_selector(self.attitude)
        return selector(trust_level, self.get_solutions())

    def communicate(self, obj) -> bool:
        return self.communication.communicate(self, obj)

    def get_num_of_iteration(self):
        return len(self.Island.get_history_solution())

    def get_trust_memory(self) -> Trust:
        return self.trust_memory

    def get_island_history(self) -> List[PopulationsData]:
        return self.Island.get_population_data()

    def random_restart(self):
        self.Island.restart_from_random_place()

    def check_trust(self, name_other) -> int:
        return self.get_trust_memory().check_trust(name_other)

    def get_algorithm_stats(self):
        return self.Island.algorithm.mutation_operator.probability, self.Island.algorithm.crossover_operator.probability

    def change_probability(self, mutation_probability, crossover_probability):
        own_mutation_probability, own_crossover_probability = self.get_algorithm_stats()
        self.Island.algorithm.mutation_operator.probability = probability_generator(own_mutation_probability,
                                                                                    mutation_probability)
        self.Island.algorithm.crossover_operator.probability = probability_generator(own_crossover_probability,
                                                                                     crossover_probability)
