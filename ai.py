import math
import random

class ChessAI:
    def __init__(self, color):
        self.color = color
        self.predefined_moves_white = [
            ((6, 4), (5, 4)),
            ((7, 3), (5, 4)),
            ((6, 6), (5, 5)),
        ]
        self.predefined_moves_black = [
            ((1, 4), (2, 4)),
            ((0, 6), (2, 5)),
            ((1, 3), (3, 3)),
        ]

    def evaluate(self, board, maximizing_color):
        if maximizing_color == 'white':
            return board.white_score - board.black_score
        else:
            return board.black_score - board.white_score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.game_over:
            return None, self.evaluate(board, self.color)

        moves = board.get_moves()
        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for move in moves:
                board.move(move[0], move[1])
                current_eval = self.minimax(board, depth - 1, True, True, False)[1]
                board.undo_move()
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = math.inf
            for move in moves:
                board.move(move[0], move[1])
                current_eval = self.minimax(board, depth - 1, True, True, True)[1]
                board.undo_move()
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
                beta = min(beta, current_eval)
            return best_move, min_eval

    def find_best_move(self, board):
        if self.color == 'white':
            if self.predefined_moves_white:
                move = self.predefined_moves_white.pop(0)
                return move
        elif self.color == 'black':
            if self.predefined_moves_black:
                move = self.predefined_moves_black.pop(0)
                return move
        return self.minimax(board, 2, True, True, True)[0]
