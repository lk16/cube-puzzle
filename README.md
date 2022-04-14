# Cube puzzle

This repo implements two brute-force solvers for a wooden puzzle. The puzzle consists of a 64 block long snake that should be shaped into a 4x4x4 cube, see image below. ([image source](http://www.dr-karstens.de/snake.html))

![image](image.jpg)

The puzzle has (including rotations and mirroring) 192 solutions.

## Python implementation

Run with `python python/cube.py >python/solutions.txt 2>python/stats.txt`.
Does the job, but takes about [11.5 minutes](python/stats.txt) on my machine.

## C implementation

Compile with `gcc c/cube.c -Wall -Wextra -Ofast -o c/cube`.
Run with `./c/cube >c/solutions.txt 2>c/stats.txt`.
Takes about [1.6 seconds](c/stats.txt) on my machine.
