import abc
import coords


BISHOP_DIRS = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
ROOK_DIRS = {(0, 1), (0, -1), (-1, 0), (1, 0)}
KNIGHT_DIRS = {(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, 2)}


class Piece(abc.ABC):
    def __init__(self, pos: coords.Coords, col: bool):
        self.pos = pos
        self.col = col

    def moves_in_dir(self, board, direc: (int, int), limit=7):
        x = self.pos.x
        y = self.pos.y

        while 0 <= x <= 7 and 0 <= y <= 7 and limit > 0:
            limit -= 1
            x += direc[0]
            y += direc[1]
            # white piece
            if board.is_white_piece(coords.Coords(x, y)):
                if self.col:
                    break
                else:
                    yield self.pos, coords.Coords(x, y)
                    break
            # black piece
            if board.is_black_piece(coords.Coords(x, y)):
                if self.col:
                    yield self.pos, coords.Coords(x, y)
                    break
                else:
                    break
            # open square
            yield self.pos, coords.Coords(x, y)

    @abc.abstractmethod
    def generate_moves(self, board):
        pass

    @abc.abstractmethod
    def attacked_squares(self, board):
        pass


class Pawn(Piece):
    def get_direc(self):
        return self.col * -2 + 1

    def generate_moves(self, board):
        # direction the pawn is going=
        ny = self.pos.y + self.get_direc()
        if board.is_free(self.pos.x, ny):
            yield self.pos, coords.Coords(self.pos.x, ny)

        # if pawn is on starting square
        if self.pos.y == 1 + 5 * self.col:
            ny = self.pos.y + self.get_direc() * 2
            if board.is_free(self.pos.x, ny):
                yield self.pos, coords.Coords(self.pos.x, ny)
        for s in self.attacked_squares(board):
            yield self.pos, s

    def attacked_squares(self, board):
        ny = self.pos.y + self.get_direc()
        if self.pos.x != 0:
            nx = self.pos.x - 1
            if board.is_black_piece():
                if self.col:
                    yield coords.Coords(nx, ny)
            if board.is_white_piece():
                if not self.col:
                    yield coords.Coords(nx, ny)
        if self.pos.x != 7:
            nx = self.pos.x + 1
            if board.is_black_piece():
                if self.col:
                    yield coords.Coords(nx, ny)
            if board.is_white_piece():
                if not self.col:
                    yield coords.Coords(nx, ny)


class Knight(Piece):
    def generate_moves(self, board):
        for direc in KNIGHT_DIRS:
            yield from self.moves_in_dir(board, direc, limit=1)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m[1]


class Bishop(Piece):
    def generate_moves(self, board):
        for direc in BISHOP_DIRS:
            yield from self.moves_in_dir(board, direc)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m[1]


class Rook(Piece):
    def generate_moves(self, board):
        for direc in ROOK_DIRS:
            yield from self.moves_in_dir(board, direc)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m[1]


class Queen(Piece):
    def generate_moves(self, board):
        for direc in BISHOP_DIRS | ROOK_DIRS:
            yield from self.moves_in_dir(board, direc)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m[1]


class King(Piece):
    def generate_moves(self, board):
        for direc in BISHOP_DIRS | ROOK_DIRS:
            yield from self.moves_in_dir(board, direc, limit=1)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m[1]
