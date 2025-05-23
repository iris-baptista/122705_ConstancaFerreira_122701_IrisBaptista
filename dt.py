import numpy as np

class DecisionTree:
    #fazemos os branches 
    #usa a entropia e a ig 
    #deve ter recursao (da para fazer mesmo sendo um construtor)
    def __init__(self, X, y, threshold=1.0, max_depth=None): # Additional optional arguments can be added, but the default value needs to be provided
        #calc ig de cata atribute
        #escolher melhor ig 
        #def as subset criadas e fazer chamada recursiva com subset 
        #repetir ate threshold ou ate todo ser homogeneo?
        pass

    #x e um objeto novo para classificarmos 
    #aqui usamos os branches?
    def predict(self, x): # (e.g. x = ['apple', 'green', 'circle'] -> 1 or -1)
        #if == isto return aquilo 
        ##else if == y : if == z etc
        pass

    def entropia(condicao): #condicao: atribute= categoria
        #conta numero de 1s (fruta) e -1s (nao fruta)
        #calcula prop de 1s e prob de -1s
        #calcula os log(prop) de 1s e -1s
        #equacoa da entropia 
        #devolve resultado
        pass

    def ig(subset): 
        #calc entropia da dataset toda
        #calc entropias de todas as categorias da attribute (i.e. atribute color teria categorias blue, red etc.)
        #equacao da ig
        #devolver valor
        pass


def train_decision_tree(X, y): #x e y ==??
    # Replace with your configuration
    #qual configuracao?
    return DecisionTree(X, y)
