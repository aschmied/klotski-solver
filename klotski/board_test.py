import unittest

import board

class HelpersTestCase(unittest.TestCase):
  def test_index_to_tuple(self):
    self.assertEqual(board._index_to_tuple(1), (0, 1))
    self.assertEqual(board._index_to_tuple(5), (1, 1))

  def test_tuple_to_index(self):
    self.assertEqual(board._tuple_to_index((0, 1)), 1)
    self.assertEqual(board._tuple_to_index((1, 1)), 5)

  def test_solved(self):
    not_solved = board.Board([], [1] * 20)
    solved = board.Board([], [1, 1, 1, 1,
                              1, 1, 1, 1,
                              1, 1, 1, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1])
    self.assertFalse(board.solved(not_solved))
    self.assertTrue(board.solved(solved))

  def test_str(self):
    b = board.Board([], [-1, 0, 0, 1, 2, 2, 3, 3])
    self.assertEqual(b.__str__(), ' 001\n2233')


class NumberOfStatesTestCase(unittest.TestCase):
  def setUp(self):
    self.occupied = [
      True, True, True, True,
      True, True, True, True,
      True, True, True, True,
      True, False, False, False,
      True, False, False, True,
    ]

  def test_block_empty(self):
    self.assertTrue(board._block_empty(self.occupied, 3, 1, 2, 2))
    self.assertTrue(board._block_empty(self.occupied, 4, 1, 1, 2))
    self.assertFalse(board._block_empty(self.occupied, 3, 2, 2, 2))
    self.assertFalse(board._block_empty(self.occupied, 3, 3, 2, 2))

  def test_fill_block(self):
    occupied = [False] * 20
    board._fill_block(occupied, 3, 1, 2, 2, True)
    for row in range(5):
      for col in range(4):
        value = occupied[4 * row + col]
        if row > 2 and col > 0 and col < 3:
          self.assertTrue(value)
        else:
          self.assertFalse(value)

  def test_next_empty_square(self):
    self.assertEqual(board._next_empty_square(self.occupied, 0, 0), (3, 1))
    self.assertEqual(board._next_empty_square(self.occupied, 4, 0), (4, 1))
    self.assertEqual(board._next_empty_square(self.occupied, 4, 3), (5, 0))

  def test_number_of_states(self):
    self.assertEqual(board._number_of_states([0] * 5, [True] * 20, 5, 0), 1)
    self.assertEqual(board._number_of_states([1, 1, 0, 0, 0], self.occupied, 3, 1), 0)
    self.assertEqual(board._number_of_states([1, 0, 0, 0, 1], self.occupied, 3, 1), 1)
    self.assertEqual(board._number_of_states([0, 1, 0, 3, 0], self.occupied, 3, 1), 3)
    self.assertEqual(board._number_of_states([0, 1, 0, 2, 1], self.occupied, 3, 1), 9)


class PieceTestCase(unittest.TestCase):
  def setUp(self):
    self.squares = [ -1, 0, 0, 1,
                     -1, 2, 2, 1 ]
    self.piece = board.Piece(0, [1, 2])

  def test_legal_shift(self):
    self.assertTrue(self.piece._legal_shift(self.squares, (0, -1)))
    self.assertFalse(self.piece._legal_shift(self.squares, (0, 1)))
    self.assertFalse(self.piece._legal_shift(self.squares, (-1, 0)))
    self.assertFalse(self.piece._legal_shift(self.squares, (1, 0)))

  def test_shift(self):
    shifted = self.piece._shift((0, -1))
    self.assertEqual(shifted.label(), 0)
    self.assertEqual(shifted._occupied_squares, [0, 1])

  def test_shift_square(self):
    self.assertEqual(self.piece._shift_square(5, (-1, 0)), 1)
    self.assertEqual(self.piece._shift_square(5, (0, 1)), 6)

  def test_next_pieces(self):
    next_pieces = self.piece.next_pieces(self.squares)
    self.assertEqual(len(next_pieces), 1)
    next_piece = next_pieces[0]
    self.assertEqual(next_piece.label(), 0)
    self.assertEqual(next_piece._occupied_squares, [0, 1])


class BoardTestCase(unittest.TestCase):
  def setUp(self):
    self.piece = board.Piece(0, [1, 2])
    self.board = board.Board([self.piece], [-1, 0, 0, -1,
                                             1, 1, 1,  1])

  def test_hash_key(self):
    self.assertEqual(self.board.hash_key(), ' SS tttt')

  def test_make_move(self):
    new_piece = board.Piece(0, [2, 3])
    new_board = self.board.make_move(self.piece, new_piece)
    self.assertEqual(len(new_board._pieces), 1)
    self.assertEqual(new_board._pieces[0], new_piece)
    self.assertEqual(new_board._squares, [-1, -1, 0, 0, 1, 1, 1, 1])

  def test_next_boards(self):
    next_boards = self.board.next_boards()
    self.assertEqual(len(next_boards), 2)


if __name__ == '__main__':
  unittest.main()
