from tkinter import *
import numpy as np
import copy
import random as r

b_w = """
  ___ _                   _           _ _ _
 | _ ) |_  _ ___  __ __ _(_)_ _  ___ | | | |
 | _ \ | || / -_) \ V  V / | ' \(_-< |_|_|_|
 |___/_|\_,_\___|  \_/\_/|_|_||_/__/ (_|_|_)

"""

r_w = """
  ___        _          _           _ _ _
 | _ \___ __| | __ __ _(_)_ _  ___ | | | |
 |   / -_) _` | \ V  V / | ' \(_-< |_|_|_|
 |_|_\___\__,_|  \_/\_/|_|_||_/__/ (_|_|_)

"""

NB = 7
size_of_board = 600
size_of_square = size_of_board / NB
symbol_size = (size_of_square * 0.75 - 10) / 2
symbol_thickness = 20
blue_color = '#496BAB'
red_color = '#F33E30'
possible_moves_global = []
position_global = []
bool = False
origin_pos = []
moves_blue_global = []
moves_red_global = []
blue_pieces = []
red_pieces = []
board2 = []
best_move = None


class ataxx():
    def __init__(self):
        self.window = Tk()
        self.window.title('Ataxx')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, background="white")
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.board = np.zeros(shape=(NB, NB))
        self.board[0][0] = 2
        self.board[0][NB - 1] = 1
        self.board[NB - 1][NB - 1] = 1
        self.board[NB - 1][0] = 2
        self.player_blue_turn = True
        self.game_ended = False
        self.mode1 = 0
        self.mode2 = 0
        self.init_draw_board()

    def mainloop(self):
        self.window.mainloop()

    # ----------------DESENHO DO TABULEIRO---------------------------------------------------------------------------------------------------------

    def init_draw_board(self):
        # Desenha a board inicial, com 2 peças de cada cor nos cantos
        self.canvas.delete("all")
        for i in range(NB - 1):
            self.canvas.create_line((i + 1) * size_of_square, 0, (i + 1) * size_of_square, size_of_board)
        for i in range(NB - 1):
            self.canvas.create_line(0, (i + 1) * size_of_square, size_of_board, (i + 1) * size_of_square)
        self.canvas.create_oval(size_of_square / 2 - symbol_size, size_of_square / 2 - symbol_size,
                                size_of_square / 2 + symbol_size, size_of_square / 2 + symbol_size,
                                width=symbol_thickness, outline=red_color,
                                fill=red_color)
        self.canvas.create_oval(size_of_board - size_of_square / 2 - symbol_size,
                                size_of_board - size_of_square / 2 - symbol_size,
                                size_of_board - size_of_square / 2 + symbol_size,
                                size_of_board - size_of_square / 2 + symbol_size,
                                width=symbol_thickness, outline=blue_color,
                                fill=blue_color)
        self.canvas.create_oval(size_of_square / 2 - symbol_size, size_of_board - size_of_square / 2 - symbol_size,
                                size_of_square / 2 + symbol_size, size_of_board - size_of_square / 2 + symbol_size,
                                width=symbol_thickness, outline=blue_color,
                                fill=blue_color)
        self.canvas.create_oval(size_of_board - size_of_square / 2 - symbol_size, size_of_square / 2 - symbol_size,
                                size_of_board - size_of_square / 2 + symbol_size, size_of_square / 2 + symbol_size,
                                width=symbol_thickness, outline=red_color,
                                fill=red_color)

    def update_board(self, x, y, origin):
        # após um movimento ser valido pelo jogo, a funcao dá
        # update à matriz que representa o tabuleiro, transformando
        # qualquer quadrado adjacente ao quadrado de destino que
        # esteja ocupado para a cor do jogador.
        # se a peça "saltar", chama a funcao draw_whitespace para desenhar
        # um quadrado branco no local de origem da peça e mete essa posicao
        # na board a 0, "apagando" a peça
        for i in range(max(0, x - 1), min(NB, x + 2)):
            for j in range(max(0, y - 1), min(NB, y + 2)):
                if not self.is_square_clear([i, j]):
                    if self.player_blue_turn:
                        self.draw_blue([i, j])
                    else:
                        self.draw_red([i, j])
                    self.board[i][j] = self.board[x][y]
        if x - origin[0] == 2 or y - origin[1] == 2 or x - origin[0] == -2 or y - origin[1] == -2:
            self.board[origin[0]][origin[1]] = 0
            pos = self.convert_logical_to_grid_position(origin)
            self.draw_whitespace(pos)
        self.score()
        self.all_moves()
        self.player_blue_turn = not self.player_blue_turn
        moves_blue_global = []
        moves_red_global = []

    def update_board2(self, board, x, y, origin):
        for i in range(max(0, x - 1), min(NB, x + 2)):
            for j in range(max(0, y - 1), min(NB, y + 2)):
                if not board[pos[0]][pos[1]] == 0:
                    board[i][j] = board[x][y]
        if x - origin[0] == 2 or y - origin[1] == 2 or x - origin[0] == -2 or y - origin[1] == -2:
            board[origin[0]][origin[1]] = 0

    def all_moves(self):
        # Verifica todos os movimentos possivies numa dada posição
        # Se um dos jogadores não estiver moves, chama a funcao no_moves
        global moves_blue_global
        global moves_red_global
        global blue_pieces
        global red_pieces
        for i in range(NB):
            for j in range(NB):
                if self.board[i][j] == 1:
                    moves_blue_global.append(self.possible_moves([i, j]))
                    blue_pieces.append([i, j])
                elif self.board[i][j] == 2:
                    moves_red_global.append(self.possible_moves([i, j]))
                    red_pieces.append([i, j])
        if len(moves_blue_global[0]) == 0:
            self.no_moves(1)
        elif len(moves_red_global[0]) == 0:
            self.no_moves(2)

    def no_moves(self, player):
        # Preenche o tabuleiro se um dos jogadores já não tiver movimentos
        if player == 1:
            for i in range(NB):
                for j in range(NB):
                    if self.board[i][j] == 0:
                        self.board[i][j] = 2
                        self.draw_red([i, j])
        elif player == 2:
            for i in range(NB):
                for j in range(NB):
                    if self.board[i][j] == 0:
                        self.board[i][j] = 1
                        self.draw_blue([i, j])
        self.score()

    def execute_move(self, move, origin, player):

        # altera na board o destino da peca que foi jogado para o valor
        # correspondente dessa peca(1 se azul, 2 se vermelho)
        # chama a funcao update_board para completar a execucao do movimento

        self.board[move[0]][move[1]] = player
        self.update_board(move[0], move[1], origin)

    def is_square_clear(self, pos):
        if not np.array_equal(pos, []):
            return self.board[pos[0]][pos[1]] == 0

    def valid_move(self, logical_pos):
        return self.is_square_clear(logical_pos)

    def possible_moves(self, move):
        # dado uma certa peça que foi seleciona, devolve uma lista
        # com todos os movimentos possiveis dessa peça
        possible_moves = []
        for i in range(max(0, move[0] - 2), min(NB, move[0] + 3)):
            for j in range(max(0, move[1] - 2), min(NB, move[1] + 3)):
                if self.is_square_clear([i, j]):
                    possible_moves.append([i, j])
        return possible_moves

    def score(self):
        # Calcula o resultado do jogo ao contar as peças de cada jogador
        # Se um dos jogadores não tiver peças ou o tabuleiro estiver cheio, chama a função game_is_over
        cont_blue = 0
        cont_red = 0
        cheio = True
        for i in range(NB):
            for j in range(NB):
                if self.board[i][j] == 1:
                    cont_blue += 1
                elif self.board[i][j] == 2:
                    cont_red += 1
                if self.board[i][j] == 0:
                    cheio = False
        print("Blue score= ", cont_blue)
        print("Red score= ", cont_red)
        print("------------------------")
        self.window.title("Ataxx - Red : %d vs %d : Blue" % (cont_red, cont_blue))
        if cont_blue == 0:
            self.game_is_over(cont_red, cont_blue)
        elif cont_red == 0:
            self.game_is_over(cont_red, cont_blue)
        elif cheio:
            self.game_is_over(cont_red, cont_blue)

    def game_is_over(self, red, blue):
        # Demonstra o ecrã final e o vencedor
        print("Blue score= ", blue)
        print("Red score= ", red)
        print("")
        self.game_ended = True
        if blue > red:
            print("")
            print(b_w)
            # Create a canvas object
            definirvenc = Canvas(self.window, width=625, height=65, bg="SteelBlue1")
            # Add a text in Canvas
            definirvenc.create_text(325, 25, text="        BLUE WINS          ", fill="black",
                                    font=('Helvetica 15 bold'))
            # definirvenc.create_text(325, 50, text="CARREGUE PARA VOLTAR AO MENU", fill="black", font=('Helvetica 15 bold'))
            definirvenc.pack()
        else:
            print("")
            print(r_w)
            # Create a canvas object
            definirvenc = Canvas(self.window, width=625, height=65, bg="OrangeRed3")
            # Add a text in Canvas
            definirvenc.create_text(325, 25, text="        RED WINS          ", fill="black",
                                    font=('Helvetica 15 bold'))
            # definirvenc.create_text(325, 50, text="CARREGUE PARA VOLTAR AO MENU", fill="black", font=('Helvetica 15 bold'))
            definirvenc.pack()
        print("")

    # ----------------------TRANSFORMAR EM MATRIZ PARA APLICAR REGRAS-------------------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # logical_position = grid value on the board
    # grid_position = actual pixel values of the center of the grid

    def convert_logical_to_grid_position(self, logical_pos):
        logical_pos = np.array(logical_pos, dtype=int)
        return np.array((size_of_square) * logical_pos + size_of_square / 2)

    def convert_grid_to_logical_position(self, grid_pos):
        grid_pos = np.array(grid_pos)
        return np.array(grid_pos // size_of_square, dtype=int)

    # -----------------------DESENHAR PECAS----------------------------------------
    def draw_whitespace(self, grid_pos):
        # desenha o quadrado branco no local dado
        self.canvas.create_rectangle(grid_pos[0] - symbol_size, grid_pos[1] - symbol_size,
                                     grid_pos[0] + symbol_size, grid_pos[1] + symbol_size,
                                     width=symbol_thickness, outline="white",
                                     fill="white")

    def draw_blue(self, logical_pos):
        logical_pos = np.array(logical_pos)
        grid_pos = self.convert_logical_to_grid_position(logical_pos)
        self.canvas.create_oval(grid_pos[0] - symbol_size, grid_pos[1] - symbol_size,
                                grid_pos[0] + symbol_size, grid_pos[1] + symbol_size,
                                width=symbol_thickness, outline=blue_color,
                                fill=blue_color)

    def draw_red(self, logical_pos):
        logical_pos = np.array(logical_pos)
        grid_pos = self.convert_logical_to_grid_position(logical_pos)
        self.canvas.create_oval(grid_pos[0] - symbol_size, grid_pos[1] - symbol_size,
                                grid_pos[0] + symbol_size, grid_pos[1] + symbol_size,
                                width=symbol_thickness, outline=red_color,
                                fill=red_color)

    def draw_possible_moves(self, possible_moves):
        # desenha no ecrâ todos os moves possiveis de uma
        # determinada peça, utilizando circulos cinzentos para
        # representar os moves possiveis
        moves = [0] * len(possible_moves)
        for i in range(len(possible_moves)):
            moves[i] = self.convert_logical_to_grid_position(possible_moves[i])
            self.canvas.create_oval(moves[i][0] - symbol_size, moves[i][1] - symbol_size,
                                    moves[i][0] + symbol_size, moves[i][1] + symbol_size,
                                    width=symbol_thickness, outline="gray", fill="gray", tags="possible")

    def clear_possible_moves(self):
        # limpa do ecrã os moves possiveis(os circulos cinzentos)
        self.canvas.delete("possible")

    def moves1(self, board, player):
        # calcula todos os movimentos possiveis
        moves = []
        moves_final = []
        for i in range(NB):
            for j in range(NB):
                if player == 1:
                    if board[i][j] == 1:
                        moves.append(self.possible_moves2(board, [i, j]))
                else:
                    if board[i][j] == 2:
                        moves.append(self.possible_moves2(board, [i, j]))
        for element in moves:
            for i in element:
                if i not in moves_final:
                    moves_final.append(i)
        return moves_final

    def minimaxao(self, board, depth, alpha, beta, maxi, player):
        global best_move
        moves = []
        best_move = None
        if depth == 0:
            return self.evaluate(board)

        if maxi:
            maxEval = float('-inf')
            best_move = None
            moves = self.moves1(board, player)
            for move in moves:
                evaluation = self.minimaxao(board, depth - 1, alpha, beta, False, 1 if player == 2 else 2)
                if evaluation > maxEval:
                    best_move = move
                    maxEval = evaluation
            return maxEval
        else:
            minEval = float('-inf')
            best_move = None
            moves = self.moves1(board, player)
            for move in moves:
                evaluation = self.minimaxao(board, depth - 1, alpha, beta, True, 1 if player == 2 else 2)
                if evaluation < minEval:
                    minEval = evaluation
            return minEval

    def possible_moves2(self, board, move):
        possible_moves = []
        for i in range(max(0, move[0] - 2), min(NB, move[0] + 3)):
            for j in range(max(0, move[1] - 2), min(NB, move[1] + 3)):
                if board[i][j] == 0:
                    possible_moves.append([i, j])
        return possible_moves

    def evaluate(self, board):
        # Heurística
        red = 0
        blue = 0
        for i in range(NB):
            for j in range(NB):
                if board[i][j] == 1:
                    blue += 1
                else:
                    red += 1

        return (red - blue)

    def random(self):
        # Escolhe um move aleatório para executar
        if not self.game_ended:
            moves_total = {}
            pieces = []
            self.all_moves()
            global position_global
            global origin_pos
            global blue_pieces
            global red_pieces
            if self.player_blue_turn:
                for piece in blue_pieces:
                    piece2 = (piece[0], piece[1])
                    moves = self.possible_moves(piece)
                    moves_total[piece2] = moves
                for key in moves_total.keys():
                    pieces.append(key)
                i = r.randint(0, len(pieces) - 1)
                random_piece = pieces[i]
                moves = moves_total[random_piece]
                while np.array_equal(moves, []):
                    i = r.randint(0, len(pieces) - 1)
                    random_piece = pieces[i]
                    moves = moves_total[random_piece]
                i = r.randint(0, len(moves) - 1)
                random_move = moves[i]
                origin_pos = random_piece
                position_global = random_move
            elif not self.player_blue_turn:
                for piece in red_pieces:
                    piece2 = (piece[0], piece[1])
                    moves = self.possible_moves(piece)
                    moves_total[piece2] = moves
                for key in moves_total.keys():
                    pieces.append(key)
                i = r.randint(0, len(pieces) - 1)
                random_piece = pieces[i]
                moves = moves_total[random_piece]
                while np.array_equal(moves, []):
                    i = r.randint(0, len(pieces) - 1)
                    random_piece = pieces[i]
                    moves = moves_total[random_piece]
                i = r.randint(0, len(moves) - 1)
                random_move = moves[i]
                origin_pos = random_piece
                position_global = random_move
            bool = True
            self.click2()

    # -----------------------INPUT---------------------------------

    def click(self, event):

        # ao clicar pela primeira vez numa peça,
        # altera o bind do Button 1 para second_click,
        # funcao que regista o segundo click do jogador
        # se a peça que foi clicada for uma peça de um jogador,
        # chama as funçoes possible_moves e draw_possible_moves
        # para mostrar no ecra os moves possiveis dessa peça
        if self.game_ended: return
        if self.mode1 == 1 and self.mode2 == 1:
            self.ai_vs_ai()
            pass
        grid_pos = [event.x, event.y]
        logical_pos = self.convert_grid_to_logical_position(grid_pos)
        global origin_pos
        global possible_moves_global
        origin_pos = logical_pos
        if self.board[logical_pos[0]][logical_pos[1]] == 1 and self.player_blue_turn:
            possible_moves_global = self.possible_moves(logical_pos)
            if not np.array_equal(possible_moves_global, []):
                self.window.bind("<Button-1>", self.second_click)
            self.draw_possible_moves(possible_moves_global)
        elif self.board[logical_pos[0]][logical_pos[1]] == 2 and not self.player_blue_turn:
            possible_moves_global = self.possible_moves(logical_pos)
            if not np.array_equal(possible_moves_global, []):
                self.window.bind("<Button-1>", self.second_click)
            self.draw_possible_moves(possible_moves_global)

    def second_click(self, event):
        # ao clicarmos uma segunda vez no ecrã, esta função
        # é executada. Regista a posição do click e compara
        # se o local onde clicamos faz parte da lista dos possible_moves.
        # Se True, chama a função click2.
        global bool
        grid_pos = [event.x, event.y]
        logical_pos = self.convert_grid_to_logical_position(grid_pos)
        global possible_moves_global
        possible_moves_global = np.array(possible_moves_global, dtype=int)
        for element in possible_moves_global:
            if np.array_equal(logical_pos, element):
                global position_global
                position_global = logical_pos
                bool = True
        bool = True
        self.click2()
        possible_moves_global = []
        position_global = []

    def click2(self):
        # Se um move for válido, desenha a peça no ecrã e dá update à board
        global position_global
        global bool
        global origin_pos
        if self.player_blue_turn:
            player = 1
        else:
            player = 2
        if self.valid_move(position_global):
            if self.player_blue_turn and self.board[origin_pos[0]][origin_pos[1]] == 1:
                self.draw_blue(position_global)
                self.execute_move(position_global, origin_pos, player)
            elif not self.player_blue_turn and self.board[origin_pos[0]][origin_pos[1]] == 2:
                self.draw_red(position_global)
                self.execute_move(position_global, origin_pos, player)
        self.clear_possible_moves()
        if not self.player_blue_turn and self.mode1 == 1 and self.mode2 == 0:
            position_global = []
            origin_pos = []
            self.random()
        if self.mode1 == 1 and self.mode2 == 1:
            self.ai_vs_ai()
        elif self.mode1 == 2:
            boardzao = copy.deepcopy(self.board)
            x = self.minimaxao(boardzao, 1, float('-inf'), float('inf'), False, 1)
            global best_move
            position_global = best_move
            self.click2()
        self.window.bind("<Button-1>", self.click)

    def ai_vs_ai(self):
        # chamada quando o modo de jogo é AI_easy vs AI_easy
        self.random()


def PvsP():
    game = ataxx()
    game.mainloop()
    start_menu()


def PvsAI():
    print("")
    print("Choose the difficulty:")
    print("(1) Easy")
    print("(2) Medium")
    print("(3) Hard")
    print("(4) Return")
    print("")
    n = int(input("Option:"))
    while (n != 1 and n != 2 and n != 3 and n != 4):
        print("------------------------------------------------------------")
        print("")
        print("Invalid option")
        print("")
        print("Choose the difficulty:")
        print("(1) Easy")
        print("(2) Medium")
        print("(3) Hard")
        print("(4) Return")
        print("")
        n = int(input("Option:"))
        print("")

    if (n == 4):
        start_menu()
    game = ataxx()
    game.mode1 = n
    game.mainloop()
    start_menu()


def AIvsAI():
    difficulty = {1: 'Easy', 2: 'Medium', 3: 'Hard'}

    print("")
    print("Choose the difficulty of the first AI:")
    print("(1) " + difficulty[1])
    print("(2) " + difficulty[2])
    print("(3) " + difficulty[3])
    print("")
    n1 = int(input("Option:"))
    while (n1 != 1 and n1 != 2 and n1 != 3):
        print("------------------------------------------------------------")
        print("")
        print("Invalid option")
        print("")
        print("Choose the difficulty:")
        print("(1) " + difficulty[1])
        print("(2) " + difficulty[2])
        print("(3) " + difficulty[3])
        print("")
        n1 = int(input("Option:"))
        print("")

    print("")
    print("Choose the difficulty of the second AI:")
    print("(1) " + difficulty[1])
    print("(2) " + difficulty[2])
    print("(3) " + difficulty[3])
    print("")
    n2 = int(input("Option:"))
    while (n2 != 1 and n2 != 2 and n2 != 3):
        print("------------------------------------------------------------")
        print("")
        print("Invalid option")
        print("")
        print("Choose the difficulty:")
        print("(1) " + difficulty[1])
        print("(2) " + difficulty[2])
        print("(3) " + difficulty[3])
        print("")
        n2 = int(input("Option:"))

    print("Choose one option:")
    print("(1) " + difficulty[n1] + " vs " + difficulty[n2])
    print("(2) Return to menu")
    print("")
    op = input("Option: ")
    while (op != "1" and op != "2"):
        print("------------------------------------------------------------")
        print("")
        print("Invalid option")
        print("")
        print("Choose one option:")
        print("(1) " + difficulty[n1] + " vs " + difficulty[n2])
        print("(2) Return")
        print("")
        op = input("Option: ")

    if (op == "2"):
        start_menu()

    game = ataxx()
    game.mode1 = n1
    game.mode2 = n2
    game.mainloop()

    start_menu()


def start_menu():
    print("")
    print("|-----------------------------------------------------------|")
    print("|      ___   .__________.     ___      ___   ___ ___   ___  |")
    print("|     /   \  |           |   /   \     \  \ /  / \  \ /  /  |")
    print("|    /  ^  \ `---|  |---`   /  ^  \     \  V  /   \  V  /   |")
    print("|   /  /_\  \    |  |      /  /_\  \     >   <     >   <    |")
    print("|  /  _____  \   |  |     /  _____  \   /  .  \   /  .  \   |")
    print("| /__/     \__\  |__|    /__/     \__\ /__/ \__\ /__/ \__\  |")
    print("|-----------------------------------------------------------|")
    print("")
    print("Choose one of the following options:")
    print("")
    print("(1) Player vs Player")
    print("(2) Player vs AI")
    print("(3) AI vs AI")
    print("(4) Exit")
    print("")
    escolha = input("Option: ")
    print("")

    while (escolha != "1" or escolha != "2" or escolha != "3" or escolha != "4"):
        if escolha == "1":
            print("--------------------------------------")
            print("")
            print("Player vs Player")
            print("")
            PvsP()
            break

        elif escolha == "2":
            print("----------------------------------")
            print("")
            print("Player vs AI")
            print("")
            PvsAI()
            break

        elif escolha == "3":
            print("----------------------------------")
            print("")
            print("AI vs AI")
            print("")
            AIvsAI()
            break
        elif escolha == "4":
            quit()
        else:
            print("------------------------------------------------------------")
            print("")
            print("Invalid option")
            print("")
            print("|-----------------------------------------------------------|")
            print("|      ___   .__________.     ___      ___   ___ ___   ___  |")
            print("|     /   \  |           |   /   \     \  \ /  / \  \ /  /  |")
            print("|    /  ^  \ `---|  |---`   /  ^  \     \  V  /   \  V  /   |")
            print("|   /  /_\  \    |  |      /  /_\  \     >   <     >   <    |")
            print("|  /  _____  \   |  |     /  _____  \   /  .  \   /  .  \   |")
            print("| /__/     \__\  |__|    /__/     \__\ /__/ \__\ /__/ \__\  |")
            print("|-----------------------------------------------------------|")
            print("")
            print("")
            print("Choose one of the following options:")
            print("")
            print("(1) Player vs Player")
            print("(2) Player vs AI")
            print("(3) AI vs AI")
            print("(4) Exit")
            print("")
            escolha = input("Option: ")
            print("")


start_menu()
