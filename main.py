import time

import p1.solver

t0 = time.time()
solver = p1.solver.Solver()
solutions = solver.solve()
t1 = time.time()

stats = p1.solver.analyze_solutions(solutions)

print 'Finished in {} seconds'.format(t1 - t0)
print '  {} unique solutions'.format(stats['number_of_solutions'])
print '  {} moves in shortest solution'.format(stats['length_of_shortest_solution'])
print '  {} moves in longest solution'.format(stats['length_of_longest_solution'])
print '  {} unique end states'.format(stats['number_of_unique_end_states'])

# for board in solution:
#   print(board)
#   print
