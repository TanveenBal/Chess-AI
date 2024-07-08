from board import Board
from ai import ChessAI
import pygame
import time
import sys
from pygame.locals import *
from pieces import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE
TAN = (184,139,74)
BLACK = (0, 0, 0)
BROWN = (227,193,111)
SPRITE_SIZE = SQUARE_SIZE - 25

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")
pygame.font.init()
font = pygame.font.SysFont(None, 36)

piece_images = {
    "Pawn": {
        "white": pygame.transform.scale(pygame.image.load("src/pieces/white-pawn.png"), (SPRITE_SIZE, SPRITE_SIZE)),
        "black": pygame.transform.scale(pygame.image.load("src/pieces/black-pawn.png"), (SPRITE_SIZE, SPRITE_SIZE))
    },
    "Rook": {
        "white": pygame.transform.scale(pygame.image.load("src/pieces/white-rook.png"), (SPRITE_SIZE, SPRITE_SIZE)),
        "black": pygame.transform.scale(pygame.image.load("src/pieces/black-rook.png"), (SPRITE_SIZE, SPRITE_SIZE))
    },
    "Knight": {
        "white": pygame.transform.scale(pygame.image.load("src/pieces/white-knight.png"), (SPRITE_SIZE, SPRITE_SIZE)),
        "black": pygame.transform.scale(pygame.image.load("src/pieces/black-knight.png"), (SPRITE_SIZE, SPRITE_SIZE))
    },
    "Bishop": {
        "white": pygame.transform.scale(pygame.image.load("src/pieces/white-bishop.png"), (SPRITE_SIZE, SPRITE_SIZE)),
        "black": pygame.transform.scale(pygame.image.load("src/pieces/black-bishop.png"), (SPRITE_SIZE, SPRITE_SIZE))
    },
    "Queen": {
        "white": pygame.transform.scale(pygame.image.load("src/pieces/white-queen.png"), (SPRITE_SIZE, SPRITE_SIZE)),
        "black": pygame.transform.scale(pygame.image.load("src/pieces/black-queen.png"), (SPRITE_SIZE, SPRITE_SIZE))
    },
    "King": {
        "white": pygame.transform.scale(pygame.image.load("src/pieces/white-king.png"), (SPRITE_SIZE, SPRITE_SIZE)),
        "black": pygame.transform.scale(pygame.image.load("src/pieces/black-king.png"), (SPRITE_SIZE, SPRITE_SIZE))
    }
}

class GUI(Board):
    def __init__(self):
        super().__init__()
        self.piece_sprites = pygame.sprite.Group()
        self.piece_sprite_move()
        self.selected_piece = None
        self.selected_pos = None
        self.ai = ChessAI("black")

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = TAN if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def piece_sprite_move(self):
        self.piece_sprites.empty()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece.__class__.__name__ != "Empty":
                    piece.image = piece_images[piece.__class__.__name__][piece.color]
                    piece.rect = piece.image.get_rect(topleft=(col * SQUARE_SIZE+12.5, row * SQUARE_SIZE+12.5))
                    self.piece_sprites.add(piece)

    def mouse_click(self, pos):
        row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
        if self.selected_piece is None:
            if isinstance(self.board[row][col], Piece) and not isinstance(self.board[row][col], Empty):
                self.selected_piece = self.board[row][col]
                self.selected_pos = (row, col)

    def mouse_drag(self, pos):
        if self.selected_piece is not None:
            self.selected_piece.rect.topleft = (pos[0] - SQUARE_SIZE // 2, pos[1] - SQUARE_SIZE // 2)

    def mouse_release(self, pos):
        if self.selected_piece is not None:
            row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
            if self.valid_move(self.selected_pos, (row, col)):
                self.move(self.selected_pos, (row, col))
                self.piece_sprite_move()
            else:
                self.selected_piece.rect.topleft = (
                self.selected_pos[1] * SQUARE_SIZE+12.5, self.selected_pos[0] * SQUARE_SIZE+12.5)
            self.selected_piece = None
            self.selected_pos = None

    def release(self):
        self.selected_piece.rect.topleft = (self.selected_pos[1] * SQUARE_SIZE+12.5, self.selected_pos[0] * SQUARE_SIZE+12.5)
        self.selected_piece = None
        self.selected_pos = None

    def run_game(self):
        running = True
        while running:
            if self.turn == 'black' and not self.game_over:
                best_move = self.ai.find_best_move(self.copy())
                if best_move:
                    self.move(best_move[0], best_move[1])
                    self.piece_sprite_move()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_click(event.pos)
                    elif event.button == 3:
                        self.release()
                if event.type == MOUSEMOTION:
                    self.mouse_drag(event.pos)
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    self.mouse_release(event.pos)
                if self.game_over:
                    self.game_over = False
                    time.sleep(.5)
                    self.initialize_board()
                    self.piece_sprite_move()
                    self.winner = None
                    self.turn = "white"

            screen.fill(TAN)
            self.draw_board()
            self.piece_sprites.draw(screen)
            pygame.display.flip()


if __name__ == "__main__":
    chess_board = GUI()
    chess_board.run_game()
    pygame.quit()
    sys.exit()
