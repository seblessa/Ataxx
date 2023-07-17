import random


def miniMax(game, depth):
    return (0, 0), 0, 1


def random_move(game):
    possible_moves = game.possible_moves()
    return random.choice(possible_moves[0])
