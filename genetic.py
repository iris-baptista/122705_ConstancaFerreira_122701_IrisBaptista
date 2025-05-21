import random

def create_individual(individual_size):
    return [random.uniform(-1, 1) for _ in range(individual_size)]

def generate_population(individual_size, population_size):
    return [create_individual(individual_size) for _ in range(population_size)]

def tournamentSelection(population):
    #randomly escolhe 2s individuos
    #o melhor e p1
    p1= "default"

    p2= None #initialzar p2
    while(p2 == None):
        #randomly escolhe 2s individuos
        #o melhor e p
        p= "default"

        if(p != p1):
            p2= p

    return p1, p2

def onePointCrossOver(p1, p2): #devolve um filho!
    midPoint= round((len(p1)+1)/2)
    child1= p1[0:midPoint]+p2[midPoint:] #deviamos escolher um?
    child2= p2[0:midPoint]+p1[midPoint:]

    #ver qual e melhor

    return child1 #default agora para nao dar erro

def mutate():
    #escolhe um grupo consecutivo 
    #faz scramble aos valores 
    pass

#double check parameters in main code broskie 
def genetic_algorithm(individual_size, population_size, fitness_function, target_fitness, generations, elite_rate=0.2, mutation_rate=0.05):
    population = generate_population(individual_size, population_size) #population initial
    best_individual = (None, 0) #initializar population
    
    generated= 0 
    while(target_fitness > best_individual[1] and generated != generations): #while condicoes de paragem nao sao met  
        for i in population:  #avaliar todos os individuals dados na populacao
            fitness= fitness_function(i) #avaliar com fitness function (FALTA UM SEED????????)
            
            if(fitness > best_individual[1]): #vai atualizando o best_individual se tem fitness menor
                best_individual= (i, fitness)

        elite= 0 #selecionar os melhor 0.2 individos para guardar na nova populacao (elitism)
        newPop= elite #initializar a nova populacao com o melhor 20% da populacao anterior 

        while(len(newPop) != population_size): #ate ter preenchido a nova populacao
            p1, p2= tournamentSelection(elite) #escolher pais (tournament)
            child= onePointCrossOver(p1, p2) #crossover (one point)
        
            if(mutation_rate): #se for para mutar
                child= mutate(child) 

            newPop.append(child) #add to newPop
        
        population= newPop #para proxima geracao 
        generated+= 1

    return best_individual # This is expected to be a pair (individual, fitness)