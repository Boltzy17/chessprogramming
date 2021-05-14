import numpy as np
from chess import piece
from chess import coords
from chess import move

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
        self.board = np.zeros((8, 8), dtype=np.uint16)

    def get_castle_rights(self):
        cr = self.board[0][0] >> 12
        return cr & 1, cr & 2, cr & 4, cr & 8

    def get_piece_at(self, x, y):
        return self.board[x][y]

    def is_black_piece(self, location: coords.Coords):
        return self.board[location.x][location.y] & 4032

    def is_ep_target(self, x):
        return self.board[x][4] & 4096

    def is_free(self, location: coords.Coords):
        return not (self.board[location.x][location.y] & 4095)

    def is_white_piece(self, location: coords.Coords):
        return self.board[location.x][location.y] & 63

    def remove_piece(self, location: coords.Coords):
        self.board[location.x][location.y] &= 61440

    def set_castle_rights(self, white_king = None, white_queen = None, black_king = None, black_queen = None):
        if white_king:
            self.board[0][0] ^= 1 << 12
        if white_queen:
            self.board[0][0] ^= 1 << 13
        if black_king:
            self.board[0][0] ^= 1 << 14
        if black_queen:
            self.board[0][0] ^= 1 << 15

    def set_en_passent_target(self, x: int):
        self.board[x][4] += 1 << 12

    def set_piece(self, location: coords.Coords, p: int):
        self.board[location.x][location.y] = p


class Chess:
    def __init__(self):
        self.to_move = WHITE
        self.pieces = [{}, {}]
        self.kings = [None, None]
        self.board = Board()
        # self.generate_standard_pieces()

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
        self.pieces[WHITE][coords.A1] = piece.Rook(coords.A1, WHITE)
        self.pieces[WHITE][coords.H1] = piece.Rook(coords.H1, WHITE)
        self.pieces[WHITE][coords.B1] = piece.Knight(coords.B1, WHITE)
        self.pieces[WHITE][coords.G1] = piece.Knight(coords.G1, WHITE)
        self.pieces[WHITE][coords.C1] = piece.Bishop(coords.C1, WHITE)
        self.pieces[WHITE][coords.F1] = piece.Bishop(coords.F1, WHITE)
        self.pieces[WHITE][coords.D1] = piece.Queen(coords.D1, WHITE)
        self.kings[WHITE] = piece.King(coords.E1, WHITE)
        self.pieces[WHITE][coords.E1] = self.kings[WHITE]
        for location in coords.pawns_white():
            self.board.set_piece(location, WHITE_PAWN)
            self.pieces[WHITE][location] = piece.Pawn(location, WHITE)

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
        self.pieces[BLACK][coords.A8] = piece.Rook(coords.A8, BLACK)
        self.pieces[BLACK][coords.H8] = piece.Rook(coords.H8, BLACK)
        self.pieces[BLACK][coords.B8] = piece.Knight(coords.B8, BLACK)
        self.pieces[BLACK][coords.G8] = piece.Knight(coords.G8, BLACK)
        self.pieces[BLACK][coords.C8] = piece.Bishop(coords.C8, BLACK)
        self.pieces[BLACK][coords.F8] = piece.Bishop(coords.F8, BLACK)
        self.pieces[BLACK][coords.D8] = piece.Queen(coords.D8, BLACK)
        self.kings[BLACK] = piece.King(coords.E8, BLACK)
        self.pieces[BLACK][coords.E8] = self.kings[BLACK]
        for location in coords.pawns_black():
            self.board.set_piece(location, BLACK_PAWN)
            self.pieces[BLACK][location] = piece.Pawn(location, BLACK)

        self.board.set_castle_rights(True, True, True, True)

    def attacked_squares(self):
        for p in self.pieces[self.to_move].values():
            yield from p.attacked_squares(self.board)

    def possible_moves(self):
        for p in self.pieces[self.to_move].values():
            yield from p.generate_moves(self.board)
        (white_king_side, white_queen_side, black_king_side, black_queen_side) = self.board.get_castle_rights()
        attacked_squares = list(self.attacked_squares())
        if self.to_move:
            if white_king_side:
                if not any(
                    x in attacked_squares for x in (coords.E1, coords.F1)
                ) and all(self.board.is_free(x) for x in (coords.F1, coords.G1)):
                    yield move.Castle(self.kings[WHITE], coords.E1, coords.G1, self.pieces[WHITE][coords.H1], coords.F1)
            if white_queen_side:
                if not any(
                    x in attacked_squares for x in (coords.E1, coords.D1)
                ) and all(self.board.is_free(x) for x in (coords.D1, coords.C1, coords.B1)):
                    yield move.Castle(self.kings[WHITE], coords.E1, coords.C1, self.pieces[WHITE][coords.A1], coords.C1)
        else:
            if black_king_side:
                if not any(
                    x in attacked_squares for x in (coords.E8, coords.F8)
                ) and all(self.board.is_free(x) for x in (coords.F8, coords.G8)):
                    yield move.Castle(self.kings[BLACK], coords.E8, coords.G8, self.pieces[BLACK][coords.H8], coords.F8)
            if black_queen_side:
                if not any(
                    x in attacked_squares for x in (coords.E8, coords.D8)
                ) and all(self.board.is_free(x) for x in (coords.D8, coords.C8, coords.B8)):
                    yield move.Castle(self.kings[BLACK], coords.E8, coords.C8, self.pieces[BLACK][coords.A8], coords.C8)

    def apply_move(self, m: move.Move):
        m.apply(self)
        if m.piece in self.kings:
            if self.to_move:
                self.board.set_castle_rights()

        print(f"played move: {m}")
        # switch player turn
        self.to_move = not self.to_move

    def unapply_move(self, m: move.Move):
        self.to_move = not self.to_move
        m.unapply(self)
        print(f"unplayed move: {m}")

    def remove_piece(self, colour: bool, location: coords.Coords):
        self.board.remove_piece(location)
        return self.pieces[colour].pop(location)

    def set_piece(self, colour: bool, p: piece.Piece, location: coords.Coords):
        self.board.set_piece(location, p.value())
        self.pieces[colour][location] = p
        p.set_pos(location)

    def print_board(self):
        board_str = ""
        for y in range(8):
            board_str += "|"
            for x in range(8):
                piece_at = self.board.get_piece_at(x, y)
                if piece_at & WHITE_PAWN:
                    board_str += "P"
                elif piece_at & WHITE_KNIGHT:
                    board_str += "N"
                elif piece_at & WHITE_BISHOP:
                    board_str += "B"
                elif piece_at & WHITE_ROOK:
                    board_str += "R"
                elif piece_at & WHITE_QUEEN:
                    board_str += "Q"
                elif piece_at & WHITE_KING:
                    board_str += "K"
                elif piece_at & BLACK_PAWN:
                    board_str += "p"
                elif piece_at & BLACK_KNIGHT:
                    board_str += "n"
                elif piece_at & BLACK_BISHOP:
                    board_str += "b"
                elif piece_at & BLACK_ROOK:
                    board_str += "r"
                elif piece_at & BLACK_QUEEN:
                    board_str += "q"
                elif piece_at & BLACK_KING:
                    board_str += "k"
                else:
                    board_str += "-"
            board_str += "|\n"
        print(board_str)
