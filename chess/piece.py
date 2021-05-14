import abc
from chess import coords
from chess import move


BISHOP_DIRS = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
ROOK_DIRS = {(0, 1), (0, -1), (-1, 0), (1, 0)}
KNIGHT_DIRS = {(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)}


class Piece(abc.ABC):
    def __init__(self, pos: coords.Coords, col: bool):
        self.pos = pos
        self.col = col

    def moves_in_dir(self, board, direc: (int, int), limit=7):
        x = self.pos.x + direc[0]
        y = self.pos.y + direc[1]

        while 0 <= x <= 7 and 0 <= y <= 7 and limit > 0:
            limit -= 1
            # white piece
            if board.is_white_piece(coords.Coords(x, y)):
                if not self.col:
                    yield move.Move(self, self.pos, coords.Coords(x, y), capture = True)
                break
            # black piece
            if board.is_black_piece(coords.Coords(x, y)):
                if self.col:
                    yield move.Move(self, self.pos, coords.Coords(x, y), capture = True)
                break
            # open square
            yield move.Move(self, self.pos, coords.Coords(x, y))
            x += direc[0]
            y += direc[1]

    def set_pos(self, pos: coords.Coords):
        self.pos = pos

    def value(self):
        return self.val << (6 - self.col * 6)

    @abc.abstractmethod
    def generate_moves(self, board):
        pass

    @abc.abstractmethod
    def attacked_squares(self, board):
        pass

    @property
    @abc.abstractmethod
    def val(self):
        pass


class Pawn(Piece):
    def __str__(self):
        return ""

    def get_direc(self):
        return self.col * -2 + 1

    def generate_moves(self, board):
        # direction the pawn is going
        ny = self.pos.y + self.get_direc()
        if board.is_free(coords.Coords(self.pos.x, ny)):
            yield move.Move(self, self.pos, coords.Coords(self.pos.x, ny))

        # if pawn is on starting square
        if self.pos.y == 1 + 5 * self.col:
            ny = self.pos.y + self.get_direc() * 2
            if board.is_free(coords.Coords(self.pos.x, ny)):
                yield move.DoublePawnMove(self, self.pos, coords.Coords(self.pos.x, ny))
        for s in self.attacked_squares(board):
            yield move.Move(self, self.pos, s, capture = True)

    def attacked_squares(self, board):
        ny = self.pos.y + self.get_direc()
        if self.pos.x != 0:
            nx = self.pos.x - 1
            if board.is_black_piece(coords.Coords(nx, ny)):
                if self.col:
                    yield coords.Coords(nx, ny)
            if board.is_white_piece(coords.Coords(nx, ny)):
                if not self.col:
                    yield coords.Coords(nx, ny)
        if self.pos.x != 7:
            nx = self.pos.x + 1
            if board.is_black_piece(coords.Coords(nx, ny)):
                if self.col:
                    yield coords.Coords(nx, ny)
            if board.is_white_piece(coords.Coords(nx, ny)):
                if not self.col:
                    yield coords.Coords(nx, ny)
        # TODO En Passent

    @property
    def val(self):
        return 1


class Knight(Piece):
    def __str__(self):
        return "N"

    def generate_moves(self, board):
        for direc in KNIGHT_DIRS:
            yield from self.moves_in_dir(board, direc, limit=1)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m.end

    @property
    def val(self):
        return 2


class Bishop(Piece):
    def __str__(self):
        return "B"

    def generate_moves(self, board):
        for direc in BISHOP_DIRS:
            yield from self.moves_in_dir(board, direc)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m.end

    @property
    def val(self):
        return 4


class Rook(Piece):
    def __str__(self):
        return "R"

    def generate_moves(self, board):
        for direc in ROOK_DIRS:
            yield from self.moves_in_dir(board, direc)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m.end

    @property
    def val(self):
        return 8


class Queen(Piece):
    def __str__(self):
        return "Q"

    def generate_moves(self, board):
        for direc in BISHOP_DIRS | ROOK_DIRS:
            yield from self.moves_in_dir(board, direc)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m.end

    @property
    def val(self):
        return 16


class King(Piece):
    def __str__(self):
        return "K"

    def generate_moves(self, board):
        for direc in BISHOP_DIRS | ROOK_DIRS:
            yield from self.moves_in_dir(board, direc, limit=1)

    def attacked_squares(self, board):
        for m in self.generate_moves(board):
            yield m.end

    @property
    def val(self):
        return 32
