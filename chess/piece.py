import abc


BISHOP_DIRS = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
ROOK_DIRS = {(0, 1), (0, -1), (-1, 0), (1, 0)}
KNIGHT_DIRS = {(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, 2)}


class Piece(abc.ABC):
    def __init__(self, pos: (int, int), col: bool):
        self.pos = pos
        self.col = col

    def moves_in_dir(self, board, direc: (int, int), limit=7):
        x = self.pos[0]
        y = self.pos[1]

        while 0 <= x <= 7 and 0 <= y <= 7 and limit > 0:
            limit -= 1
            x += direc[0]
            y += direc[1]
            # white piece
            if board[x][y] & 63:
                if self.col:
                    break
                else:
                    yield self.pos, (x, y)
                    break
            # black piece
            if board[x][y] & 4032:
                if self.col:
                    yield self.pos, (x, y)
                    break
                else:
                    break
            # open square
            yield self.pos, (x, y)

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
        ny = self.pos[1] + self.get_direc()
        if board.is_free(self.pos[0], ny):
            yield self.pos, (self.pos[0], ny)

        # if pawn is on starting square
        if self.pos[1] == 1 + 5 * self.col:
            ny = self.pos[1] + self.get_direc() * 2
            if board.is_free(self.pos[0], ny):
                yield self.pos, (self.pos[0], ny)
        for s in self.attacked_squares(board):
            yield self.pos, s

    def attacked_squares(self, board):
        ny = self.pos[1] + self.get_direc()
        if self.pos[0] != 0:
            nx = self.pos[0] - 1
            # black piece
            if board[nx][ny] & 4032:
                if self.col:
                    yield nx, ny
            # white piece
            if board[nx][ny] & 63:
                if not self.col:
                    yield nx, ny
        if self.pos[0] != 7:
            nx = self.pos[0] + 1
            # black piece
            if board[nx][ny] & 4032:
                if self.col:
                    yield nx, ny
            # white piece
            if board[nx][ny] & 63:
                if not self.col:
                    yield nx, ny


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
