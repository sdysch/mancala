# mancala
Exploring different strategies for [mancala](https://en.wikipedia.org/wiki/Mancala)

* Player 1 is the player to move first

## Bucket numbering
* A board is represented like so:
```
        6 6 6 6 6 6
[0]                      [0]
        6 6 6 6 6 6

```
* Player 1's cups are numbered from left to right
* Player 2's cups are numbered from _right to left_
* Player 1's goal is on the right, player 2's is on the left
```
Bucket  6 5 4 3 2 1

        6 6 6 6 6 6
[0]                      [0]
        6 6 6 6 6 6
        
Bucket  1 2 3 4 5 6

```
## Strategies
- [X] Random:
	* Player's moves are selected with equal probabilitiy from available moves
- [ ] Max score:
	* Player's moves are chosen by the one which maximises the increase in score from the move
	* Requires implementation of deep copying of Board class
- [ ] Minimax algorithm:
	* More complicated, requires depth parameter and alpha/beta pruning (for no crazy runtimes)
- [ ] Reinforecment learning

## TODO
- [ ] Loop over different marble and cups


## Investigations
- [ ] Win rate vs player
- [ ] Win rate vs first move
- [ ] Win rate vs n_marbles/n_buckets
- [ ] Win rate vs n_moves
