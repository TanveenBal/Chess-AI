import pygame
import sys
from const import *
from gui import GUI
from square import Square
from ai import ChessAI
from piece import *
from move import Move
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.gui = GUI()
        self.ai = ChessAI("black")

    def mouse_down(self, gui, board, dragger, event):
        dragger.update_mouse(event.pos)
        clicked_row = dragger.mouseY // SQUARE_SIZE
        clicked_col = dragger.mouseX // SQUARE_SIZE
        if board.squares[clicked_row][clicked_col].has_piece():
            piece = board.squares[clicked_row][clicked_col].piece
            if piece.color == gui.turn:
                board.calc_move(piece, clicked_row, clicked_col, bool=True)
                dragger.save_initial(event.pos)
                dragger.drag_piece(piece)
                gui.show_bg(self.screen)
                gui.show_last_move(self.screen)
                gui.show_moves(self.screen)

    def mouse_motion(self, gui, dragger, event):
        motion_row = event.pos[1] // SQUARE_SIZE
        motion_col = event.pos[0] // SQUARE_SIZE
        gui.set_hover(motion_row, motion_col)
        if dragger.dragging:
            dragger.update_mouse(event.pos)
            gui.show_bg(self.screen)
            gui.show_last_move(self.screen)
            gui.show_moves(self.screen)
            gui.show_pieces(self.screen)
            gui.show_hover(self.screen)
            dragger.update_blit(self.screen)

    def mouse_up(self, gui, board, dragger, event):
        if dragger.dragging:
            dragger.update_mouse(event.pos)
            released_row = dragger.mouseY // SQUARE_SIZE
            released_col = dragger.mouseX // SQUARE_SIZE
            if Square.in_range(released_row, released_col):
                initial = Square(dragger.initial_row, dragger.initial_col)
                final = Square(released_row, released_col)
                move = Move(initial, final)
                if board.valid_move(dragger.piece, move):
                    normal_capture = board.squares[released_row][released_col].has_piece()
                    en_passant_capture = (final.col - initial.col != 0 and
                                          board.squares[final.row][final.col].is_empty() and
                                          isinstance(board.squares[initial.row][initial.col].piece, Pawn))
                    captured = normal_capture or en_passant_capture
                    board.move(dragger.piece, move)
                    board.set_true_en_passant(dragger.piece)
                    gui.play_sound(captured)
                    gui.show_bg(self.screen)
                    gui.show_last_move(self.screen)
                    gui.show_pieces(self.screen)
                    gui.next_turn()

        dragger.undrag_piece()

    def ai_move(self, gui, board, dragger, event):
        ai_move = self.ai.find_best_move(board)
        print(ai_move)
        # ai_move_square = ai_move.initial
        # if board.squares[ai_move_square.row][ai_move_square.col].has_piece():
        #     piece = board.squares[ai_move_square.row][ai_move_square.col].piece
        #     if piece.color == gui.turn:
        #         board.calc_move(piece, ai_move_square.row, ai_move_square.col, bool=True)
        #         dragger.save_initial(event.pos)
        #         dragger.drag_piece(piece)
        #         gui.show_bg(self.screen)
        #         gui.show_last_move(self.screen)
        #         gui.show_moves(self.screen)

    def run(self):
        screen = self.screen
        gui = self.gui
        board = self.gui.board
        dragger = self.gui.dragger
        while True:
            gui.show_bg(self.screen)
            gui.show_last_move(self.screen)
            gui.show_moves(self.screen)
            gui.show_pieces(self.screen)
            gui.show_hover(self.screen)
            if dragger.dragging:
                dragger.update_blit(screen)
            # if gui.turn == self.ai.color:
            #     self.ai_move(gui, board, dragger, event)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down(gui, board, dragger, event)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion(gui, dragger, event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_up(gui, board, dragger, event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.ai_move(gui, board, dragger, event)
                    if event.key == pygame.K_u:
                        if board.undo_move():
                            gui.next_turn()
                    if event.key == pygame.K_t:
                        gui.change_theme()
                    if event.key == pygame.K_r:
                        gui.reset()
                        screen = self.screen
                        gui = self.gui
                        board = self.gui.board
                        dragger = self.gui.dragger

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    main = Main()
    main.run()