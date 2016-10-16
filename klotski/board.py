WIDTH = 4
HEIGHT = 5

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

      if sr < 0 or sr >= HEIGHT:
        return False
      if sc < 0 or sc >= WIDTH:
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

  def __str__(self):
    output = ''
    for i, square in enumerate(self._squares):
      if i > 0 and i % WIDTH == 0:
        output += '\n'
      output += str(square) if not square == -1 else ' '
    return output

  def hash_key(self):
    value_map = { -1: ' ', 0: 'S', 1: 't', 2: 't', 3: 's', 4: 's', 5: 't', 6: 's', 7: 's', 8: 't', 9: 'w'}
    chars = [value_map[s] for s in self._squares]
    return ''.join(chars)

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

_piece_heights = [2, 1, 2, 1, 1]
_piece_widths = [2, 2, 1, 1, 1]

def number_of_states():
  remaining_pieces = [1, 1, 4, 4, 2]
  occupied_squares = [False] * (WIDTH * HEIGHT)
  return _number_of_states(remaining_pieces, occupied_squares, 0, 0)

def _number_of_states(remaining_pieces, occupied_squares, start_row, start_col):
  if all(map(lambda x: x == 0, remaining_pieces)):
    assert start_row == HEIGHT
    assert start_col == 0
    return 1
  assert start_row < HEIGHT and start_col < WIDTH

  number_of_states = 0
  for (i, count) in enumerate(remaining_pieces):
    if count == 0:
      continue
    h = _piece_heights[i]
    w = _piece_widths[i]
    if not _block_empty(occupied_squares, start_row, start_col, h, w):
      continue

    _fill_block(occupied_squares, start_row, start_col, h, w, True)
    remaining_pieces[i] -= 1

    next_start_row, next_start_col = _next_empty_square(occupied_squares, start_row, start_col)
    number_of_states += _number_of_states(remaining_pieces, occupied_squares, next_start_row, next_start_col)

    _fill_block(occupied_squares, start_row, start_col, h, w, False)
    remaining_pieces[i] += 1
  return number_of_states

def _block_empty(occupied_squares, row, col, height, width):
  if row + height > HEIGHT or col + width > WIDTH:
    return False
  for r in range(row, row + height):
    for c in range(col, col + width):
      if occupied_squares[_tuple_to_index((r, c))]:
        return False
  return True

def _fill_block(occupied_squares, row, col, height, width, value):
  for r in range(row, row + height):
    for c in range(col, col + width):
      occupied_squares[_tuple_to_index((r, c))] = value

def _next_empty_square(occupied_squares, start_row, start_col):
  index = _tuple_to_index((start_row, start_col))
  while index < WIDTH * HEIGHT and occupied_squares[index]:
    index += 1
  return _index_to_tuple(index)

def _index_to_tuple(index):
  r = index / WIDTH
  c = index % WIDTH
  return (r, c)

def _tuple_to_index(tuple):
  return WIDTH * tuple[0] + tuple[1]
