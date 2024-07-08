from pieces import *
import copy

class Board:
    def __init__(self):
        self.board = None
        self.initialize_board()
        self.game_over = False
        self.turn = "white"
        self.winner = None
        self.white_score = 1290
        self.black_score = 1290
        self.previous_move = {
            "src_loc": None,
            "dst_loc": None,
            "src_piece": None,
            "dst_piece": None,
            "turn": None,
            "winner": None,
            "game_over": None,
            "white_score": None,
            "black_score": None
        }

    def initialize_board(self):
        self.board = [
            [Rook("black", (0, 0)), Knight("black", (0, 1)), Bishop("black", (0, 2)), Queen("black", (0, 3)), King("black", (0, 4)), Bishop("black", (0, 5)), Knight("black", (0, 6)), Rook("black", (0, 7))],
            [Pawn("black", (1, 0)), Pawn("black", (1, 1)), Pawn("black", (1, 2)), Pawn("black", (1, 3)), Pawn("black", (1, 4)), Pawn("black", (1, 5)), Pawn("black", (1, 6)), Pawn("black", (1, 7))],
            [Empty((2, 0)), Empty((2, 1)), Empty((2, 2)), Empty((2, 3)), Empty((2, 4)), Empty((2, 5)), Empty((2, 6)), Empty((2, 7))],
            [Empty((3, 0)), Empty((3, 1)), Empty((3, 2)), Empty((3, 3)), Empty((3, 4)), Empty((3, 5)), Empty((3, 6)), Empty((3, 7))],
            [Empty((4, 0)), Empty((4, 1)), Empty((4, 2)), Empty((4, 3)), Empty((4, 4)), Empty((4, 5)), Empty((4, 6)), Empty((4, 7))],
            [Empty((5, 0)), Empty((5, 1)), Empty((5, 2)), Empty((5, 3)), Empty((5, 4)), Empty((5, 5)), Empty((5, 6)), Empty((5, 7))],
            [Pawn("white", (6, 0)), Pawn("white", (6, 1)), Pawn("white", (6, 2)), Pawn("white", (6, 3)), Pawn("white", (6, 4)), Pawn("white", (6, 5)), Pawn("white", (6, 6)), Pawn("white", (6, 7))],
            [Rook("white", (7, 0)), Knight("white", (7, 1)), Bishop("white", (7, 2)), Queen("white", (7, 3)), King("white", (7, 4)), Bishop("white", (7, 5)), Knight("white", (7, 6)), Rook("white", (7, 7))]
        ]

    def valid_move(self, src, dest):
        src_row, src_col = src
        dest_row, dest_col = dest

        src_piece = self.board[src_row][src_col]

        # Turn check
        if self.turn == "white" and src_piece.color == "black":
            return False
        elif self.turn == "black" and src_piece.color == "white":
            return False

        # Boundary check
        if src_piece is None or dest_row < 0 or dest_row >= 8 or dest_col < 0 or dest_col >= 8:
            return False

        dest_piece = self.board[dest_row][dest_col]

        # Take only enemy piece check
        if src_piece.color == "white" and dest_piece.color == "white":
            return False
        elif src_piece.color == "black" and dest_piece.color == "black":
            return False

        # Move is within set of valid possible moves
        valid_moves = src_piece.move_set()
        if dest not in valid_moves:
            return False

        # Preventing jumping over piece and special cases for different pieces
        if isinstance(src_piece, Pawn):
            direction = -1 if src_piece.color == "white" else 1
            if src_col != dest_col:
                if isinstance(self.board[dest_row][dest_col], Empty):
                    return False
            elif not isinstance(self.board[src_row + direction][src_col], Empty):
                return False
        elif isinstance(src_piece, Bishop):
            cur_row, cur_col = src_row, src_col
            direction_row = 1 if dest_row > cur_row else -1
            direction_col = 1 if dest_col > cur_col else -1
            while (cur_row + direction_row != dest_row) or (cur_col + direction_col != dest_col):
                cur_row += direction_row
                cur_col += direction_col
                if not isinstance(self.board[cur_row][cur_col], Empty):
                    return False
        elif isinstance(src_piece, Rook):
            cur_row, cur_col = src_row, src_col
            if dest_row == cur_row:
                direction_row = 0
                direction_col = 1 if dest_col > cur_col else -1
            else:
                direction_row = 1 if dest_row > cur_row else -1
                direction_col = 0
            while (cur_row + direction_row != dest_row) or (cur_col + direction_col != dest_col):
                cur_row += direction_row
                cur_col += direction_col
                if not isinstance(self.board[cur_row][cur_col], Empty):
                    return False
        elif isinstance(src_piece, Queen):
            cur_row, cur_col = src_row, src_col
            if dest_row == cur_row:
                direction_row = 0
                direction_col = 1 if dest_col > cur_col else -1
            elif dest_col == cur_col:
                direction_row = 1 if dest_row > cur_row else -1
                direction_col = 0
            else:
                direction_row = 1 if dest_row > cur_row else -1
                direction_col = 1 if dest_col > cur_col else -1

            while (cur_row + direction_row != dest_row) or (cur_col + direction_col != dest_col):
                cur_row += direction_row
                cur_col += direction_col
                if not isinstance(self.board[cur_row][cur_col], Empty):
                    return False
        return True

    def move(self, src, dest):
        src_row, src_col = src
        dest_row, dest_col = dest

        # Save previous move (for AI)
        self.previous_move["src_loc"] = src
        self.previous_move["dst_loc"] = dest
        self.previous_move["src_piece"] = self.board[src_row][src_col].copy()
        self.previous_move["dst_piece"] = self.board[dest_row][dest_col].copy()
        self.previous_move["turn"] = self.turn
        self.previous_move["winner"] = self.winner
        self.previous_move["game_over"] = self.game_over
        self.previous_move["white_score"] = self.white_score
        self.previous_move["black_score"] = self.black_score

        src_piece = self.board[src_row][src_col]

        src_piece.position = (dest_row, dest_col)

        # Update board score
        if self.board[dest_row][dest_col].color == "white":
            self.white_score -= self.board[dest_row][dest_col].weight
        elif self.board[dest_row][dest_col].color == "black":
            self.black_score -= self.board[dest_row][dest_col].weight

        # King is taken
        if isinstance(self.board[dest_row][dest_col], King):
            self.winner = self.turn
            self.game_over = True

        # Update board and special pawn case
        # self.board[dest_row][dest_col].kill()
        if (dest_row == 0 or dest_row == 7) and isinstance(src_piece, Pawn):
            if src_piece.color == "white":
                self.board[dest_row][dest_col] = Queen('white', (dest_row, dest_col))
            else:
                self.board[dest_row][dest_col] = Queen('black', (dest_row, dest_col))
        else:
            self.board[dest_row][dest_col] = self.board[src_row][src_col]
        self.board[src_row][src_col] = Empty((src_row, src_col))
        self.turn = "white" if self.turn == "black" else "black"

    def undo_move(self):
        # Undo attributes
        self.black_score = self.previous_move["black_score"]
        self.white_score = self.previous_move["white_score"]
        self.game_over = self.previous_move["game_over"]
        self.winner = self.previous_move["winner"]
        self.turn = self.previous_move["turn"]

        # Undo board and pieces
        prev_src_row, prev_src_col = self.previous_move["src_loc"]
        prev_dst_row, prev_dst_col = self.previous_move["dst_loc"]
        self.previous_move["src_piece"].position = self.previous_move["src_loc"]
        self.previous_move["dst_piece"].position = self.previous_move["dst_loc"]
        self.board[prev_src_row][prev_src_col] = self.previous_move["src_piece"]
        self.board[prev_dst_row][prev_dst_col] = self.previous_move["dst_piece"]

    def get_moves(self):
        moves = []
        for row in self.board:
            for piece in row:
                piece_moves = piece.move_set()
                src = piece.position
                piece_valid_moves = [(src, dest) for dest in piece_moves if self.valid_move(src, dest)]
                moves.extend(piece_valid_moves)
        return moves

    def display(self):
        print("\n\n")
        for row in self.board:
            print(" ".join(repr(piece) for piece in row))
        print("\n\n")

    def __copy__(self):
        new_board = Board()
        new_board.board = [[copy.copy(piece) for piece in row] for row in self.board]
        new_board.turn = self.turn
        new_board.game_over = self.game_over
        return new_board

    def __deepcopy__(self, memo):
        new_board = Board()
        new_board.board = [[copy.deepcopy(piece, memo) for piece in row] for row in self.board]
        new_board.turn = copy.deepcopy(self.turn, memo)
        new_board.game_over = copy.deepcopy(self.game_over, memo)
        return new_board

    def copy(self):
        return copy.deepcopy(self)


if __name__ == "__main__":
    chess_board = Board()
    chess_board.display()
