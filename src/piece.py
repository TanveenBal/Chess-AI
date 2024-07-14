from math import inf
from square import Square
from move import Move
from copy import deepcopy
from const import *

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        self.en_passant = False
        value_sign = 1 if color == "white" else -1
        self.check = False
        self.value = value_sign * value
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = f"../assets/pieces/{size}px/{self.color}_{self.name}.png"

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

    def create_move(self, init_row, init_col, fin_row, fin_col, board, bool=True):
        initial = Square(init_row, init_col, board.squares[init_row][init_col].piece)
        final = Square(fin_row, fin_col, board.squares[fin_row][fin_col].piece)
        move = Move(initial, final)
        if bool:
            if not board.in_check(self, move):
                self.add_move(move)
        else:
            self.add_move(move)

    def straight_move(self, dirs, row, col, squares, board, bool=True):
        self.check = False
        for dir in dirs:
            row_dir, col_dir = dir
            poss_row = row + row_dir
            poss_col = col + col_dir
            while Square.in_range(poss_row, poss_col):
                dest = squares[poss_row][poss_col]
                if dest.is_empty():
                    self.create_move(row, col, poss_row, poss_col, board, bool)
                elif dest.has_enemy_piece(self.color):
                    if isinstance(dest, King):
                        self.check = True
                    self.create_move(row, col, poss_row, poss_col, board, bool)
                    break
                elif dest.has_team_piece(self.color):
                    break
                poss_row = poss_row + row_dir
                poss_col = poss_col + col_dir

    def poss_move_loop(self, row, col, squares, possible_moves, board, bool=True):
        self.check = False
        for possible_move in possible_moves:
            poss_row, poss_col = possible_move
            if Square.in_range(poss_row, poss_col):
                dest = squares[poss_row][poss_col]
                if dest.is_empty_or_enemy(self.color):
                    if isinstance(dest, King):
                        self.check = True
                    self.create_move(row, col, poss_row, poss_col, board, bool)

    def __repr__(self):
        return f"Piece({self.name}, {self.color})"

class Pawn(Piece):
    def __init__(self, color):
        self.direction = -1 if color == "white" else 1
        super().__init__("pawn", color, 1.0)

    def hover_moves(self, row, col, squares, board, bool=True):
        steps = 1 if self.moved else 2
        start = row + self.direction
        end = row + (self.direction * (1 + steps))
        self.check = False
        # vertical
        for poss_row in range(start, end, self.direction):
            if Square.in_range(poss_row):
                if squares[poss_row][col].is_empty():
                    initial = Square(row, col, self)
                    final = Square(poss_row, col, squares[poss_row][col].piece)
                    move = Move(initial, final)
                    if bool:
                        if not board.in_check(self, move):
                            self.add_move(move)
                    else:
                        self.add_move(move)
                else:
                    break
            else:
                break
        # diagonal
        poss_move_row = row + self.direction
        poss_move_cols = [col - 1, col + 1]
        for poss_move_col in poss_move_cols:
            if Square.in_range(poss_move_row, poss_move_col):
                dest = squares[poss_move_row][poss_move_col]
                if squares[poss_move_row][poss_move_col].has_enemy_piece(self.color):
                    if isinstance(dest, King):
                        self.check = True
                    self.create_move(row, col, poss_move_row, poss_move_col, board, bool)

        # en passant
        r = 3 if self.color == "white" else 4
        fr = 2 if self.color == "white" else 5
        if row == r and Square.in_range(col-1, col):
            if squares[row][col-1].has_enemy_piece(self.color):
                p = squares[row][col-1].piece
                if isinstance(p, Pawn):
                    if p.en_passant:
                        self.create_move(row, col, fr, col - 1, board, bool)
        if row == r and Square.in_range(col+1, col):
            if squares[row][col+1].has_enemy_piece(self.color):
                p = squares[row][col+1].piece
                if isinstance(p, Pawn):
                    if p.en_passant:
                        self.create_move(row, col, fr, col + 1, board, bool)


class Knight(Piece):
    def __init__(self, color):
        super().__init__("knight", color, 3.0)

    def hover_moves(self, row, col, squares, board, bool=True):
        possible_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]
        self.poss_move_loop(row, col, squares, possible_moves, board, bool)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__("bishop", color, 3.00)

    def hover_moves(self, row, col, squares, board, bool=True):
        self.straight_move([
            (-1, 1),
            (-1, -1),
            (1, 1),
            (1, -1),
        ], row, col, squares, board, bool)

class Rook(Piece):
    def __init__(self, color):
        super().__init__("rook", color, 5.0)

    def hover_moves(self, row, col, squares, board, bool=True):
        self.straight_move([
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1),
        ], row, col, squares, board, bool)

class Queen(Piece):
    def __init__(self, color):
        super().__init__("queen", color, 9.0)

    def hover_moves(self, row, col, squares, board, bool=True):
        self.straight_move([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ], row, col, squares, board, bool)

class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__("king", color, inf)

    def hover_moves(self, row, col, squares, board, bool=True):
        adjs = [
            (row - 1, col + 0),
            (row - 1, col + 1),
            (row + 0, col + 1),
            (row + 1, col + 1),
            (row + 1, col + 0),
            (row + 1, col - 1),
            (row + 0, col - 1),
            (row - 1, col - 1),
        ]
        for possible_move in adjs:
            poss_row, poss_col = possible_move
            if Square.in_range(poss_row, poss_col):
                if squares[poss_row][poss_col].is_empty_or_enemy(self.color):
                    self.create_move(row, col, poss_row, poss_col, board, bool)
        if not self.moved:
            left_rook = squares[row][0].piece
            if isinstance(left_rook, Rook):
                if not left_rook.moved:
                    for c in range(1, 4):
                        if squares[row][c].has_piece():
                            break
                        if c == 3:
                            self.left_rook = left_rook
                            left_rook.create_move(row, 0, row, 3, board, bool)
                            self.create_move(row, col, row, 2, board, bool)
            right_rook = squares[row][7].piece
            if isinstance(right_rook, Rook):
                if not right_rook.moved:
                    for c in range(5, 7):
                        if squares[row][c].has_piece():
                            break
                        if c == 6:
                            self.right_rook = right_rook
                            right_rook.create_move(row, 7, row, 5, board, bool)
                            self.create_move(row, col, row, 6, board, bool)
