import Queue

import board

class Solver:
  def __init__(self):
    self._q = Queue.Queue()
    self._enqueued = set()
    
    initial_board = board.initial_board()
    self._q.put(initial_board)
    self._enqueued.add(initial_board.hash_key())

  def solve(self):
    while True:
      current_board = self._q.get()
      next_boards = current_board.next_boards()
      for next_board in next_boards:
        if next_board.hash_key() in self._enqueued:
          next
        next_board.previous_board = current_board
        if board.solved(next_board):
          return next_board
        self._q.put(next_board)
        self._enqueued.add(next_board.hash_key())
