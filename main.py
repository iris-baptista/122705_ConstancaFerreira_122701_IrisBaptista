import random
import argparse
import csv

from pathlib import Path

from game import start_game, get_score
from genetic import genetic_algorithm
from nn import create_network_architecture
from dt import train_decision_tree


STATE_SIZE = 1 + 3 * 3
MAX_SCORE = 100

def fitness(nn, individual, seed):
    nn.load_weights(individual)
    random.seed(seed)
    return get_score(player=lambda state: nn.forward(state))

def train_ai_player(filename, population_size, generations):
    nn = create_network_architecture(STATE_SIZE)
    individual_size = nn.compute_num_weights()

    fitness_function = lambda individual, seed=None: fitness(nn, individual, seed)

    best = genetic_algorithm(individual_size, population_size, fitness_function, MAX_SCORE, generations)
    print(best)
    with open(filename, 'w') as f:
        f.write(','.join(map(str, best[0])))


def load_ai_player(filename):
    
    file_path = Path(filename)

    if not file_path.exists():
        return None

    with open(filename, 'r') as f:
        weights = list(map(float, f.read().split(',')))

    nn = create_network_architecture(STATE_SIZE)
    nn.load_weights(weights)

    return lambda state: nn.forward(state)


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
    dt = train_decision_tree(X, y)
    return lambda item: dt.predict(item) 


def main():
    parser = argparse.ArgumentParser(description='IA 2024/2025 - Project 2 - Fruit Catcher')
    parser.add_argument('-t', '--train', action='store_true', help='train neural AI player with genetic algorithm')
    parser.add_argument('-p', '--population', default=100, help='the population size for the genetic algorithm', type=int)
    parser.add_argument('-g', '--generations', default=100, help='the number of generations for the genetic algorithm', type=int)
    parser.add_argument('-f', '--file', default='best_individual.txt', help='the file to store/load the AI player weights')
    parser.add_argument('-l', '--headless', action='store_true', help='run without graphics')
    args = parser.parse_args()

    if args.train:
        train_ai_player(args.file, args.population, args.generations)
        exit()


    ai_player = load_ai_player(args.file) 

    fruit_classifier = train_fruit_classifier('train.csv')

    if args.headless:
        score = get_score(ai_player, fruit_classifier)
        print(f'Score: {score}')
    else:
        start_game(ai_player, fruit_classifier)
    

if __name__ == '__main__':
    main()
