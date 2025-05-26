class DecisionNode():
    saidaL= None
    saidaR= None
    saidaM= None
    conditionL= []
    conditionR= []
    conditionM= []

    def __init__(self, atributeId):
        self.atribute= atributeId

    def setLeft(self, node, condition):
        self.saidaL= node
        self.conditionL= condition

    def setRight(self, node, condition):
        self.saidaL= node
        self.conditionL= condition

    def setMiddle(self, node, condition):
        self.saidaL= node
        self.conditionL= condition

    def getAtributeIndex(self):
        return self.atribute
    
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
    
lista= ["red", "yellow", "blue"]

c= ConclusionNode(1)

if(c.__class__ == ConclusionNode):
    print("hi")

# if("green" in lista):
#     print("why r u running")

# if("yellow" in lista):
#     print("ahh yes")