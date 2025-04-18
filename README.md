# Connect4 AI – GUI Version

A Python-based Connect Four game featuring a **graphical user interface** (GUI) and multiple intelligent AI agents. Built with **Pygame**, this project allows you to play against various types of AI, from simple random agents to strategic algorithms like **Minimax with alpha-beta pruning**.

## Features

GUI-Based Gameplay using Pygame.
Game Modes:
Human vs Human: Play against another human player on the same device.
Human vs Smart Agent: Play against a strategic AI that attempts to block or win.
Human vs Random Agent: Play against an AI that makes random moves.
Human vs MiniMax Agent: Play against an AI that uses Minimax with alpha-beta pruning.
Human vs MLAgent: Play against an AI that uses machine learning (currently a placeholder).

AI vs AI: Let two AI agents play against each other. You can choose from:
RandomAgent
SmartAgent
MiniMaxAgent
MLAgent

Human vs ML Agent (Placeholder): Play against a future machine learning-based agent (currently a placeholder).

AI Agents Included:
🔹 RandomAgent: Chooses legal moves randomly.
🔹 SmartAgent: Attempts to win or block the opponent.
🔹 MiniMaxAgent: Uses Minimax with alpha-beta pruning.
🔹 MLAgent (Placeholder): Placeholder for future ML-based agent.

Background Music via music_player.py.
Modular Codebase for easy modification and extension.


## Installation & Setup

### Prerequisites
- Python 3.x
- Pip package manager

### Install dependencies
```bash
pip install -r requirements.txt

Running the Game (GUI)
Navigate to the src/connect4 directory and launch the game:

cd path/to/Connect4AIProject/src/connect4
python main.py

Project Structure

Connect4AIProject/
├── .venv/                 # Virtual environment files (Git ignored)
└── assets/                # Directory to hold assets like images, music, etc.
└── Images                
└── src/
    └── connect4/
        ├── __init__.py
        ├── main.py
        ├── agents/
        │   ├── __init__.py
        │   ├── random_agent.py
        │   ├── smart_agent.py
        │   ├── minimax_agent.py
        │   ├── ml_agent.py
        ├── game_logic.py
        ├── game_utils.py
        ├── music_player.py
        ├── message.py
        ├── utils.py
        ├── constants.py
        ├── graphics.py
        ├── player_data.py
        ├── player_data.json
        └── README.md  
        └── connect4_dataset/
            ├── connect-4.data
            ├── connect-4.names
                  # Now in connect4_dataset directory




Customization
Choose AI Agents
Edit main.py to configure which AI agents are playing:

from agents import RandomAgent, SmartAgent, MiniMaxAgent, MLAgent

agent1 = RandomAgent()      # e.g., SmartAgent(), MiniMaxAgent()
agent2 = MiniMaxAgent()     # e.g., MLAgent()

Future Improvements
Replace placeholder ML agent with an actual trained model (e.g., reinforcement learning).

Add animations and sound effects to the GUI.

Integrate more advanced AI like Monte Carlo Tree Search (MCTS).

Acknowledgements
Minimax algorithm adapted from:
GeeksforGeeks – Minimax Algorithm in Game Theory (Alpha-Beta Pruning)

Repository
GitHub:https://github.com/OlaShu112/Connect4-Readme.md



1. **Create `.gitignore`**:

```gitignore
__pycache__/
*.pyc
.venv/
assets/*.wav

2. Create requirements.txt:

pygame

3. Initialize and push to GitHub:

git init
git add .
git commit -m "Initial commit: GUI Connect4 with AI agents"
git remote add origin https://github.com/YourUsername/Connect4.git
git push -u origin main

Screenshot 
![alt text](image.png)