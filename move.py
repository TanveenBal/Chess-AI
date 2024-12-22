class Move:

    def __init__(self, initial, final, piece_moved=None, piece_taken=None, en_passant_row=None, en_passant_col=None,promotion=False, en_passant=False, castle=False):
        self.initial = initial
        self.final = final
        self.piece_moved = piece_moved
        self.piece_taken = piece_taken
        self.promotion = promotion
        self.en_passant = en_passant
        self.en_passant_row = en_passant_row
        self.en_passant_col = en_passant_col
        self.castle = castle

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def __repr__(self):
        return f"Move({self.initial}, {self.final})"
