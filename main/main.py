import pygame
import random
import math

from array import *

'''
This is the main.py
Here the action will happen
'''

''' TODO VVV
Zeitnahme
Punktevergabe
Speicherung
Automatisches Setzen von Kreuzen, wenn Reihe vollständig
Gewinn-Screen
Lebensanzeige
'''

# CONSTANTS
# Miscellaneous
size_of_square = 50
filled = 0
transparent = 1

# Display
display_width = 800
display_height = 800
mid_x = display_width * 0.5
mid_y = display_height * 0.5

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# PyGame
game_display = pygame.display.set_mode((display_width, display_height))
game_display.fill(white)
pygame.display.set_caption('Nonogramm')
clock = pygame.time.Clock()

# Game
time = 0
crashed = False
lives = 3
field = [[]]
numbers_x = [[]]
numbers_y = [[]]
already_drawn = []


# METHODS
# Draw Square
def square_empty(x, y, color):
    square_definition = (x, y, size_of_square, size_of_square)
    pygame.draw.rect(game_display, color, square_definition, transparent)


def square_proportions(x, y, color, width, height):
    square_definition = (x, y, width, height)
    pygame.draw.rect(game_display, color, square_definition, filled)


# Initialize field
def initiate_round():
    counter_x = 0
    counter_y = []

    for i in range(10):
        counter_y.insert(i, 0)
        numbers_y.insert(i, [])
        numbers_x.insert(i, [])

    for x in range(10):
        field.insert(x, [])
        for y in range(10):
            circle = bool(random.getrandbits(1))
            if circle:
                counter_y[y] += 1
                counter_x += 1
                if y == 9:
                    numbers_x[x].append(counter_x)
                    counter_x = 0
                if x == 9:
                    numbers_y[y].append(counter_y[y])
                    counter_y[y] = 0
            else:
                if counter_y[y] != 0:
                    numbers_y[y].append(counter_y[y])
                if counter_x != 0:
                    numbers_x[x].append(counter_x)
                counter_y[y] = 0
                counter_x = 0

            field[x].append(circle)


# Draw field
def create_field():
    for x in range(1, 11):
        text = font.render(create_string(numbers_y[x - 1]), False, (0, 0, 0))
        game_display.blit(text, (11 * size_of_square, x * size_of_square))

        for y in range(1, 11):
            text = font.render(create_string(numbers_x[y - 1]), False, (0, 0, 0))
            text = pygame.transform.rotate(text, 270)
            game_display.blit(text, (y * size_of_square, 11 * size_of_square))
            square_empty(x * size_of_square, y * size_of_square, black)


# Creation of String next to row/column
def create_string(row_or_column):
    string = ""
    for number in row_or_column:
        string += str(number)
        string += " "
    return string


# Draw X or O in square
def draw(coordinates, circle):
    x = round((coordinates[0] - 25) / 50)
    y = round((coordinates[1] - 25) / 50)

    if x < 1 or x > 10 or y < 1 or y > 10:
        return

    point = (x - 1, y - 1)

    if point in already_drawn:
        return

    already_drawn.append(point)

    correct = field[x - 1][y - 1]
    x = (x + (1 / 4)) * size_of_square
    y = y * size_of_square

    global lives

    if correct == circle:
        text = font.render('O' if circle else 'X', False, (0, 0, 0))
    else:
        text = font.render('X' if circle else 'O', False, (0, 0, 0))
        lives -= 1
        print("YOU LOST A LIVE. YOU HAVE STILL " + str(lives) + " LEFT") if lives > 0 else print("Loser")

    game_display.blit(text, (round(x), round(y)))


# PyGame initializing
pygame.init()
initiate_round()
font = pygame.font.SysFont('Comic Sans MS', 30)

# PyGame loop
while not crashed:
    for event in pygame.event.get():
        if pygame.mouse.get_pressed() == (1, 0, 0):
            draw(pygame.mouse.get_pos(), True)

        if pygame.mouse.get_pressed() == (0, 0, 1):
            draw(pygame.mouse.get_pos(), False)

        if event.type == pygame.QUIT or lives <= 0 or len(already_drawn) >= 100:
            crashed = True

    # Time increment
    time += 1

    # Creation of field
    create_field()

    pygame.display.update()
    clock.tick(60)

# PyGame quit
pygame.quit()
quit()
