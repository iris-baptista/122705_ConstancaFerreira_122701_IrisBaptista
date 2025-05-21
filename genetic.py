import random

def create_individual(individual_size):
    return [random.uniform(-1, 1) for _ in range(individual_size)]

def generate_population(individual_size, population_size):
    return [create_individual(individual_size) for _ in range(population_size)]

def genetic_algorithm(individual_size, population_size, fitness_function, target_fitness, generations, elite_rate=0.2, mutation_rate=0.05):
    population = generate_population(individual_size, population_size) #population initial
    best_individual = None
   
    #while target fitness != bestIndividual fitness e generations != generations 

    #avaliar individuals com a fittness function dada
    #vai atualizando o best_individual

    #selecionar os melhor 0.2 individos para guardar na nova populacao (elitism)

    #ate ter preenchido a nova populacao
    #escolher pais (tournament)
    #crossover (one point)
    #mutation (scramble)
    
    #population= newPop
    #endwhile

    return best_individual # This is expected to be a pair (individual, fitness)