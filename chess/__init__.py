import numpy as np
import piece
import coords

WHITE = True
BLACK = False

# ----------------------------- #
# PIECE ORDER:
# 0 PAWN
# 1 KNIGHT
# 2 BISHOP
# 3 ROOK
# 4 QUEEN
# 5 KING
# ----------------------------- #

WHITE_PAWN = 1
WHITE_KNIGHT = 2
WHITE_BISHOP = 4
WHITE_ROOK = 8
WHITE_QUEEN = 16
WHITE_KING = 32
BLACK_PAWN = 64
BLACK_KNIGHT = 128
BLACK_BISHOP = 256
BLACK_ROOK = 512
BLACK_QUEEN = 1024
BLACK_KING = 2048

# ----------------------------- #
# The board representation is an array of 64 squares containing 16-bit unsigned integers.
# These integers contain:
# 6 LSB: white pieces in order
# bit 7  - 12: black pieces in order
# bit 13 - 16: The top left square will contain the castle legality moves > KQkq
# bit 13 - 16: The next 2 squares will contain the 50 mr counter
# EP targets are pawns on the first/last rank!
# ----------------------------- #


class Board:
    def __init__(self):
        self.board = np.ndarray((8, 8), dtype=np.uint16)

    def is_free(self, location: coords.Coords):
        return self.board[location.x][location.y] & 4095

    def set_piece(self, location: coords.Coords, p: int):
        self.board[location.x][location.y] = p


class Chess:
    def __init__(self):
        self.to_move = WHITE
        self.pieces = []
        self.board = Board()
        self.generate_standard_pieces()

    def generate_standard_pieces(self):
        # White pieces
        # Board
        self.board.set_piece(coords.A1, WHITE_ROOK)
        self.board.set_piece(coords.H1, WHITE_ROOK)
        self.board.set_piece(coords.B1, WHITE_KNIGHT)
        self.board.set_piece(coords.G1, WHITE_KNIGHT)
        self.board.set_piece(coords.C1, WHITE_BISHOP)
        self.board.set_piece(coords.F1, WHITE_BISHOP)
        self.board.set_piece(coords.D1, WHITE_QUEEN)
        self.board.set_piece(coords.E1, WHITE_KING)

        # Piece array
        self.pieces.append(piece.Rook(coords.A1, WHITE))
        self.pieces.append(piece.Rook(coords.B1, WHITE))
        self.pieces.append(piece.Knight(coords.C1, WHITE))
        self.pieces.append(piece.Knight(coords.D1, WHITE))
        self.pieces.append(piece.Bishop(coords.E1, WHITE))
        self.pieces.append(piece.Bishop(coords.F1, WHITE))
        self.pieces.append(piece.Queen(coords.G1, WHITE))
        self.pieces.append(piece.King(coords.H1, WHITE))
        for location in coords.pawns_white():
            self.board.set_piece(location, WHITE_PAWN)
            self.pieces.append(piece.Pawn(location, WHITE))

        # Black pieces
        # Board
        self.board.set_piece(coords.A8, BLACK_ROOK)
        self.board.set_piece(coords.H8, BLACK_ROOK)
        self.board.set_piece(coords.B8, BLACK_KNIGHT)
        self.board.set_piece(coords.G8, BLACK_KNIGHT)
        self.board.set_piece(coords.C8, BLACK_BISHOP)
        self.board.set_piece(coords.F8, BLACK_BISHOP)
        self.board.set_piece(coords.D8, BLACK_QUEEN)
        self.board.set_piece(coords.E8, BLACK_KING)

        # Piece array
        self.pieces.append(piece.Rook(coords.A8, BLACK))
        self.pieces.append(piece.Rook(coords.H8, BLACK))
        self.pieces.append(piece.Knight(coords.B8, BLACK))
        self.pieces.append(piece.Knight(coords.G8, BLACK))
        self.pieces.append(piece.Bishop(coords.C8, BLACK))
        self.pieces.append(piece.Bishop(coords.F8, BLACK))
        self.pieces.append(piece.Queen(coords.D8, BLACK))
        self.pieces.append(piece.King(coords.E8, BLACK))
        for location in coords.pawns_black():
            self.board.set_piece(location, BLACK_PAWN)
            self.pieces.append(piece.Pawn(location, BLACK))

    def attacked_squares(self):
        for p in self.pieces:
            yield from p.attacked_squares(self.board)

    def possible_moves(self):
        for p in self.pieces:
            yield from p.generate_moves(self.board)
        castle_rights = 2  # TODO
        # castle_rights = self.board[0][0] >> 12
        if castle_rights & 1:
            if not any(x in self.attacked_squares() for x in ((7, 4), (7, 5), (7, 6))):
                yield (7, 4), (7, 6)
        if castle_rights & 2:
            if not any(x in self.attacked_squares() for x in ((7, 4), (7, 3), (7, 2))):
                yield (7, 4), (7, 2)
        if castle_rights & 4:
            if not any(x in self.attacked_squares() for x in ((0, 4), (0, 5), (0, 6))):
                yield (0, 4), (0, 6)
        if castle_rights & 8:
            if not any(x in self.attacked_squares() for x in ((0, 4), (0, 3), (0, 2))):
                yield (0, 4), (0, 2)

    def move(self):
        pass
