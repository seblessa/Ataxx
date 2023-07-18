from copy import copy


def create_game():
    game = [["-"] * 7 for _ in range(7)] # Create a 7x7 board

    game[0][0] = game[0][6] = "1"
    game[6][0] = game[6][6] = "2"

    return game


class Game:
    def __init__(self, algorithm=None, winner=None, player1_pieces=None, player2_pieces=None):
        self.game = create_game()
        self.turn = "1"
        self.algorithm = algorithm
        self.winner = winner
        self.player1_pieces = player1_pieces if player1_pieces is not None else [(0, 0), (0, 6)]
        self.player2_pieces = player2_pieces if player2_pieces is not None else [(6, 0), (6, 6)]

    def __copy__(self):
        return Game(
            algorithm=self.algorithm,
            winner=self.winner,
            player1_pieces=copy(self.player1_pieces),
            player2_pieces=copy(self.player2_pieces)
        )

    def __str__(self):
        string_game = ""
        for row in self.game:
            string_game += " ".join(row) + "\n"
        return string_game

    def selecting_piece(self, i, j):
        if self.turn == "1":
            return (i, j) in self.player1_pieces
        else:
            return (i, j) in self.player2_pieces

    def change_turn(self):
        self.turn = "2" if self.turn == "1" else "1"

    def walk(self, i, j):
        successors = []
        for n in range(-1, 2):
            for m in range(-1, 2):
                if n != 0 or m != 0:
                    successors.extend(self.append_moves(n, m, i, j))
        return successors

    def jump(self, i, j):
        successors = []
        for n in range(-2, 3):
            for m in range(-2, 3):
                if n != 0 or m != 0 or n != 1 or m != 1 or n != -1 or m != -1:
                    successors.extend(self.append_moves(n, m, i, j))
        return successors

    def append_moves(self, n, m, i, j):
        successors = []
        if 0 <= i + n < 7 and 0 <= j + m < 7:
            if self.game[i + n][j + m] == "-":
                successors.append((i + n, j + m))
        return successors

    def successors(self):
        successors = []
        walkers, jumpers = self.possible_moves()

        for walker in walkers:
            selected, piece = walker
            game_copy = self.__copy__()
            game_copy.game[piece[0]][piece[1]] = self.turn
            game_copy.transform_surrondings(piece[0], piece[1])
            successors.append((game_copy, selected, piece))

        for jumper in jumpers:
            selected, piece = jumper
            game_copy = self.__copy__()
            game_copy.game[piece[0]][piece[1]] = self.turn
            game_copy.game[selected[0]][selected[1]] = "-"
            game_copy.transform_surrondings(piece[0], piece[1])
            successors.append((game_copy, selected, piece))

        return successors

    def possible_moves(self):
        walkers = []
        jumpers = []
        if self.turn == "1":
            for piece in self.player1_pieces:
                jumpers.extend((piece, successor) for successor in self.jump(*piece))
                walkers.extend((piece, successor) for successor in self.walk(*piece))
        else:
            for piece in self.player2_pieces:
                jumpers.extend((piece, successor) for successor in self.jump(*piece))
                walkers.extend((piece, successor) for successor in self.walk(*piece))

        moves = jumpers, walkers
        return moves

    def transform_surrondings(self, i, j):
        for n in range(-1, 2):
            for m in range(-1, 2):
                if 0 <= i + n < 7 and 0 <= j + m < 7:
                    if self.turn == "1":
                        if self.game[i + n][j + m] == "2":
                            self.game[i + n][j + m] = "1"
                            self.player1_pieces.append((i + n, j + m))
                            if (i + n, j + m) in self.player2_pieces:
                                self.player2_pieces.remove((i + n, j + m))
                    else:
                        if self.game[i + n][j + m] == "1":
                            self.game[i + n][j + m] = "2"
                            self.player2_pieces.append((i + n, j + m))
                            if (i + n, j + m) in self.player1_pieces:
                                self.player1_pieces.remove((i + n, j + m))

    def move(self, selected, i, j):
        jumpers, walkers = self.possible_moves()

        walkers = [walker[1] for walker in walkers]
        jumpers = [jumper[1] for jumper in jumpers]

        if (i, j) in walkers:
            if (i, j) != selected:
                self.game[i][j] = self.turn
                if self.turn == "1":
                    self.player1_pieces.append((i, j))
                else:
                    self.player2_pieces.append((i, j))
            self.transform_surrondings(i, j)
            self.change_turn()
            return True

        elif (i, j) in jumpers:
            self.game[i][j] = self.turn
            self.game[selected[0]][selected[1]] = "-"
            if self.turn == "1":
                self.player1_pieces.append((i, j))
                self.player1_pieces.remove((selected[0], selected[1]))
            else:
                self.player2_pieces.append((i, j))
                self.player2_pieces.remove((selected[0], selected[1]))
            self.transform_surrondings(i, j)
            self.change_turn()
            return True

        else:
            return False

    def game_over(self):
        successors = self.possible_moves()
        if len(successors[0]) == 0 and len(successors[1]) == 0:
            if len(self.player1_pieces) > len(self.player2_pieces):
                self.winner = "1"
            else:
                self.winner = "2"
            return True
        return False
