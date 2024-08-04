from square import Square
from move import Move
from sound import Sound
from piece import *
from const import *

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.moves = []
        self._create()
        self._add_piece("white")
        self._add_piece("black")
        self.white_score = 39
        self.black_score = 39

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # Capture the initial state of the move
        piece_taken = self.squares[final.row][final.col].piece
        en_passant_empty = self.squares[final.row][final.col].is_empty()

        # Update score
        if piece_taken:
            if piece_taken.color == "white":
                self.white_score -= abs(piece_taken.value)
            else:
                self.black_score -= abs(piece_taken.value)

        # Update the board
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Handle en passant
        if isinstance(piece, Pawn):
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                piece_taken = self.squares[initial.row][initial.col + diff].piece
                self.squares[initial.row][initial.col + diff].piece = None
                self.moves.append(Move(initial, final, piece, piece_taken, en_passant=True,
                                       en_passant_row=initial.row, en_passant_col=initial.col + diff))
                if piece_taken:
                    if piece_taken.color == "white":
                        self.white_score -= abs(piece_taken.value)
                    else:
                        self.black_score -= abs(piece_taken.value)
            else:
                self.check_promotion(piece, final)
                self.moves.append(Move(initial, final, piece, piece_taken,
                                       promotion=(final.row == 0 or final.row == 7)))
        else:
            self.moves.append(Move(initial, final, piece, piece_taken))
        # Handle castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                self.moves.pop()
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])
                self.moves.append(Move(initial, final, piece, piece_taken=None, castle=True))

        # Update piece state
        piece.moved = True
        piece.clear_moves()

    def undo_move(self):
        if not self.moves:
            return False

        last_move = self.moves.pop()
        last_initial = last_move.initial
        last_final = last_move.final
        moved_piece = last_move.piece_moved
        piece_taken = last_move.piece_taken

        if piece_taken:
            if piece_taken.color == "white":
                self.white_score += abs(piece_taken.value)
            else:
                self.black_score += abs(piece_taken.value)

        # Move the piece back to its original position
        self.squares[last_initial.row][last_initial.col].piece = moved_piece
        self.squares[last_final.row][last_final.col].piece = piece_taken

        # Handle en passant
        if isinstance(moved_piece, Pawn):
            if last_move.en_passant:
                self.squares[last_move.en_passant_row][last_move.en_passant_col].piece = piece_taken
                self.squares[last_final.row][last_final.col].piece = None

            elif last_move.promotion:
                # Restore the pawn instead of the promoted piece
                self.squares[last_initial.row][last_initial.col].piece = Pawn(moved_piece.color)
                self.squares[last_final.row][last_final.col].piece = piece_taken
        # Handle castling
        elif isinstance(last_move.piece_moved, King):
            if last_move.castle:
                self.undo_move()

        moved_piece.moved = False
        moved_piece.clear_moves()

        return True

    def get_moves(self, color):
        all_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.calc_move(piece, row, col, bool=True)
                    all_moves.extend(piece.moves)
                    piece.clear_moves()
        return all_moves

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = deepcopy(piece)
        temp_board = deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_move(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calc_move(self, piece, row, col, bool=True):
        """ Calculates the valid moves of a specific piece in a given position """
        piece.hover_moves(row, col, self.squares, self, bool)

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def game_over(self):
        if self.moves:
            return self.squares[self.moves[-1].final.row][self.moves[-1].final.col]
        return False

    def _add_piece(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
