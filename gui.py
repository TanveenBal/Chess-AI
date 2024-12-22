import pygame
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from const import *

class GUI:
    def __init__(self):
        self.turn = "white"
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def show_bg(self, screen):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect)

                if col == 0:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQUARE_SIZE)
                    screen.blit(lbl, lbl_pos)
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 20)
                    screen.blit(lbl, lbl_pos)

    def show_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # All not being dragged
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        screen.blit(img, piece.texture_rect)

    def show_moves(self, screen):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect)

    def show_last_move(self, screen):
        theme = self.config.theme

        if self.board.moves:
            initial = self.board.moves[-1].initial
            final = self.board.moves[-1].final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect)

    def show_hover(self, screen):
        if self.hovered_sqr:
            color = (150, 150, 150)
            rect = (self.hovered_sqr.col * SQUARE_SIZE, self.hovered_sqr.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect, width=3)

    def next_turn(self):
        self.turn = "white" if self.turn == "black" else "black"

    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
