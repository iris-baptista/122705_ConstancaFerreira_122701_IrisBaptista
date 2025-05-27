from dt import train_decision_tree
import csv

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

def train_fruit_classifier(filename):
    f, X, y = load_train_dataset(filename)
    dt = train_decision_tree(X, y, f)

    return lambda item: dt.predict(item) 

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

f, X, y = load_train_dataset("train.csv")

# print(f)
# print(X)
# print(y)
# f, X, y= newDataset(f, X, y, ["orange", "yellow"], 1)
# print("_________________________")
# print(f)
# print(X)
# print(y)

#fruit_classifier = train_fruit_classifier('train.csv')

lista= [1, 2, 3, 4, 5]

print(lista[0])
print(lista[4])

print(lista[0:6])