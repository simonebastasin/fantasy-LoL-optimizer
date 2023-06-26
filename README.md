# Optimizer for League of Legends fantasy game competitions

**Mathematical optimization of a linear programming problem using the CPLEX Optimizer**

## How it works

Considering the European professional League of Legends league (LEC), there is the related online fantasy game competition open to everyone.

In League of Legends games are played 5v5 (between two teams) and there are 5 standard roles that each team must cover in a game. So, in a team each of the 5 players covers a different role. There can be other players on the bench. In LEC there are 10 teams and more than 50 players.

For each week, fantasy game participants make their own custom team based on which real team and which players will play better according to them. To create a complete custom team you have to pick the representing team and 5 players (one per role). Each week, players and teams gain points based on their performance. The amount of points that they are going to get at the end of the current week is what we want to predict. So as to predict the best custom team of the week. The problem is that all of these picks (players and teams) have a salary to get paid and fantasy game participants have a fixed budget that they cannot exceed. For each possible pick there are some statistics available, among which for players: name, role, team, pointsPerGame, salary. The pointsPerGame value, also available for teams, is the average of points per game obtained in previous weeks by that pick.

To predict the best custom team of the week we maximize the sum of pointsPerGame of the picks of every possible custom team, that is not exceeding the budget. This is a linear programming problem solved using CPLEX Optimizer.

## Example

The proposed example is about the week 8 of a past LEC season.

- *content_8.txt:* input file
- *intented_content_8.txt:* intented input file with only interesting data
- *picks_week_8.txt:* output file with the 10 best possible custom team choices