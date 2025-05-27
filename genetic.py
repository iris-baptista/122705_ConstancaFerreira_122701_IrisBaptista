import random

def create_individual(individual_size):
    return [random.uniform(-1, 1) for _ in range(individual_size)]

def generate_population(individual_size, population_size):
    return [create_individual(individual_size) for _ in range(population_size)]

def tournamentSelection(population, ff):
    p1= population[random.randint(0, len(population)-1)] #-1 por q o tamanho total nao e um index valido
    possibleP1= population[random.randint(0, len(population)-1)]
    
    if(ff(possibleP1) > ff(p1)): #se o outro pai gerado tiver uma fitness melhor q o primeiro gerado 
        p1= possibleP1

    p2= None #initialzar p2
    while(p2 == None):
        p= population[random.randint(0, len(population)-1)]
        possibleP= population[random.randint(0, len(population)-1)]

        if(ff(possibleP) > ff(p)): #se o outro pai gerado tiver uma fitness melhor q o primeiro gerado 
            p= possibleP

        if(p != p1): #se o pai escolhido nao e igual ao p1
            p2= p

    return p1, p2

def onePointCrossOver(p1, p2, ff): #devolve um filho!
    midPoint= round((len(p1)+1)/2)
    child= p1[0:midPoint]+p2[midPoint:] #deviamos escolher um?
    possibleChild= p2[0:midPoint]+p1[midPoint:]

    if(ff(possibleChild) > ff(child)): #se o outro filho gerado tiver uma fitness melhor q o primeiro gerado 
        child= possibleChild

    return child 

def mutate(child): #mutate um bit
    index= random.randint(0, len(child)-1) #escolhe um index 
    valorAntigo= child[index]

    alteracao= random.uniform(0, 1) #gera um novo valor? Ou devia manipular o antigo???
    if(valorAntigo > 0):
        novoValor= valorAntigo - alteracao
    else:
        novoValor= valorAntigo + alteracao

    if(novoValor > 1):
        child[index]= 1
    elif(novoValor < -1):
        child[index]= -1
    else:
        child[index]= novoValor
    
    return child

def sortPop(pop, ff):
    for i in range(0, len(pop)-1):
        swapped= False

        for j in range(i, len(pop)-1):
            if(pop[j] < pop[j+1]): #por os maiores a frente
                temp= pop[j]
                pop[j]= pop[j+1]
                pop[j+1]= temp

                swapped= True
        
        if(swapped == False): #se nao trocou nada, ja esta ordenado 
            return pop

#double check parameters in main code broskie 
def genetic_algorithm(individual_size, population_size, fitness_function, target_fitness, generations, elite_rate=0.2, mutation_rate=0.05):
    print("TIME TO START")
    population = generate_population(individual_size, population_size) #population initial
    best_individual = (None, 0) #initializar population
    
    generated= 0 
    while(target_fitness > best_individual[1] and generated != generations): #while condicoes de paragem nao sao met  
        for i in population:  #avaliar todos os individuals dados na populacao
            fitness= fitness_function(i) #avaliar com fitness function (falta um seed?)
            
            if(fitness > best_individual[1]): #vai atualizando o best_individual se tem fitness menor
                best_individual= (i, fitness)

        #selecionar os melhor 0.2 individos para guardar na nova populacao (elitism)
        sortedPop= sortPop(population, fitness_function) #sort pop por fitness
        twentyPercent= round(len(sortedPop)*0.2) #primeiros 20%
        elite= sortedPop[0:twentyPercent] 

        newPop= elite
        while(len(newPop) != population_size): #ate ter preenchido a nova populacao
            p1, p2= tournamentSelection(elite, fitness_function) #escolher pais (tournament)
            child= onePointCrossOver(p1, p2, fitness_function) #crossover (one point)
        
            if(mutation_rate): #se for para mutar
                child= mutate(child) 

            newPop.append(child) #add to newPop
        
        population= newPop #para proxima geracao 
        generated+= 1

    return best_individual # This is expected to be a pair (individual, fitness)