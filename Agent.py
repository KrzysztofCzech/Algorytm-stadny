from Island import Island

class Agent():
    def __init__ (self,Island:Island):
        self.Island = Island
        self.drawing_series_labels = "Label"

    def run(self, iterations):
        self.Island.run(iterations)

    def get_result(self):
        return self.Island.algorithm.get_result()

    def drawing_fun():
        pass

    def migrate(self,size):
        return self.Island.algorithm.solutions[0:size]