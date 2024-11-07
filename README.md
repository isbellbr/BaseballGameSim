# BaseballGameSim
**Inspiration**

Watching the World Series in 2022, I noticed that the managers of the Houston Astros and Philadelphia Phillies made several decisions that seemingly worsened their odds of winning the game. For example, manager Rob Thomson's decision to bat right fielder Nick Castellanos in the 5th spot of his lineup seemed rather questionable. Given Castellanos' poor hitting that season, it made sense to place him at the bottom of the lineup. To determine the validity of my observations and theories, I created this simulation to determine whether certain lineup and/or game decisions would help the World Series teams win more games.

**What it does**

Presents the user with a choice between three options:

1. Simulate one game and receive a game recap. A game recap consists of a box score and succinct summary of all scoring plays in the game. <br />
2. Simulate one game and receive a detailed play-by-play description of the game. This option also provides a box score following the play-by-play description. <br />
3. Simulate many games (determined by user input). Prints to the console the winning percentages of both teams in the amount of games specified by the user.

**How I built it**

The program was written with Python and utlized the Pandas library.

**Future Goals**

I hope to configure the program in a way in which data can be read in from Baseball Reference so that all 30 MLB teams and their current players can be used in the program. I also want to adjust the way the program determines the outcome of an at-bat in a way that is more realistic. Currently, the program weights the statistics of the batters too heavily. Lastly, I would like to turn this program into a web application so that it is more user-friendly and aesthetically-pleasing.

**Website**

https://baseballgamesim.onrender.com/
