from agent.island import Island
from trust.base_trust import Trust
from primitives.primitiveTypes import CommunicationType


class BaseAgent():
    def __init__(self, island: Island, name: str, attitude, communication_type: CommunicationType):
        self.Island = island
        self.name = name
        self.attitude = attitude
        self.communication = communication_type

    def initialize(self, observer):
        raise NotImplementedError()

    def run(self, iterations):
        raise NotImplementedError()

    def get_result(self):
        raise NotImplementedError()

    def get_trust_memory(self) -> Trust:
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
