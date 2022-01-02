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
* Player 1's buckets are numbered from left to right
* Player 2's buckets are numbered from _right to left_
* Player 1's goal is on the right, player 2's is on the left
```
Bucket  6 5 4 3 2 1

		6 6 6 6 6 6
[0]                      [0]
		6 6 6 6 6 6
		
Bucket  1 2 3 4 5 6

```
