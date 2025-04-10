# Connect4AIProject

Connect4 - Python Implementation
Overview
This is a Python implementation of the Connect Four game where two players compete against each other. Player 1 is a human, while Player 2 can be either another human or an AI agent. The game supports multiple AI strategies, ranging from random moves to advanced decision-making using the Minimax algorithm with alpha-beta pruning.

Features
•	Human vs AI: Play against different AI agents.
•	Multiple AI Agents:
o	Random Agent: Selects moves randomly.
o	Smart Agent: Attempts to win or block the opponent's winning move.
o	MiniMax Agent: Uses the Minimax algorithm with alpha-beta pruning for optimal moves.
o	ML Agent (Placeholder): A basic implementation that currently selects random moves but can be extended for machine learning.
•	Game Logic: Handles board creation, move validation, win conditions, and game-ending scenarios.
•	Console-Based Display: The game board is updated and displayed after each move.
Installation & Setup
Prerequisites
Ensure you have Python 3.x installed. You can check your Python version with:
python –version

Cloning the Repository
If you're using Git, clone the repository with:

git clone https://github.com/your-repo/connect-four.git
cd Connect4


## Repository 
You can find the source code and contribute to the project on GitHub:https://github.com/OlaShu112/Connect4-Readme.md


Otherwise, manually download the script
Running the Game
Execution Instructions (For Local Development)
1.	Install Dependencies
pip install -r requirements.txt
2.	Running the AI Agents
MiniMax AI: python src/connect_ai.py --mode ml
Machine Learning Agent: python src/connect_ai.py --mode ml
Random AI (Baseline): python src/connect_ai.py --mode random
3.	Running Tests
pytest src/tests/

Execution Instructions for Google Colab
1.	Install Dependencies
Google Colab comes with a lot of libraries pre-installed. However, if you need additional libraries, simply use the following commands in your notebook
!pip install <library_name>
If pytest is needed, it could be installed by running: !pip install pytest
2.	Mount Google Drive
Before accessing project files, mount Google Drive with the following code:
from google.colab import drive
drive.mount('/content/drive')
The code allow to access file from Google Drive
3.	Running the AI Agents
In Colab, terminal commands like src/connect_ai.py are not needed. Instead, run Python scripts directly in Colab cells. Here’s how you can run the different agents
MiniMax AI: !python src/connect_ai.py --mode minimax
Machine Learning Agent: !python src/connect_ai.py --mode ml
Random AI (Baseline):  !python src/connect_ai.py --mode random
4.	Running Tests
For unit tests: !pytest src/tests/
Google Colab's automatic environment: Colab handles much of the setup, so you don't need to worry about the basic configuration or dependencies for the majority of use cases.
Interactive Execution: You can execute code directly in the notebook cells, making it easy to run and test individual components interactively without worrying about terminal commands.
File Management: You can upload your project files directly into Colab, or if using Google Drive, mount the drive to access your files easily.

Run the game using:
python connect_four.py

You will be prompted to input moves for Player 1, while Player 2 (AI) will make its move automatically.
How to Play
The game prompts Player 1 to choose a column (0-6) to drop a disc.
Player 2 (AI) makes a move based on the selected agent.
The game alternates turns until one player wins by aligning four discs (horizontally, vertically, or diagonally), or the board is full, resulting in a draw.

Game Board Display
The board consists of 6 rows × 7 columns and is updated after every move:

' ' → Empty slot
'●' → Player 1's disc
'○' → Player 2's disc
 
---------------
Available AI Agents
1.	RandomAgent: Selects a random column.
2.	SmartAgent: Tries to win or block an opponent’s winning move.
3.	MiniMaxAgent: Uses Minimax with alpha-beta pruning for optimal play.
4.	MLAgent (Placeholder): Currently makes random moves but can be extended with machine learning.


Code Structure

File	Description
connect4.py	
The main script that runs the game loop

GameBoard	Handles board state, move validation, and win checking
RandomAgent	AI agent that selects random moves
SmartAgent	AI agent that tries to win or block an opponent’s win
MiniMaxAgent	AI agent implementing Minimax with alpha-beta pruning
MLAgent	A placeholder for potential ML-based decision-making

Customization
Change AI Agent: Modify the last lines in connect_four.py to switch AI agents:

agent1 = RandomAgent()  # Replace with SmartAgent or MiniMaxAgent
agent2 = MiniMaxAgent()  # Replace with MLAgent for the ML-based player

Adjust Minimax Depth (for difficulty tuning):
In MiniMaxAgent, modify:

self.depth = 3  # Increase for stronger AI, decrease for faster gameplay

Implement a GUI: The game is currently console-based, but it can be extended with Pygame or Tkinter.

Future Improvements
✅ Enhance the ML Agent with machine learning (e.g., reinforcement learning).
✅ GUI Version using Pygame for better visuals.
✅ More AI Strategies like Monte Carlo Tree Search (MCTS).


Game Session
Player1's turn (Human) - ●
Choose a column (0-6): 3
 

---------------
Player2's turn (MiniMaxAgent)
 
---------------
...
Player ● wins!

Acknowledgements

The game logic and AI strategies are based on classic Connect Four rules.
Minimax with Alpha-Beta Pruning is a common AI technique for two-player games.

References
# Minimax algorithm implementation adapted from:
Minimax Algorithm in Game Theory | Set 4 (Alpha-Beta Pruning) - GeeksforGeeks
# MiniMax Agent with Alpha-Beta Pruning - Google Search






