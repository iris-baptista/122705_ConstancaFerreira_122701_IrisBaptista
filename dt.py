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
        self.atribute= atributeId #para identificar a atribute q representa 

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
            return self.saidaM
        else:
            print("Not a valid value for the atribute being used!")

class ConclusionNode():
    def __init__(self, l): 
        self.label= l #1 para fruit, -1 para nao fruit

    def getLabel(self):
        return self.label 
    
################################ Class Principal ################################
class DecisionTree:
    root= None

    #fazemos os branches 
    #usa a entropia e a information gain  
    #deve ter recursao (da para fazer mesmo sendo um construtor)
    def __init__(self, X, y, atributes, threshold=1.0, max_depth=50): 
        entropiaDataset= entropiaInitial(y)
        biggestIG= [-1, None, None] #initializar para substituir 
        for aIndex in range(0, len(atributes)): #calcular todas as tabelas 
            dados= findSubsets(X, y, aIndex) 

            entropias= {}
            for subset in dados: #subset e a chave do dicionario
                entropias[subset]= entropia(dados.get(subset))
            
            currentIG= [ig(entropiaDataset, entropias), aIndex, entropias]
            if(currentIG[0] > biggestIG[0]): #se o IG calculado for maior do q o guardado
                biggestIG= currentIG #atualizar maior ig

        self.root= DecisionNode(biggestIG[1])
        #print("Root")

        zeros= countZeros(biggestIG[2]) 
        if(len(zeros) >= 1): #se temos mais q 1 caso de entropia ser zero
            fruit= []
            nFruit= []
            toRemove= []

            for chave, valor in zeros.items():
                toRemove.append(chave) #guardar todos os valores das atributes q vao dar a um no de conclusao 

                if(valor[2] == 1): #se a label for 1 
                    fruit.append(chave)
                else: #se a label for -1
                    nFruit.append(chave)
            
            #vamos ter ou 1 ou 2 folhas como ha 1+ casos de ser 0 (e so pode ser fruit/nFruit)
            if(len(fruit) > 0): #se uma das folhas classifica como 1 (fruta)
                self.root.setLeft(ConclusionNode(1), fruit)
                #print("Left is fruit with conditions ", fruit)
                
                if(len(nFruit) > 0): #se tb tem uma segunda folha para -1
                    self.root.setMiddle(ConclusionNode(-1), nFruit)
                    #print("Middle is not fruit with conditions ", nFruit)
            else: #se a conclusao nao e 1, tem de ser -1 
                self.root.setLeft(ConclusionNode(-1), nFruit)
                #print("Left is not fruit with conditions ", nFruit)
        else: #se temos 0 casos de entropia ser 0 (so adicionamos um no basiado na menor entropia)
            smallestE= [100, None, None] #initializar para encontrar a menor entropia
            for chave, valor in biggestIG[2].items(): #iterar sobre as entropias 
                if(valor[0] < smallestE[0]): #se encontramos uma entropia menor 
                    smallestE= [valor[0], chave, valor[2]] #atualizar menor entropia  

            toRemove= smallestE[1]
            #print("Left is fruit= ", smallestE[2], " para ", smallestE[1])
            self.root.setLeft(ConclusionNode(smallestE[2]), smallestE[1]) #adicionar o no de conclusion

        atributes, X, y= newDataset(atributes, X, y, toRemove, biggestIG[1])

        resto= [] #valores q vao dar ao ramo restante 
        for chave in biggestIG[2]:
            if(chave not in toRemove):
                resto.append(chave)

        #check condicoes de paragem 
        if(len(atributes) == 0 or thresholdReached(y, threshold) or max_depth-1 == 0): #se nao ha proximo atribute ou se ja antigio o threshold ou se a max height foi antigida 
            divisoes= spreadValues(entropias, resto) #dividir os valores restantes entre fruit e nFruit

            labelLeft= self.root.getLeft().getLabel()
            mid= self.root.getMiddle()

            if(labelLeft == 1): #se a da esquerda classificar fruta
                self.root.addConditionsLeft(divisoes[0]) #adicionar frutas as condicoes

                #mid tem de ter label -1 (a q resta)
                if(mid == None): #se ainda nao criou middle no 
                    self.root.setMiddle(ConclusionNode(-1), divisoes[1]) #criar no do meio 
                else: #se ja existe, adiciona os nao fruit as condicoes 
                    self.root.addConditionsMiddle(divisoes[1])
            else: #se left for -1
                self.root.addConditionsLeft(divisoes[1])

                #mid tem de ter label 1
                if(mid == None):
                    self.root.setMiddle(ConclusionNode(1), divisoes[0])
                else: 
                    self.root.addConditionsMiddle(divisoes[0])
        else: #se continua a recursao vai criar uma arvore nova. A raiz dessa nova vai ser o no da direita
            self.root.setRight(DecisionTree(X, y, atributes, threshold, max_depth-1).getRoot(), resto) 
    
    #x e um objeto novo para classificarmos 
    def predict(self, x): # (e.g. x = ['apple', 'green', 'circle'] -> 1 or -1)
        nextNode= self.root
        while(nextNode.__class__ != ConclusionNode):
            index= nextNode.getAtributeIndex()
            value= x.pop(index) #pop para os proximos indexes baterem certo  
            
            nextNode= nextNode.getSaida(value)
            
        return nextNode.getLabel()

    def getRoot(self):
        return self.root

################################ Fns Usadas ################################ 
#calcular primeira coluna das tabelas 
def findSubsets(valores, labels, atributeIndex):
    d= {} #dicionario vai ter {atribute: [numFruta, numNaoFruta]}

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

#calcular entropia 
def entropia(numeroOcorrencias): #numeroOcorrencias= [numFruit, numNaoFruit]
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

#calcula a entropia da dataset completa 
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

#calcula information gain 
def ig(entropiaInitial, entropias): 
    soma= 0
    for e in entropias.values():
        soma+= e[0]*e[1]

    mediaPonderada= 1/entropiaInitial[1] * (soma)
    ig= entropiaInitial[0] - mediaPonderada

    return round(ig, 3) #resultado dado com 3 valores decimais

#conta numero de entropias homogeneas 
def countZeros(entropias):
    zeros= {}
    for chave, valor in entropias.items():
        if(valor[0] == 0):
            zeros[chave]= valor
    
    return zeros

#devolve a nova dataset sem os valores classificados, e sem o atribute utilizado
def newDataset(f, X, y, toRemove, atributeIndex): #calcular nova subset, as atributes e as suas labels 
    f.pop(atributeIndex) #remover a atribute 

    newX= []
    for xIndex in range(len(X)-1, -1, -1): #vai ir em ordem decrescente para os indexes baterem certo
        currentLine= X[xIndex]
        if(currentLine[atributeIndex] in toRemove): #se e para remover a linha
            y.pop(xIndex) #tira a label associada a linha
        else: #se for para manter a linha 
            currentLine.pop(atributeIndex)
            newX.insert(0, currentLine) #para ficar sempre a frente das anteriores

    return [f, newX, y]

#verifica se o threshold ja foi antigido 
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

#divide os valores de resto entre fruit e nFruit
def spreadValues(entropias, resto):
    divisoes= [[], []]

    for chave, valor in entropias.items():
        if(chave in resto):
            if(valor[2] == 1): #se label for 1
                divisoes[0].append(chave)
            else: #se a label for -1
                divisoes[1].append(chave)

    return divisoes #[fruit, nFruit]

def train_decision_tree(X, y, a):
    threshold= 0.75
    max_depth= 50

    return DecisionTree(X, y, a, threshold, max_depth)