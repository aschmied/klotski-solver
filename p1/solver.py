import collections

import board

class Solver:
  def __init__(self):
    self._q = collections.deque()
    self._enqueued = set()
    
    initial_board = board.initial_board()
    initial_board.previous_board = None
    self._q.append(initial_board)
    self._enqueued.add(initial_board.hash_key())

  def solve(self):
    solutions = []
    while len(self._q) > 0:
      current_board = self._q.popleft()
      next_boards = current_board.next_boards()
      for next_board in next_boards:
        if next_board.hash_key() in self._enqueued:
          continue
        next_board.previous_board = current_board
        if board.solved(next_board):
          solutions.append(_solution_to_list(next_board))
        self._q.append(next_board)
        self._enqueued.add(next_board.hash_key())
    return solutions, _analyze_solutions(solutions, self._enqueued)


def _analyze_solutions(solutions, examined_configurations):
  return {
    'number_of_solutions': len(solutions),
    'length_of_shortest_solution': min(map(len, solutions)),
    'length_of_longest_solution': max(map(len, solutions)),
    'number_of_unique_end_states': len(set([s[-1].hash_key() for s in solutions])),
    'number_of_board_states': len(examined_configurations),
  }

def _solution_to_list(solution):
  l = []
  while solution is not None:
    l.append(solution)
    solution = solution.previous_board
  l.reverse()
  return l
