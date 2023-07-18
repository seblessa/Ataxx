import contextlib
import sys

with contextlib.redirect_stdout(None):
    import pygame
import time
from algorithms import *

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)

RED = (255, 0, 0)
LIGHT_RED = (255, 10, 90)
LIGHTER_RED = (255, 95, 95)

YELLOW = (249, 166, 3)
LIGHT_YELLOW = (255, 255, 0)
LIGHTER_YELLOW = (241, 235, 156)


def draw_board(screen, game, selected_piece=None):
    offset = (screen.get_width() - 700) // 2

    screen.fill(LIGHTER_RED if game.turn == "1" else LIGHTER_YELLOW)

    for row in range(7):
        for col in range(7):
            x = col * 100 + 50 + offset
            y = row * 100 + 50 + offset
            pygame.draw.circle(screen, LIGHT_BLUE, (x, y), 40)

            if game.game[row][col] == "1":
                pygame.draw.circle(screen, RED, (x, y), 40)
            elif game.game[row][col] == "2":
                pygame.draw.circle(screen, YELLOW, (x, y), 40)

    if selected_piece is not None:
        x = selected_piece[1] * 100 + 50 + offset
        y = selected_piece[0] * 100 + 50 + offset
        if game.turn == "1":
            pygame.draw.circle(screen, LIGHT_RED, (x, y), 40)
        else:
            pygame.draw.circle(screen, LIGHT_YELLOW, (x, y), 40)



def play_game(game):
    pygame.init()

    # Set up the screen
    screen_width = 700  # Adjust as needed
    screen_height = 700  # Adjust as needed
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ataxx Game")

    clock = pygame.time.Clock()

    selected_piece = None

    while True:
        # Draw the board
        draw_board(screen, game, selected_piece)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Get the current position of the mouse

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // 100
                row = mouse_pos[1] // 100

                if selected_piece is None:
                    if game.selecting_piece(row, col):
                        selected_piece = (row, col)
                else:  # A piece is already selected
                    if (row, col) == selected_piece:
                        # Deselect the piece if it is selected again
                        selected_piece = None
                    elif game.move(selected_piece, row, col):
                        # Move the selected piece to the clicked position
                        selected_piece = None

        pygame.display.flip()
        clock.tick(60)

        if game.game_over():
            draw_board(screen, game, selected_piece)
            break

        if game.turn == "2":
            if game.algorithm is not None:
                if game.algorithm == 1:
                    selected_piece, pos_i, pos_j = random_move(game)
                else:  # game.algorithm == 2:
                    selected_piece, pos, score = minimax(game, 3, False)
                    pos_i, pos_j = pos

                game.move(selected_piece, pos_i, pos_j)
                selected_piece = None

    # Game over message
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, BLACK)
    text_rect = text.get_rect(center=(350, 350))
    screen.blit(text, text_rect)
    pygame.display.flip()

    time.sleep(2)  # Delay for 2 seconds
    pygame.quit()

    # Announce the winner in the terminal
    if game.winner == "1":
        print("\nPlayer 1 (RED) wins!")
    elif game.winner == "2":
        print("\nPlayer 2 (YELLOW) wins!")
