from chess import coords


class Move:
    def __init__(self, p, start: coords.Coords, end: coords.Coords, capture = False):
        self.piece = p
        self.start = start
        self.end = end
        self.capture = capture

    def __str__(self):
        cap = "x" if self.capture else ""
        return f"{str(self.piece)}{str(self.start)}{cap}{str(self.end)}"

    def apply(self, game):
        if self.capture:
            # remove captured piece
            self.capture = game.remove_piece(not game.to_move, self.end)

        # remove piece from starting location
        game.remove_piece(game.to_move, self.start)

        # set piece to end location
        game.set_piece(game.to_move, self.piece, self.end)

    def unapply(self, game):
        game.remove_piece(game.to_move, self.end)
        game.set_piece(game.to_move, self.piece, self.start)
        if self.capture:
            game.set_piece(not game.to_move, self.capture, self.end)


class Castle(Move):
    def __init__(self, king, start: coords.Coords, end: coords.Coords, rook, end_pos):
        self.rook = rook
        self.end_pos = end_pos
        super().__init__(king, start, end)

    def apply(self, game):
        super().apply(game)
        extra_move = Move(self.rook, self.rook.pos, self.end_pos)
        extra_move.apply(game)


class DoublePawnMove(Move):
    def apply(self, game):
        super().apply(game)
        game.board.set_en_passent_target(self.piece.pos.x)
