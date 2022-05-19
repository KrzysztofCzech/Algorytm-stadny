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

    def send_solution(self):
        return self.Island.get_solutions()

    def get_front(self):
        return self.Island.algorithm.get_result()

    def compare(self, other):
        sol = self.get_front()
        return self.get_front().objectives[0] < other.get_front().objectives[0]


    def communicate(self, agent):
        if (self.compare(agent)):
            agent.Island.update_solutions(self.send_solution())
        else:
            self.Island.update_solutions(agent.send_solution())



    

