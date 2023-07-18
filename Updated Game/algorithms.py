import random


# Chooses the best move based on which
# move is going to place more pieces on the board
# formula: player1_pieces - player2_pieces
# player 1 is the maximizing player
# player 2 is the minimizing player
def heuristic(game):
    return len(game.player1_pieces) - len(game.player2_pieces)


# return the selecting piece, the destination and the score
def minimax(game, depth, maximizing_player):
    if depth == 0 or game.game_over():
        return None, None, heuristic(game)

    if maximizing_player:
        max_score = float('-inf')
        best_move = None
        selected = None
        for successor_t in game.successors():
            successor, selected, played = successor_t
            _, _, score = minimax(successor, depth - 1, False)
            if score > max_score:
                max_score = score
                best_move = played
        return selected, best_move, max_score
    else:
        min_score = float('inf')
        best_move = None
        selected = None
        for successor_t in game.successors():
            successor, selected, played = successor_t
            _, _, score = minimax(successor, depth - 1, True)
            if score < min_score:
                min_score = score
                best_move = played
        return selected, best_move, min_score


def random_move(game):
    walkers, jumpers = game.possible_moves()

    if random.randint(0, 1) == 0:
        move = random.choice(walkers)
        return move[0], move[1][0], move[1][1]
    else:
        move = random.choice(jumpers)
        return move[0], move[1][0], move[1][1]
