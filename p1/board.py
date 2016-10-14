width = 4
height = 5

class Piece:
  def __init__(self, label, occupied_squares):
    self._label = label
    self._occupied_squares = occupied_squares

  def label(self):
    return self._label

  def next_pieces(self, squares):
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [ self._shift(offset)
             for offset in offsets
             if self._legal_shift(squares, offset) ]

  def _legal_shift(self, squares, offset):
    for occupied_square in self._occupied_squares:
      r, c = _index_to_tuple(occupied_square)
      sr = r + offset[0]
      sc = c + offset[1]

      if sr < 0 or sr >= height:
        return False
      if sc < 0 or sc >= width:
        return False

      if not squares[_tuple_to_index((sr, sc))] in [-1, self.label()]:
        return False

    return True

  def _shift(self, offset):
    new_occupied_squares = [ self._shift_square(square, offset)
                             for square in self._occupied_squares ]
    return Piece(self._label, new_occupied_squares)

  def _shift_square(self, square, offset):
    r, c = _index_to_tuple(square)
    return _tuple_to_index((r + offset[0], c + offset[1]))

class Board:
  def __init__(self, pieces, squares):
    self._pieces = pieces
    self._squares = squares

  def make_move(self, src_piece, dst_piece):
    assert src_piece.label() == dst_piece.label()
    label = src_piece.label()

    new_pieces = list(self._pieces)
    new_squares = list(self._squares)

    new_pieces[label] = dst_piece

    for vacated_square in src_piece._occupied_squares:
      new_squares[vacated_square] = -1

    for occupied_square in dst_piece._occupied_squares:
      new_squares[occupied_square] = label

    return Board(new_pieces, new_squares)

  def next_boards(self):
    next_boards = []
    for piece in self._pieces:
      next_pieces = piece.next_pieces(self._squares)
      for next_piece in next_pieces:
        next_boards.append(self.make_move(piece, next_piece))
    return next_boards


def initial_board():
  squares = [
    -1,  0,  0, -1,
     1,  0,  0,  2,
     1,  3,  4,  2,
     5,  6,  7,  8,
     5,  9,  9,  8
  ]
  pieces = []
  for label_to_find in range(10):
    occupied_sauares = [ occupied_square
                         for (occupied_square, label) in enumerate(squares)
                         if label == label_to_find ]
    pieces.append(Piece(label_to_find, occupied_sauares))
  return Board(pieces, squares)

def solved(board):
  return board._squares[17] == 0 and board._squares[18] == 0

def _index_to_tuple(index):
  r = index / width
  c = index % width
  return (r, c)

def _tuple_to_index(tuple):
  return width * tuple[0] + tuple[1]
