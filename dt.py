import numpy as np
import math

################################ Classes dos Nos da Arvore ################################
class DecisionNode():
    saidaL= None
    saidaR= None
    saidaM= None
    conditionL= []
    conditionR= []
    conditionM= []

    def __init__(self, atributeId):
        self.atribute= atributeId #Se calhar mudar isto para o string?

    def setLeft(self, node, condition):
        self.saidaL= node
        self.conditionL= condition

    def setRight(self, node, condition):
        self.saidaR= node
        self.conditionR= condition

    def setMiddle(self, node, condition):
        self.saidaM= node
        self.conditionM= condition

    def addConditionsLeft(self, conditions):
        for c in conditions:
            self.conditionL.append(c)
    
    def addConditionsRight(self, conditions):
        for c in conditions:
            self.conditionR.append(c)

    def addConditionsMiddle(self, conditions):
        for c in conditions:
            self.conditionM.append(c)

    def getAtributeIndex(self):
        return self.atribute
    
    def getLeft(self):
        return self.saidaL
    
    def getMiddle(self):
        return self.saidaM
    
    def getSaida(self, valor):
        if valor in self.conditionL:
            return self.saidaL
        elif valor in self.conditionR:
            return self.saidaR
        elif valor in self.conditionM:
            return self.conditionM
        else:
            print("Not a valid value for the atribute being used!")

class ConclusionNode():
    def __init__(self, l): 
        self.label= l

    def getLabel(self):
        return self.label
    
################################Class Principal################################
class DecisionTree:
    root= None

    #fazemos os branches 
    #usa a entropia e a ig 
    #deve ter recursao
    def __init__(self, X, y, atributes, threshold=1.0, max_depth=50): 
        entropiaDataset= entropiaInitial(y)
        biggestIG= [-1, None, None] #initializar para substituir 
        for aIndex in range(0, len(atributes)): #calcular todas as tabelas 
            dados= findSubsets(X, y, aIndex) 

            entropias= {}
            for subset in dados: #subset e a chave nao o valor associado
                entropias[subset]= entropia(dados.get(subset))
            
            currentIG= [ig(entropiaDataset, entropias), aIndex, entropias]
            if(currentIG[0] > biggestIG[0]):
                biggestIG= currentIG
            
        self.root= DecisionNode(biggestIG[1])
        zeros= countZeros(biggestIG[2]) 

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
                self.root.setLeft(ConclusionNode(1), fruit)
                
                if(len(nFruit) > 0): #se tb tem uma segunda folha para -1
                    self.root.setMiddle(ConclusionNode(-1), nFruit)
            else: #se a conclusao nao e 1, tem de ser -1
                self.root.setLeft(ConclusionNode(-1), nFruit)
        else: #se temos 0 casos de entropia ser 0 (so adicionamos )
            smallestE= [100, None]
            for chave, valor in biggestIG[2].items(): #iterar sobre as entropias 
                if(valor[0] < smallestE):
                    smallestE= [valor[0], chave]

            toRemove= smallestE[1]
            self.root.setLeft(ConclusionNode(smallestE[2]), smallestE[1]) #adicionar o no de conclusion

        #passa variaveis por (object) reference entao altera o valor de atributes, X, e y permanentemente
        newDataset(atributes, X, y, toRemove, biggestIG[1])

        resto= []
        for chave in biggestIG[2]:
            if(chave not in toRemove):
                resto.append(chave)

        #check condicoes de paragem 
        if(len(atributes) == 0 or thresholdReached(y, threshold) or max_depth-1 == 0): #se nao ha proximo atribute ou se ja antigio o threshold 
            divisoes= spreadValues(entropias, resto) 

            labelLeft= self.root.getLeft().getLabel()
            mid= self.root.getMiddle()

            if(labelLeft == 1):
                self.root.addConditionsLeft(divisoes[0])

                #mid tem de ter label -1
                if(mid == None):
                    self.root.setMiddle(ConclusionNode(-1), divisoes[1])
                else: 
                    self.root.addConditionsMiddle(divisoes[1])
            else: #se for -1
                self.root.addConditionsLeft(divisoes[1])

                #mid tem de ter label 1
                if(mid == None):
                    self.root.setMiddle(ConclusionNode(1), divisoes[0])
                else: 
                    self.root.addConditionsMiddle(divisoes[0])
        else: #vai criar uma arvore q vai usar a folha deste como raiz
            self.root.setRight(DecisionTree(X, y, atributes, threshold, max_depth-1).getRoot(), resto) 
    
    #x e um objeto novo para classificarmos 
    def predict(self, x): # (e.g. x = ['apple', 'green', 'circle'] -> 1 or -1)
        nextNode= self.root
        while(nextNode.__class__ != ConclusionNode):
            index= nextNode.getAtributeIndex
            value= x.pop(index) #pop para os proximos indexes ficarem corretos 

            nextNode= nextNode.getSaida(value)

        return nextNode.getLabel()

    def getRoot(self):
        return self.root

################################Fns Usadas################################ 
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
    if(numeroOcorrencias[1] >= numeroOcorrencias[0]): #se temos mais ou o mesmo nFruta essa fica a label
        label= -1 #melhor classificar uma fruta como bomba do q uma bomba como fruta

    return [round(e, 3), total, label] #devolve o valor da entropia, o numero de frutas na subset, e a label atribuida 

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

def thresholdReached(labels, threshold):
    fruit= 0
    nFruit= 0

    for l in labels:
        if(l == 1):
            fruit+= 1
        else:
            nFruit+= 1
    
    total= fruit+nFruit

    if(fruit/total >= threshold or nFruit/total >= threshold): #se antigio o threshold
        return True
    else:
        return False

def spreadValues(entropias, resto):
    divisoes= [[], []]

    for chave, valor in entropias.items():
        if(chave in resto):
            if(valor[2] == 1): #se label for 1
                divisoes[0].append(chave)
            else: #se a label for -1
                divisoes[1].append(chave)

    return divisoes #[1, -1]

def train_decision_tree(X, y, a):
    threshold= 0.75
    max_depth= 50

    return DecisionTree(X, y, a, threshold, max_depth)