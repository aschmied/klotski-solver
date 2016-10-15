import Queue

import board

class Solver:
  def __init__(self):
    self._q = Queue.Queue()
    self._enqueued = set()
    
    initial_board = board.initial_board()
    initial_board.previous_board = None
    self._q.put(initial_board)
    self._enqueued.add(initial_board.hash_key())

  def solve(self):
    while True:
      current_board = self._q.get()
      next_boards = current_board.next_boards()
      for next_board in next_boards:
        if next_board.hash_key() in self._enqueued:
          continue
        next_board.previous_board = current_board
        if board.solved(next_board):
          return _solution_to_list(next_board)
        self._q.put(next_board)
        self._enqueued.add(next_board.hash_key())


def _solution_to_list(solution):
  l = []
  while solution is not None:
    l.append(solution)
    solution = solution.previous_board
  l.reverse()
  return l
