
from copy import copy

from numpy import diff
from Evolutionary_algorithm import S
import random 
from jmetal.core.solution import Solution
import numpy as np


def crossover(population_old, population_new, crossover_operator):
    offspring_population = []
    population_size = len(population_old)
    for idx, solution in enumerate(population_new, start= 1):
        for j in range(int(len(population_new))):
            new_solution = copy(solution)
            offspring_population.extend(crossover_operator.execute([new_solution,  random.choice( population_old)]))

    return offspring_population

def mutation(population_old, population_new, mutation_oparator, trust_level):
    offspring_population = []
    population_size = len(population_old)
    for idx, solution in enumerate(population_new, start= 1):
        new_solution = copy(solution)
        offspring_population.append(mutation_oparator(new_solution, random.choice( population_old),trust_level))

    return offspring_population

def average_operator(new_solution : Solution, old_soultion: Solution, trust_level :int):
    diff_list =  abs(np.array(new_solution.variables) - np.array(old_soultion.variables))
    diff_list = list(enumerate(diff_list))
    solution_type = type(new_solution.variables[0])
    diff_list.sort(reverse=True, key = lambda x : x[1])
    for i in range (0, min(trust_level, len(diff_list))):
        old_soultion.variables[diff_list[i][0]] = solution_type((old_soultion.variables[diff_list[i][0]] + new_solution.variables[diff_list[i][0]])/2)
    return old_soultion

def swap_operator(new_solution : Solution, old_soultion: Solution, trust_level :int):
    diff_list =  abs(np.array(new_solution.variables) - np.array(old_soultion.variables))
    solution_type = type(new_solution.variables[0])
    diff_list = list(enumerate(diff_list))
    diff_list.sort(reverse=True, key = lambda x : x[1])
    for i in range (0, min(trust_level, len(diff_list))):
        old_soultion.variables[diff_list[i][0]] = solution_type(new_solution.variables[diff_list[i][0]])
    return old_soultion
