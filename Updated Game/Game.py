from copy import copy


def create_game():
    game = [["-"] * 7 for _ in range(7)]

    game[0][0] = game[0][6] = "1"
    game[6][0] = game[6][6] = "2"

    return game


class Game:
    def __init__(self, algorithm=None, winner=None, player1_pieces=None, player2_pieces=None):
        self.game = create_game()
        self.turn = "1"
        self.algorithm = algorithm
        self.winner = winner
        if player1_pieces is None:
            self.player1_pieces = [(0, 0), (0, 6)]
        if player2_pieces is None:
            self.player2_pieces = [(6, 0), (6, 6)]

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
                    successors.extend(self.get_moves(n, m, i, j))
        return successors

    def jump(self, i, j):
        successors = []
        for n in range(-2, 3):
            for m in range(-2, 3):
                if n != 0 or m != 0 or n != 1 or m != 1 or n != -1 or m != -1:
                    successors.extend(self.get_moves(n, m, i, j))
        return successors

    def get_moves(self, n, m, i, j):
        successors = []
        if 0 <= i + n < 7 and 0 <= j + m < 7:
            if self.game[i + n][j + m] == "-":
                successors.append((i + n, j + m))
        return successors

    def successors(self):
        walkers = []
        jumpers = []
        if self.turn == "1":
            for piece in self.player1_pieces:
                jumpers.extend(self.jump(piece[0], piece[1]))
                walkers.extend(self.walk(piece[0], piece[1]))
        else:
            for piece in self.player2_pieces:
                jumpers.extend(self.jump(piece[0], piece[1]))
                walkers.extend(self.walk(piece[0], piece[1]))

        successors = jumpers, walkers
        return successors

    def transform_surrondings(self, i, j):
        for n in range(-1, 2):
            for m in range(-1, 2):
                if 0 <= i + n < 7 and 0 <= j + m < 7:
                    if self.turn == "1":
                        if self.game[i + n][j + m] == "2":
                            self.game[i + n][j + m] = "1"
                            self.player1_pieces.append((i + n, j + m))
                            self.player2_pieces.remove((i + n, j + m))
                    else:
                        if self.game[i + n][j + m] == "1":
                            self.game[i + n][j + m] = "2"
                            self.player2_pieces.append((i + n, j + m))
                            self.player1_pieces.remove((i + n, j + m))

    def move(self, selected, i, j):
        jumpers, walkers = self.successors()

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
        successors = self.successors()
        if len(successors[0]) == 0 and len(successors[1]) == 0:
            if len(self.player1_pieces) > len(self.player2_pieces):
                self.winner = "1"
            else:
                self.winner = "2"
            return True
        return False
