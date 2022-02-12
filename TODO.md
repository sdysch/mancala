# To do list
## Strategies
- [X] Random:
	* Player's moves are selected with equal probabilitiy from available moves
- [X] Exact move strategy
- [X] Max score:
	* Player's moves are chosen by the one which maximises the increase in score from the move
	* Requires implementation of deep copying of Board class
	* How to make choice for "Mancala move"?
- [ ] Max moves:
	* Make move which maximises the number of moves a player will make
- [ ] Minimax algorithm:
	* More complicated, requires depth parameter and alpha/beta pruning (for no crazy runtimes)
- [ ] Reinforecment learning
	* Check out keras-rl and gym environment

## TODO
- [X] Move mancala "rules" into Board class
- [X] New rule implementation
- [X] Max moves agent
- [X] max goal (random fall back)
- [X] Completely rewrite make_player_turn - it is buggy (player switching is just plain wrong)
- [ ] Loop over different marble and cups
- [ ] Minimax
- [ ] Multiprocessing


## Investigations
- [ ] Win rate vs first move for different agents (2D plot)
- [ ] Win rate vs n_marbles/n_buckets
