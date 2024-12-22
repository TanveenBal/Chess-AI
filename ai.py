import math
import random
from move import Move
from square import Square

class ChessAI:
    def __init__(self, max_color, min_color):
        self.color = max_color
        self.max_color = max_color
        self.min_color = min_color
        self.start_depth = 3

    def evaluate(self, board, eval_color):
        if eval_color == "white":
            return board.white_score - board.black_score
        else:
            return board.black_score - board.white_score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.game_over():
            color_eval = "white" if maximizing_player else "black" # May need to swap if else
            return None, self.evaluate(board, color_eval)
        best_move = None
        
        if maximizing_player:
            moves = board.get_moves(self.max_color)
            if moves is None:
                color_eval = "white" if maximizing_player else "black"
                return None, self.evaluate(board, color_eval)
            
            max_eval = -math.inf
            for move in moves:
                board.move(move.initial.piece, move)
                current_eval = self.minimax(board, depth - 1, alpha, beta, False)[1]
                board.undo_move()
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            moves = board.get_moves(self.min_color)
            if moves is None:
                color_eval = "white" if maximizing_player else "black"
                return None, self.evaluate(board, color_eval)
            
            min_eval = math.inf
            for move in moves:
                board.move(move.initial.piece, move)
                current_eval = self.minimax(board, depth - 1, alpha, beta, True)[1]
                board.undo_move()
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def find_best_move(self, board):
        return self.minimax(board, self.start_depth, -math.inf, math.inf, True)[0]
