
class CommunicationType:
    def __init__(self):
        self.operator: function = None
        self.mutation: function = None
        self.mutation_type: function = None

    def communicate(self, agent1, agent2) -> bool:
        raise NotImplementedError()
