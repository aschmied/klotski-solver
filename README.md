## Klotski Solver

A short Python 2.7 program to solve the Klotski (a.k.a. Square Root, Pioneer 1) puzzle game.

## Code Example

Running it:

```
$ python main.py 
Finished in 8.9454369545 seconds
  964 unique solutions
  85 moves in shortest solution
  125 moves in longest solution
  964 unique end states
  25955 board configurations examined
  65880 board configurations total (39925 unreachable)
```

## Motivation

When I was about 10 years old my grandmother gave me the [Klotski](https://en.wikipedia.org/wiki/Klotski) puzzle game (also called the [Square Root puzzle](http://squarerootgames.com/puzzles.html) and Pioneer 1) as a gift. Twenty years later I had only solved it once. It was time for a new approach.

## Analysis

Before writing a program to solve the puzzle I convinced myself that it was feasible. The number of possible configurations of pieces on the board provides an upper bound on the number of states that the program must examine. Since there are 10 pieces, so I estimated the number of board configurations as 10! ~ 3.6 million. This is a coarse estimate. Some unique board configurations are uncounted because sliding a piece left or right can produce a new board configuration while retaining the same ordering. On the other hand there are four identical small squares and four identical tall rectangles, so we can remove two factors of 4!.

At this point I was sufficiently convinced.

## Solution Design

Assuming my estimate of 3 million board configurations is accurate then it is feasible to examine them all. I model the game with an undirected graph. Imagine each board configuration is assigned to a node in the graph. An edge `(u, v)` is introduced for each pair of board configurations where the board may be moved from the configuration represented by `u` to the configuration represented by `v` with a single move. Then a path from the initial board configuration to a solved configuration represents a solution to the puzzle.

This program uses a breadth first search to traverse the graph. It does not explicitly construct the graph. Instead it begins by constructing a representation of the initial board configuration. It then determines the board configurations reachable in one move from the first configuration and adds them to a queue for subsequent processing. It then pops the next configuration from the front of the queue, finds the next reachable configurations, enqueues them, and repeats.

The program keeps track of all previously enqueued configurations to ensure that each configuration is examined exactly once. Finally, before being enqueued each configuration is examined to determine whether it is a solved configuration.

## Results

The shortest solution this program finds is 85 moves. The [Wikipedia article](https://en.wikipedia.org/wiki/Klotski) reports a solution of 81 moves, but they count moving a piece by two squares in the same direction as a single move whereas this program counts it as two. Also the starting configurations differ between the Klotski variant this program solves (Pioneer 1) and the variant described in the Wikipedia article.

The program examines 25,955 unique board configurations. The search is exhaustive, so this is the number of configurations reachable from the initial configuration. This made me wonder if there exist any unreachable configurations, so I wrote a backtracking search to count the number of possible configurations (both reachable and unreachable from the start configuration). There were 65880 (39925 unreachable). I wonder how many connected components are in the graph that models all board configurations.

## Complexity

The queue is a Python `collections.deque`. Its `append` and `pop` are O(1). The visited configurations are stored in a `set`. The `add` and `in` operations on a `set` have average complexity O(1) and worst case O(N). Breadth first search has complexity O(V+E) where V is the number of board configurations and E is the number of transitions between them. Membership in the set of visited configurations is checked for each transition and the number of elements in the set of visited configurations is bounded by the number of board configurations V. Therefore the program has average complexity O(V+E) and worst case complexity O((V+E) * V).

## Tests

There are tests for the board module. Run them with `python klotski/board_test.py`.

## License: 2-clause BSD

Copyright (c) 2016, Anthony Schmieder
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
