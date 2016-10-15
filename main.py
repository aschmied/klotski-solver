import time

import p1.solver

t0 = time.time()
solver = p1.solver.Solver()
solution = solver.solve()
t1 = time.time()

print "Found solution in {} seconds".format(t1 - t0)
print "Solution has {} moves".format(len(solution) - 1)

for board in solution:
  print(board)
  print
