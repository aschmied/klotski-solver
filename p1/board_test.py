import unittest

import board

class GlobalsTestCase(unittest.TestCase):
  def test_index_to_tuple(self):
    self.assertEqual(board._index_to_tuple(1), (0, 1))
    self.assertEqual(board._index_to_tuple(5), (1, 1))

  def test_tuple_to_index(self):
    self.assertEqual(board._tuple_to_index((0, 1)), 1)
    self.assertEqual(board._tuple_to_index((1, 1)), 5)


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
