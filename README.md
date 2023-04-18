# PlayPal
### Game Application with a user interface that allows users to play tic-tac-toe games against different difficulty AI Players and check their own statistics.
- 1000 randomly generated users created with 10000 games simulated to initialize the game data.
- Programmed with Python (PyRedis).
## To Run:
- download all files into a folder or clone the repository
#### Option 1:
- open the folder in a preferred compiler
- run the 'load_users_games.py' file
- run the 'playpal_app.py' file 
#### Option 2:
- open the folder in your device's termial or command prompt
- run the 'load_users_games' file
- run the 'playpal_app.py' file
Files can be run in the command line using 'python <filename>' or 'python3 <filename>'

## Files:
- ai_player.py: programming for the AI players 
- board.py: creates the tic-tac-toe board
- create_user_table.py: randomly generates 1000 users with IDs and passwords
- game.py: simulates a tic-tac-toe game
- game_data.csv: .csv file containing simulated game data
- game_data_generator.py: generates 10000 game results between existing users
- learning_demo.py: demo for reinforcement learning of AI players
- load_users_games.py: loads a users' game history from the .csv files
- new_game.py: plays a new tic-tac-toe game
- player.py: programming for the user player 
- playpal_app.py: runs the application
- playpal_redis.py: connects the application to the redis database for information storage and retrieval
- s_board.py: standardizes game board positions
- user_table.csv: .csv file containing generated user data
