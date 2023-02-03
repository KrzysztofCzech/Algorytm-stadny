from agent.island import Island
from trust.base_trust import Trust
from primitives.primitiveTypes import CommunicationType

class BaseAgent():
    def __init__ (self,Island:Island, name: str, attidute, communication_type : CommunicationType):
        self.Island = Island
        self.name = name
        self.attidute = attidute
        self.communication = communication_type



    def initalize(self, observer):
        raise NotImplementedError()

    def run(self, iterations):
        raise NotImplementedError()

    def get_result(self):
        raise NotImplementedError()

    def get_trust_memory(self, name_other: str) -> Trust:
        raise NotImplementedError()

    def get_solutions(self):
        raise NotImplementedError()

    def transfer_data(self, name_other):
        raise NotImplementedError()


    def communicate(self, obj):
        raise NotImplementedError()


    def get_num_of_iteration(self):
        raise NotImplementedError()

    def check_trust(self, name_other) -> None:
        raise NotImplementedError()
