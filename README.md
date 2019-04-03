# minesweeper_solver

Minesweeper Solver is simply a personal project I took up to round out my coding skills. In it I implement minesweeper in Python 3 with the Pygame library. In it I implemented the game as well as algorithms to solve it. 

To play the game and see demonstrations of the algorithms, make sure Python 3 and pygame are installed and run the following commands from the top level directory:

```bash
$ python3 playgame.py
$ python3 showalgorithm.py
```
Add a -h to see options. There are options to change the display style and difficulty (size of the game) for both commands, but most importantly showalgorithm.py can display different algorithms

```bash
$ python3 showalgorithm.py -m {human,exhaustive,hybrid}
```

Also, check out theory/theory.pdf to read about the development of the solving algorithms. The main files of interest beyond that are solve.py, game.py and display.py
