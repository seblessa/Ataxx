import contextlib

with contextlib.redirect_stdout(None):
    import pygame
import time
from algorithms import *

# Colors

BLACK = (0, 0, 0)

BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)

RED = (255, 0, 0)
LIGHT_RED = (255, 95, 95)

YELLOW = (249, 166, 3)
LIGHT_YELLOW = (241, 235, 156)


def draw_board(screen, game, selected_piece=None):
    # Calculate the offset to center the board
    offset_x = (screen.get_width() - 700) // 2
    offset_y = (screen.get_height() - 700) // 2

    # Draw the background
    if game.turn == "1":
        screen.fill(LIGHT_RED)
    else:
        screen.fill(LIGHT_YELLOW)

    # Draw the circles representing empty spaces
    for row in range(7):
        for col in range(7):
            x = col * 100 + 50 + offset_x
            y = row * 100 + 50 + offset_y
            pygame.draw.circle(screen, LIGHT_BLUE, (x, y), 40)

    # Draw the player pieces
    for i in range(7):
        for j in range(7):
            if game.game[i][j] == "1":
                x = j * 100 + 50 + offset_x
                y = i * 100 + 50 + offset_y
                pygame.draw.circle(screen, RED, (x, y), 40)
            elif game.game[i][j] == "2":
                x = j * 100 + 50 + offset_x
                y = i * 100 + 50 + offset_y
                pygame.draw.circle(screen, YELLOW, (x, y), 40)

    # Draw the selected piece
    if selected_piece is not None:
        x = selected_piece[1] * 100 + 50 + offset_x
        y = selected_piece[0] * 100 + 50 + offset_y
        pygame.draw.circle(screen, BLACK, (x, y), 40)


def play_game(game):
    pygame.init()

    # Set up the screen
    screen_width = 700  # Adjust as needed
    screen_height = 700  # Adjust as needed
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ataxx Game")

    clock = pygame.time.Clock()

    game_over = False
    selected_piece = None

    while not game_over:
        # Draw the board
        draw_board(screen, game, selected_piece)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
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

        # Check if an algorithm is specified
        if game.algorithm is not None:
            if game.algorithm == 1:
                selected_piece, pos_i, pos_j = random_move(game)
            elif game.algorithm == 2:
                selected_piece, pos_i, pos_j = miniMax(game, 3)
            else:
                selected_piece, pos_i, pos_j = miniMax(game, 5)

            game.move(selected_piece, pos_i, pos_j)
            selected_piece = None
            pygame.display.flip()
            time.sleep(0.5)  # Delay for better visualization

        # Check if the game is over
        if game.game_over():
            draw_board(screen, game, selected_piece)
            game_over = True

    # Game over message
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, YELLOW)
    text_rect = text.get_rect(center=(350, 350))
    screen.blit(text, text_rect)
    pygame.display.flip()

    time.sleep(2)  # Delay for 2 seconds
    pygame.quit()

    # Announce the winner in the terminal
    if game.winner == "1":
        print("Player 1 (RED) wins!")
    elif game.winner == "2":
        print("Player 2 (YELLOW) wins!")
