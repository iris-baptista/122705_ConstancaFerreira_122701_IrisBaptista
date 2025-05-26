from dt import train_decision_tree
import csv
import math
from testArvore import DecisionNode, ConclusionNode

def load_train_dataset(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        headers = next(reader)
        feature_names = headers[1:-1]  # Skip ID, exclude label
        X, y = [], []
        for row in reader:
            X.append(row[1:-1])  # Skip ID column
            y.append(int(row[-1])) # Last column is the label
    return feature_names, X, y

#########################################################

def findSubsets(valores, labels, atributeIndex):
    d= {}

    for vIndex in range(0, len(valores)):
        valorAtual= valores[vIndex][atributeIndex]
        
        if(d.get(valorAtual) == None): #se o valor ainda n esta no dicionario 
            d[valorAtual]= [0, 0] #numero de 1s e -1s initializado
        
        oldD= d.get(valorAtual)
        if(labels[vIndex] == 1):
            d[valorAtual]= [oldD[0]+1, oldD[1]]
        else: #se for -1
            d[valorAtual]= [oldD[0], oldD[1]+1] 

    return d

def entropia(numeroOcorrencias): 
    total= numeroOcorrencias[0]+numeroOcorrencias[1]
    probFruta= (float) (numeroOcorrencias[0]/total)
    if(probFruta == 0):
        logFruta= 0
    else:
        logFruta= math.log2(probFruta)

    probNaoFruta= float (numeroOcorrencias[1]/total)
    if(probNaoFruta == 0):
        logNaoFruta= 0
    else:
        logNaoFruta= math.log2(probNaoFruta)
    
    e= -((probFruta*logFruta) + (probNaoFruta*logNaoFruta))

    label= 1
    if(numeroOcorrencias[1] > numeroOcorrencias[0]): #se temos mais nFruta essa fica a label
        label= -1

    return [round(e, 3), total, label]

def entropiaInitial(labels):
    fruta= 0
    nFruta= 0
    for l in labels:
        if(l == 1):
            fruta+= 1
        else:
            nFruta+= 1 

    total= fruta + nFruta
    probFruta= (float) (fruta/total)
    if(probFruta == 0):
        logFruta= 0
    else:
        logFruta= math.log2(probFruta)

    probNaoFruta= float (nFruta/total)
    if(probNaoFruta == 0):
        logNaoFruta= 0
    else:
        logNaoFruta= math.log2(probNaoFruta)
    
    e= -((probFruta*logFruta) + (probNaoFruta*logNaoFruta))
    return [round(e, 3), total]

def ig(entropiaInitial, entropias): 
    soma= 0
    for e in entropias.values():
        soma+= e[0]*e[1]

    mediaPonderada= 1/entropiaInitial[1] * (soma)
    ig= entropiaInitial[0] - mediaPonderada

    return round(ig, 3)

def countZeros(entropias):
    zeros= {}
    for chave, valor in entropias.items():
        if(valor[0] == 0):
            zeros[chave]= valor
    
    return zeros

def newDataset(f, oldX, oldY, toRemove, atributeIndex): #calcular nova subset, as atributes e as suas labels 
    f.pop(atributeIndex)

    toPop= []
    for xIndex in range(0, len(oldX)):
        currentX= oldX[xIndex]
        if(currentX[atributeIndex] in toRemove):
            toPop.insert(0, xIndex) #adiciona o index ao inicio da lista 
            #assim a lista de coordenadas fica em ordem decrescente

    newX= oldX
    newY= oldY
    for p in toPop:
        newX.pop(p)
        newY.pop(p)

    return [f, newX, newY]

#main
f, X, y = load_train_dataset("train.csv")

def main(f, X, y):
    entropiaDataset= entropiaInitial(y)
    biggestIG= [-1, None, None] #default para comecar 
    for aIndex in range(0, len(f)): #calcular todas as tabelas 
        dados= findSubsets(X, y, aIndex) 

        entropias= {}
        for subset in dados:
            #subset e a chave nao o valor associado
            entropias[subset]= entropia(dados.get(subset))
        
        currentIG= [ig(entropiaDataset, entropias), aIndex, entropias]
        if(currentIG[0] > biggestIG[0]):
            biggestIG= currentIG

    print(biggestIG)
    root= DecisionNode(biggestIG[1])
    zeros= countZeros(biggestIG[2]) 
    #{1:[0, 6, 1], 2:[3, 3, -1], 3:[0, 3, 1]}
    #{1:[0, 6, 1], 2:[3, 3, -1], 3:[0, 3, 1], 4:[0, 2, -1]}
    #biggestIG[2]
    if(len(zeros) >= 1): #se temos mais q 1 zero
        fruit= []
        nFruit= []

        toRemove= []
        for chave, valor in zeros.items():
            toRemove.append(chave)

            if(valor[2] == 1):
                fruit.append(chave)
            else:
                nFruit.append(chave)
        
        #vamos ter ou 1 ou 2 folhas
        if(len(fruit) > 0):
            root.setLeft(ConclusionNode(1), fruit)
            
            if(len(nFruit) > 0): #se tb tem uma segunda folha para -1
                root.setMiddle(ConclusionNode(-1), nFruit)
        else: #se a conclusao nao e 1, tem de ser -1
            root.setLeft(ConclusionNode(-1), nFruit)

    else: #se temos 0 casos de entropia ser 0 (so adicionamos )
        smallestE= [100, None]
        for chave, valor in biggestIG[2].items(): #iterar sobre as entropias 
            if(valor[0] < smallestE):
                smallestE= [valor[0], chave]

        toRemove= smallestE[1]
        root.setLeft(ConclusionNode(smallestE[2]), smallestE[1]) #adicionar o no de conclusion

    newDataset(f, X, y, toRemove, biggestIG[1])

    resto= []
    for chave in biggestIG[2]:
        if(chave not in toRemove):
            resto.append(chave)

    root.setRight(main(f, X, y), resto) #isto nao tem a root por isso acho q nao da para percorrer, mas eu so quero ver a condicao de paragem 
    
main(f, X, y)

#["orange", "blueberry", "banana"], 0
#["orange", "yellow"], 1
# novoF, novoX, novoY= newDataset(f, X, y, ["orange", "blueberry", "banana"], 0) 
# print(novoF)
# print(novoX)
# print(novoY)
#################################TESTES#################################
#se threshold reached:
#fazer tudo folhas 
#caso contrario:
#def a subset criada por a divisao 
#chamada recursiva

#fruit_classifier = train_fruit_classifier('train.csv')
#print(fruit_classifier)