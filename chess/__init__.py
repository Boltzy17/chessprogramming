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
        self.pieces.append(piece.Rook((7, 7), WHITE))
        self.pieces.append(piece.Knight((1, 7), WHITE))
        self.pieces.append(piece.Knight((6, 7), WHITE))
        self.pieces.append(piece.Bishop((2, 7), WHITE))
        self.pieces.append(piece.Bishop((5, 7), WHITE))
        self.pieces.append(piece.Queen((3, 7), WHITE))
        self.pieces.append(piece.King((4, 7), WHITE))
        for location in coords.pawns_white():
            self.board.set_piece(location, WHITE_PAWN)
            self.pieces.append(piece.Pawn((i, 6), WHITE))

        # Black pieces
        # Board
        self.board.set_piece(0, 0, BLACK_ROOK)
        self.board.set_piece(7, 0, BLACK_ROOK)
        self.board.set_piece(1, 0, BLACK_KNIGHT)
        self.board.set_piece(6, 0, BLACK_KNIGHT)
        self.board.set_piece(2, 0, BLACK_BISHOP)
        self.board.set_piece(5, 0, BLACK_BISHOP)
        self.board.set_piece(3, 0, BLACK_QUEEN)
        self.board.set_piece(4, 0, BLACK_KING)

        # Piece array
        self.pieces.append(piece.Rook((0, 0), BLACK))
        self.pieces.append(piece.Rook((7, 0), BLACK))
        self.pieces.append(piece.Knight((1, 0), BLACK))
        self.pieces.append(piece.Knight((6, 0), BLACK))
        self.pieces.append(piece.Bishop((2, 0), BLACK))
        self.pieces.append(piece.Bishop((5, 0), BLACK))
        self.pieces.append(piece.Queen((3, 0), BLACK))
        self.pieces.append(piece.King((4, 0), BLACK))
        for i in range(8):
            self.board.set_piece(i, 1, BLACK_PAWN)
            self.pieces.append(piece.Pawn((i, 1), BLACK))

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
