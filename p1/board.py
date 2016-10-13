class Piece:
  def __init__(self, occupied_indexes):
    self._occupied_indexes = occupied_indexes

  def next_pieces(self, occupied):
    pass


class Board:
  def __init__(self, pieces, occupied):
    self._pieces = pieces
    self._occupied = occupied

  def make_move(self, src_piece, dst_piece):
    next_pieces = list(self._pieces)
    next_occupied = list(self._occupied)

    src_piece_index = next_occupied[src_piece.occupied_indexes[0]]
    next_pieces[src_piece_index] = dst_piece

    for vacated_index in src_piece.occupied_indexes:
      next_occupied[vacated_index] = -1

    for occupied_index in dst_piece.occupied_indexes:
      next_occupied[occupied_index] = src_piece_index

    return Board(next_pieces, next_occupied)

  def next_boards(self):
    next_boards = []
    for piece in self._pieces:
      next_pieces = piece.next_pieces(occupied)
      for next_piece in next_pieces:
        next_boards.append(self.make_move(piece, next_piece))


def initial_board():
  occupied = [
    -1,  0,  0, -1,
     1,  0,  0,  2,
     1,  3,  4,  2,
     5,  6,  7,  8,
     5,  9,  9,  8
  ]
  pieces = []
  for i in range(10): 
    pieces.append(Piece([occupied_index for ((occupied_index, piece_index)) in enumerate(occupied) if piece_index == i]))
  return Board(pieces, occupied)
