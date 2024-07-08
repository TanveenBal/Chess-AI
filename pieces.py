import copy
import math
import pygame


class Piece(pygame.sprite.Sprite):
    def __init__(self, weight, color, position):
        super().__init__()
        self.weight = weight
        self.color = color
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 16, 16)

    def __repr__(self):
        return f"{self.__class__.__name__[0]}{self.color[0]}"

    def __copy__(self):
        return type(self)(self.color, self.position)

    def __deepcopy__(self, memo):
        return type(self)(
            copy.deepcopy(self.color, memo),
            copy.deepcopy(self.position, memo)
        )

    def copy(self):
        return copy.deepcopy(self)

    def move_set(self):
        return []


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(10, color, position)

    def move_set(self):
        moves = []
        row, col = self.position
        if self.color == "white":
            if row - 1 >= 0:
                moves.append((row - 1, col))
            if row == 6 and row - 2 >= 0:
                moves.append((row - 2, col))
            if row - 1 >= 0 and col - 1 >= 0:
                moves.append((row - 1, col - 1))
            if row - 1 >= 0 and col + 1 < 8:
                moves.append((row - 1, col + 1))
        else:
            if row + 1 < 8:
                moves.append((row + 1, col))
            if row == 1 and row + 2 < 8:
                moves.append((row + 2, col))
            if row + 1 < 8 and col - 1 >= 0:
                moves.append((row + 1, col - 1))
            if row + 1 < 8 and col + 1 < 8:
                moves.append((row + 1, col + 1))

        return moves


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(30, color, position)

    def move_set(self):
        row, col = self.position
        possible_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]

        valid_moves = [(r, c) for r, c in possible_moves if 0 <= r < 8 and 0 <= c < 8]
        return valid_moves


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(30, color, position)

    def move_set(self):
        moves = []
        row, col = self.position
        for i in range(1, 8):
            if row + i < 8 and col + i < 8:
                moves.append((row + i, col + i))
            if row + i < 8 and col - i >= 0:
                moves.append((row + i, col - i))
            if row - i >= 0 and col + i < 8:
                moves.append((row - i, col + i))
            if row - i >= 0 and col - i >= 0:
                moves.append((row - i, col - i))
        return moves


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(50, color, position)

    def move_set(self):
        moves = []
        row, col = self.position
        for i in range(1, 8):
            if row + i < 8:
                moves.append((row + i, col))
            if row - i >= 0:
                moves.append((row - i, col))
            if col + i < 8:
                moves.append((row, col + i))
            if col - i >= 0:
                moves.append((row, col - i))
        return moves


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(90, color, position)

    def move_set(self):
        return Rook.move_set(self) + Bishop.move_set(self)


class King(Piece):
    def __init__(self, color, position):
        super().__init__(math.inf, color, position)

    def move_set(self):
        moves = []
        row, col = self.position
        possible_moves = [
            (row + 1, col), (row - 1, col),
            (row, col + 1), (row, col - 1),
            (row + 1, col + 1), (row + 1, col - 1),
            (row - 1, col + 1), (row - 1, col - 1)
        ]

        valid_moves = [(r, c) for r, c in possible_moves if 0 <= r < 8 and 0 <= c < 8]
        return valid_moves


class Empty(Piece):
    def __init__(self, position):
        super().__init__(0, "none", position)

    def __copy__(self):
        return type(self)(self.color, self.position)

    def __deepcopy__(self, memo):
        return type(self)(
            copy.deepcopy(self.position, memo)
        )

    def __repr__(self):
        return "--"
