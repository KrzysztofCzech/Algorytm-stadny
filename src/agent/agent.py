from agent.island import Island, PopulationsData
from communication.types import AttiduteType, get_selector, CommunicationType
from agent.base_agent import BaseAgent
from trust.base_trust import Trust 
from typing import List


class Agent(BaseAgent):
    def __init__ (self,Island:Island, name: str, attidute : AttiduteType, communication_type : CommunicationType, trust_type :  Trust):
        super().__init__(Island, name, attidute, communication_type)
        self.trust_memory = trust_type

    def initalize(self, observer):
        self.Island.clear_data_and_start()
        self.trust_memory.trust_dict = { }
        self.Island.algorithm.observable.register(observer)

    def run(self, iterations):
        self.Island.run(iterations)

    def get_result(self):
        return self.Island.algorithm.get_result()

    def get_solutions(self):
        return self.Island.get_solutions()

    def transfer_data(self, name_other):
        trust_level = self.get_trust_memory().check_trust(name_other)
        selector = get_selector(self.attidute)
        return selector(trust_level, self.get_solutions())

    def communicate(self, obj):
        self.communication.comunnicate(self, obj)

    def get_num_of_iteration(self):
        return len(self.Island.get_history_soultion())

    def get_trust_memory(self):
        return self.trust_memory

    def get_island_history(self) -> List[PopulationsData]:
        return self.Island.get_population_data()








    

