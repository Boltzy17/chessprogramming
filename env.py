import chess
import random


game = chess.Chess()
game.generate_standard_pieces()

moves_played = []
for _ in range(50):
    moves = game.possible_moves()
    to_play = random.choice(list(moves))
    game.apply_move(to_play)
    moves_played.append(to_play)

moves_played.reverse()
for move in moves_played:
    game.unapply_move(move)
game.print_board()


