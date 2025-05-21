import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
import random
import csv
import numpy as np


pygame.init()

#COLORS
black = (0, 0, 0)
white = (255, 255, 255)
dark_blue = (0, 0, 200)
dark_red = (200, 0, 0)
dark_green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

#DISPLAY
display_width = 500
display_height = 800
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Fruit Catcher')

#IMAGES
bg = pygame.image.load('images/background.jpg')
basket_img = pygame.image.load('images/basket.png')
basket_img = pygame.transform.scale(basket_img, (150, 100))

item_types = {}
with open('items.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=';')
    for i in reader:
        id = int(i.pop('id'))
        i['is_fruit'] = int(i['is_fruit'])
        img = pygame.image.load(f'images/items/{id}.png')
        i['image'] = pygame.transform.scale(img, (100, 100))
        item_types[id] = i

fruit_ids = [i for i, item in item_types.items() if item['is_fruit'] == 1] 
bomb_ids = [i for i, item in item_types.items() if item['is_fruit'] == -1]

clock = pygame.time.Clock()

class Basket(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.w = 150
        self.h = 100
    
    def draw(self, window):
        window.blit(basket_img, (self.x, self.y))

class Item:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.vel = 10
        self.w = 100
        self.h = 100
        self.id = id

    def draw(self, window):
        window.blit(item_types[self.id]['image'], (self.x, self.y))

def extract_state(basket, items, classifier=None):
    state = np.zeros(1 + 3 * 3)
    state[0] = (basket.x + basket.w / 2) / window.get_width()
    for i, item in enumerate(items[:3]):
        state[1 + i * 3] = (item.x + item.w / 2) / window.get_width()
        state[2 + i * 3] = item.y / window.get_height()
        if classifier is None:
            state[3 + i * 3] = item_types[item.id]['is_fruit']
        else:
            features = [item_types[item.id]['name'], item_types[item.id]['color'], item_types[item.id]['format']]
            prediction = classifier(features)
            state[3 + i * 3] = 0 if prediction is None else prediction
    return state

def human_player(_):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        return -1
    elif keys[pygame.K_RIGHT]:
        return 1
    else:
        return 0
    
def ai_player(_):
    return 0

fruit_classifier = None  

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, x, y, size):
    regText = pygame.font.Font('freesansbold.ttf', size)
    textSurf, textRect = text_objects(msg, regText)
    textRect.center = (x, y)
    window.blit(textSurf, textRect)

def button(msg, x, y, width, height, inactive_color, active_color, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if (x+width > mouse[0] > x and y+height > mouse[1] > y):
        pygame.draw.rect(window, active_color, (x, y, width, height))
        if (click[0] == 1 and action != None):
            if (action == 'human'):
                play(classifier=fruit_classifier)
            elif (action == 'ai'):
                play(player=ai_player, classifier=fruit_classifier)
            pygame.quit()
            quit()
    else:
        pygame.draw.rect(window, inactive_color, (x, y, width, height))
    message_to_screen(msg, (x + (width/2)), (y + (height/2)), 20)

        
def start_game(ai=ai_player, classifier=None):

    global ai_player
    ai_player = ai

    global fruit_classifier
    fruit_classifier = classifier

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        window.blit(bg, (0,0))
        message_to_screen('FRUIT CATCHER', window.get_width()/2, window.get_height()/2, 50)
        button('Human', 100, 450, 75, 50, dark_green, bright_green, 'human')
        button('AI', 200, 450, 75, 50, dark_blue, bright_blue, 'ai')
        button('Quit', 300, 450, 75, 50, dark_red, bright_red, 'quit')
        pygame.display.update()
        clock.tick(15)


def redraw(basket, items, score):
    window.blit(bg, (0,0))
    for item in items:
        item.draw(window)
    basket.draw(window)
    message_to_screen(f'Score: {score}', 50, 30, 20)    
    pygame.display.update()


def play(player=human_player, classifier=None, draw=True, fruit_limit=100):
    fruit_drop_rate = 30
    bomb_drop_rate = 100
    fruit_drop_count = 0
    fruit_drop_timer = 0
    bomb_drop_timer = 0

    score = 0
    items = []
    basket = Basket(window.get_width() / 2 - 75, window.get_height() - 150)

    play = True
    while play:
        if draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False

        state = extract_state(basket, items, classifier)

        selected_play = player(state)
        if selected_play == -1:
            basket.x = max(0, basket.x - basket.vel)
        elif selected_play == 1:
            basket.x = min(window.get_width() - basket.w, basket.x + basket.vel)   

        fruit_drop_timer += 1
        bomb_drop_timer += 1

        if fruit_drop_count >= fruit_limit and not items:
            play = False

        if fruit_drop_timer == fruit_drop_rate and fruit_drop_count < fruit_limit:
            fruit_x = random.randrange(0, window.get_width() - 100)
            fruit_type = random.choice(fruit_ids)
            items.append(Item(fruit_x, 0, fruit_type))
            fruit_drop_timer = 0
            fruit_drop_count += 1
        if bomb_drop_timer == bomb_drop_rate and fruit_drop_count < fruit_limit:
            bomb_x = random.randrange(0, window.get_width() - 100)
            bomb_type = random.choice(bomb_ids)
            items.append(Item(bomb_x, 0, bomb_type))
            bomb_drop_timer = 0


        for item in items[:]:
            item.y += item.vel
            if item.y > window.get_height():
                items.remove(item)
                continue
            if (item.x + item.w / 3 >= basket.x) and (item.x + 2 * item.w / 3 <= basket.x + basket.w):
                if item.y + item.h > basket.y + basket.h / 3 and item.y + item.h < basket.y + basket.h / 2:
                    items.remove(item)
                    if item_types[item.id]['is_fruit'] == -1:
                        play = False
                    else:
                        score += 1

        if draw:
            redraw(basket, items, score)
            clock.tick(60)

    return score


def get_score(player, classifier=None):
    return play(player=player, classifier=classifier, draw=False)