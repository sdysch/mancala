![Test](https://github.com/sdysch/mancala/actions/workflows/test.yml/badge.svg)
# mancala
Exploring different strategies for the board game [mancala](https://en.wikipedia.org/wiki/Mancala), also known as Kalaha.

## Rules
* WIP

## Blog post
* WIP

## Strategies

| Strategy        | Explanation                                                                                                                             |
| --------        | -----------                                                                                                                             |
| Random          | Moves are chosen with an equal probability                                                                                              |
| Max score       | The move which maximises the player's score is chosen. If multiple moves give the same max score, choose randomly                       |
| Exact Random    | If possible, choose a move which ends in player's goal. Otherwise, use random strategy                                                  |
| Exact Max Score | Same as Exact Random, except that the fallback strategy is Max score                                                                    |
| Max marbles     | Choose the move which has the most marbles. If multiple moves fit this criteria, choose randomly                                        |
| Max moves       | The move which maximises the number of moves a player makes is chosen. If multiple moves give the same number, choose randomly          |



## Player 1 win probabilities
[![Player 1 win probability](plots/player_1_win_probs.png)](plots/player_1_win_probs.png)

## Todo list
Current to do list: [here](TODO.md)
