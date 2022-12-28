from copy import copy
from typing import TypeVar, List
import random
from jmetal.core.algorithm import EvolutionaryAlgorithm
from jmetal.core.operator import Mutation, Crossover
from jmetal.core.problem import Problem
from jmetal.util.evaluator import Evaluator, SequentialEvaluator
from jmetal.util.generator import Generator, RandomGenerator
from jmetal.util.termination_criterion import TerminationCriterion
from jmetal.util.constraint_handling import overall_constraint_violation_degree
from jmetal.core.operator import Selection
from jmetal.operator.selection import NaryRandomSolutionSelection

S = TypeVar('S')
R = TypeVar('R')

class EvolutionAlgoritm(EvolutionaryAlgorithm[S, R]):

    def __init__(self,
                 problem: Problem,
                 population_size: int,
                 offspring_population_size: int,
                 mutation: Mutation,
                 selection: Selection,
                 crossover: Crossover,
                 termination_criterion: TerminationCriterion,
                 population_generator: Generator = RandomGenerator(),
                 population_evaluator: Evaluator = SequentialEvaluator()):
        super(EvolutionAlgoritm, self).__init__(
            problem=problem,
            population_size=population_size,
            offspring_population_size=offspring_population_size)
        self.population_size = population_size
        self.offspring_population_size = offspring_population_size

        self.mutation_operator = mutation
        self.selection_operator = selection
        self.replacement_operator = NaryRandomSolutionSelection(number_of_solutions_to_be_returned=population_size)

        self.population_generator = population_generator
        self.population_evaluator = population_evaluator
        self.crossover_oparator = crossover

        self.termination_criterion = termination_criterion
        self.observable.register(termination_criterion)

    def create_initial_solutions(self) -> List[S]:
        return [self.population_generator.new(self.problem)
                for _ in range(self.population_size)]

    def evaluate(self, solution_list: List[S]):
        return self.population_evaluator.evaluate(solution_list, self.problem)

    def stopping_condition_is_met(self) -> bool:
        return self.termination_criterion.is_met

    def selection(self, population: List[S]) -> List[S]:
        return population

    def reproduction(self, population: List[S]) -> List[S]:
        offspring_population = []
        for solution in population:
            for j in range(max(1,int(self.offspring_population_size/2 / len(population)))):
                new_solution = copy(solution)
                offspring_population.append(self.mutation_operator.execute(new_solution))
                
        for i in range(max(5,len(offspring_population)-self.offspring_population_size)):
            solution1, solution2 = random.sample(population, 2)
            offspring_population.extend(self.crossover_oparator.execute([copy(solution1), copy(solution2)]))


        return offspring_population

    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        population_pool = []
        population_pool = population
        population_pool.extend(offspring_population)


        population_pool.sort(key=lambda s:(overall_constraint_violation_degree(s), s.objectives[0]))
        #new_population = self.replacement_operator.execute(population_pool)
        new_population = [population_pool[0]]
        for i in range(self.population_size - 1):
            new_population.append(self.selection_operator.execute(population_pool[1:]))
        return new_population

    def get_result(self) -> R:
        return self.solutions[0]

    def get_name(self) -> str:
        return 'Evolution algorithm'
