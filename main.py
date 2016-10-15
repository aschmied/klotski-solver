import time

import p1.solver

t0 = time.time()
solver = p1.solver.Solver()
solutions, stats = solver.solve()
t1 = time.time()

print 'Finished in {} seconds'.format(t1 - t0)
print '  {} unique solutions'.format(stats['number_of_solutions'])
print '  {} moves in shortest solution'.format(stats['length_of_shortest_solution'])
print '  {} moves in longest solution'.format(stats['length_of_longest_solution'])
print '  {} unique end states'.format(stats['number_of_unique_end_states'])
