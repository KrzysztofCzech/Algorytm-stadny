# Komunikacja agentów

1. Komunikacja pomiędzy agentami opiera jest inicjalizowana w każdym cyklu po przejsciu iteracje algorytmu ewolucyjnego wyspy każdego agenta.
plik Executor.py 
def run(self, cycles : int, cycle_iter: int, num_of_comm:int)

2. Każdy agent probóje nawiązać komunikacje z agentem (ilośc prob zależna od parametru)
plik Executor.py 
def communicate(self, number_of_communications)

3. Agent wywołuje przekazany podczas inicalizajcji typ komunikacji. Typy komnikacji dostępne są w pliku communication.py 

# Dostępne typy komunikacji 

## Basic Communication plik communication.py 
1. uzysaknie osobników od agenta2 na podstawie zaufania
    new_population = agent2.transfer_data(agent1.name) 
2. porwnanie średnich wartości uzyskanej populacji z aktualną 
    solutions_old = agent1.get_solution() 
    mean_old = mean_of_solutions(solutions_old)
    mean_new = mean_of_solutions(new_population)
    if mean_new < mean_old:
3. aktualizacja populacji 
        agent1.Island.update_solutions(new_population)
    1. plik Island.py
        * def update_solutions(self, new_solutions):
    2. uzykanie populacji stosując operator crossover wykorzystając operator  przekazany podczas inicjalizacji aktulanie uzywnany jest SBXCrossover
        * crossover_population = self.algorithm.crossover(new_solutions)
        1. plik Evolutionary_algorithm.py
            * def crossover(self, population: List[S]) -> List[S]:
                * offspring_population = []
                * for idx, solution in enumerate(population, start= 1):
                    * for j in range(int(len(population)*2)):
                        * new_solution = copy(solution)
        2. uzyskanie nowego osobnika wykonując crossover na otrzymanaym osobniku oraz jednym ze starych osobnikó
            * offspring_population.extend(self.crossover_operator.execute([new_solution, self.solutions[j*idx % self.population_size]]))
                * return offspring_population
   1. ewaluacja wyników i zapisanie nowych rozwiązań    
        * offspring_population = self.algorithm.evaluate(crossover_population)
        * self.algorithm.solutions = self.algorithm.replacement(self.algorithm.solutions, offspring_population.

4. sprawdzenie poprawy populacji       
    * solutions_new = agent1.get_solution()
    * mean_updated = mean_of_solutions(solutions_new)
    * if mean_updated < mean_old:
        * agent1.update_trust(agent2.name, 1)

5. aktualizacja rozwiazań
    * agent1.Island.update_solutions(new_population)