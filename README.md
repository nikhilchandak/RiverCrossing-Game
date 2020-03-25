# Game

Game made using PyGame for ISS course. 

Run the game via the following command: 

    python3 river_game.py
    
# Controls

Up, Down, Left, Right keys for Player1

W, S, A, D keys for Player2

# Scoring Criteria

5 points are awarded for crossing fixed obstacles, 10 points for crossing moving obstacles.

If a player completes the round, points are also added inversely proportional to the time taken.

# Technical Details

Game lasts for 4 rounds. The next player automatically starts if a player dies or reachers the other end. Final Scores are reported after the game ends. 
Functionality to play again is also present.

The number of moving, fixed obstacles and their speed, position is randomly generated. Moving obstacles move left to right, wraping around the screen. 

The player's position is also randomly generated such that it does not collide with any other obstacle when they are spawned on the screen.
If by the end of some round, a player has more wins (i.e. not died via colliding) than other player, then the speed of the player and the obstacles increases to make it
more challenging for him to cross the river. 

