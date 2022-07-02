from ast import Str
from Island import Island
from communication import AttiduteType, get_selector, CommunicationType, CommunicationBasic
from statistics import mean

from typing import List
from Utils  import mean_of_solutions

class Agent():
    def __init__ (self,Island:Island, name: Str, attidute : AttiduteType, communication_type : CommunicationType):
        self.Island = Island
        self.name = name
        self.trust_dict = {}
        self.attidute = attidute
        self.communication = communication_type


    def initalize(self):
        self.trust_dict = {}
        self.Island.clear_data_and_start()

    def run(self, iterations):
        self.Island.run(iterations)

    def get_result(self):
        return self.Island.algorithm.get_result()

    def get_solution(self):
        return self.Island.get_solutions()

    def transfer_data(self, name_other):
        trust_level = self.check_trust(name_other)
        selector = get_selector(self.attidute)
        return selector(trust_level, self.get_solution())


    def communicate(self, obj):
        
        self.communication.comunnicate(self, obj)


    def get_num_of_iteration(self):
        return len(self.Island.get_history_soultion())

    def check_trust(self, name_other) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        
        return self.trust_dict[name_other]

    def update_trust(self, name_other: Str, val: int) -> None:
        if not (name_other in self.trust_dict):
            self.trust_dict[name_other] = 1
        self.trust_dict[name_other] += val




    

