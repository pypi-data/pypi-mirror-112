# python-draughts

[![PyPI version](https://badge.fury.io/py/python-draughts.svg)](https://badge.fury.io/py/python-draughts)

*Based on [ImparaAI/checkers](https://github.com/ImparaAI/checkers) and using various concepts from [RoepStoep/draughtsnet](https://github.com/RoepStoep/draughtsnet).*

A Python3 library that you can use to play a game of draughts. This is just a set of classes that you can use in your code, it's not an interactive shell draughts game (unlike [python-chess](https://pypi.python.org/pypi/python-shogi) and [python-shogi](https://pypi.python.org/pypi/chess) for the games [chess](https://en.wikipedia.org/wiki/Chess) and [shogi](https://en.wikipedia.org/wiki/Shogi) respectively).

## Assumptions

The rules used are for competitive [International draughts *(also called Polish draughts or International checkers)*](https://en.wikipedia.org/wiki/International_draughts). This means a 10x10 board with force captures and regular kings. Also supporting various other draughts variant ([description on supported variants](https://lidraughts.org/variant)).

Each position on the board is numbered 1 to 50. Each move is represented as an array with two values: `starting position` and `ending position`. So if you're starting a new game, one of the available moves is `[9, 13]` for player 1. If there's a capture move, the ending position is the position the capturing piece will land on (i.e. two rows from its original row), which might look like `[13, 22]`.

Each piece movement is completely distinct, even if the move is part of a multiple capture series. In [Portable Draughts Notation](https://en.wikipedia.org/wiki/Portable_Draughts_Notation) mutli-capture series are usually represented by a `5-32` (for a particularly long series of jumps), but in certain situations there could be multiple pathways to achieve that final position. This game requires an explicit spelling out of each distinct move in the multi-capture series.

*Note: Just examples, not necessarily legal positions/moves.*

## Usage

- Create a new game:

```python
from checkers.game import Game

game = Game()
```

- See whose turn it is:

```python
game.whose_turn() #1 or 2
```

- Get the possible moves:

```python
game.get_possible_moves() #[[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]
```

- Make a move:

```python
game.move([9, 13])
```

- Check if the game is over:

```python
game.is_over() #True or False
```

- Find out who won:

```python
game.get_winner() #None or 1 or 2
```

- Review the move history:

```python
game.moves #[[int, int], [int, int], ...]
```

Change the consecutive noncapture move limit (default `40` according to the [rules](http://www.usacheckers.com/rulesofcheckers.php)):

```python
game.consecutive_noncapture_move_limit = 20
game.move_limit_reached() #True or False
```

- Review the pieces on the board:

```python
for piece in game.board.pieces:
	piece.player #1 or 2
	piece.other_player #1 or 2
	piece.king #True or False
	piece.captured #True or False
	piece.position #1-32
	piece.get_possible_capture_moves() #[[int, int], [int, int], ...]
	piece.get_possible_positional_moves() #[[int, int], [int, int], ...]
```

## To do

- [ ] Fix [tests dir](/tests) to test code each commit.

## Acknowledgements

- [ImparaAI/checkers](https://github.com/ImparaAI/checkers) for creating a 8x8 draughts library.
- [RoepStoep/draughtsnet](https://github.com/RoepStoep/draughtsnet) for various python concepts to help create this library.
- [AttackingOrDefending/lidraughts-bot](https://github.com/AttackingOrDefending/lidraughts-bot) for implementing [ImparaAi/checkers](https://github.com/ImparaAi/checkers) for variants and 10x10 international draughts for a [lidraughts-bot](https://lidraughts.org/api#tag/Bot).