import random
import copy
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=pd.errors.DtypeWarning)
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from Connect4Console.game_logic import PLAYER1, PLAYER2



# ================================
# Random AI Agent
# ================================
class RandomAgent:
    """An AI that selects a random available move."""
    def get_move(self, game_board):
        """Chooses a random column from available moves."""
        available = game_board.available_moves()
        return random.choice(available)


# ================================
# Smart AI Agent (Rule-Based)
# ================================
class SmartAgent:
    """A rule-based AI that prioritizes winning moves and blocking the opponent."""
    def get_move(self, game_board):
        """Decides the best move using a simple rule-based strategy.""" 
        for col in game_board.available_moves():
            temp_board = copy.deepcopy(game_board)
            row, _ = temp_board.drop_disc(col, '○')
            if temp_board.is_winning('○'):
                return col
        for col in game_board.available_moves():
            temp_board = copy.deepcopy(game_board)
            row, _ = temp_board.drop_disc(col, '●')
            if temp_board.is_winning('●'):
                return col
        return random.choice(game_board.available_moves())


# ================================
# MiniMax AI Agent (With Alpha-Beta Pruning)
# ================================
class MiniMaxAgent:
    """An AI that uses the MiniMax algorithm with alpha-beta pruning for decision-making."""
    def __init__(self, depth=3):
        """Initializes the AI with a given search depth."""
        self.depth = depth

    def get_move(self, game_board):
        """Determines the best move using the MiniMax algorithm."""
        best_move = None
        best_score = -float('inf')

        for col in game_board.available_moves():
            temp_board = copy.deepcopy(game_board)
            temp_board.drop_disc(col, PLAYER2)
            score = self.minimax(temp_board, self.depth, -float('inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = col
        return best_move

    def minimax(self, board, depth, alpha, beta, is_maximizing_player):
        """MiniMax algorithm with alpha-beta pruning to optimize move selection."""

        # Base case: game over or depth limit reached
        if depth == 0 or board.is_winning(PLAYER1) or board.is_winning(PLAYER2) or board.is_full():
            return self.evaluate_board(board)

        if is_maximizing_player:
            max_eval = -float('inf')
            for col in board.available_moves():
                temp_board = copy.deepcopy(board)
                temp_board.drop_disc(col, PLAYER2)
                eval = self.minimax(temp_board, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for col in board.available_moves():
                temp_board = copy.deepcopy(board)
                temp_board.drop_disc(col, PLAYER1)
                eval = self.minimax(temp_board, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def evaluate_board(self, board):
        """Evaluates the board and returns a score indicating the favorability for PLAYER2."""
        score = 0

        # Define patterns and their corresponding scores
        patterns = {
            (PLAYER2, PLAYER2, PLAYER2, PLAYER2): 100,  # Four in a row (win)
            (PLAYER2, PLAYER2, PLAYER2, ' '): 5,       # Three in a row with an empty space
            (PLAYER2, PLAYER2, ' ', ' '): 2,           # Two in a row with two empty spaces
            (PLAYER1, PLAYER1, PLAYER1, PLAYER1): -100, # Opponent's four in a row (loss)
            (PLAYER1, PLAYER1, PLAYER1, ' '): -5,      # Opponent's three in a row with an empty space
            (PLAYER1, PLAYER1, ' ', ' '): -2           # Opponent's two in a row with two empty spaces
        }

        # Check all possible lines of four in the board
        for row in range(6):
            for col in range(7):
                # Horizontal
                if col + 3 < 7:
                    line = (board.board[row][col], board.board[row][col+1], board.board[row][col+2], board.board[row][col+3])
                    score += patterns.get(line, 0)
                # Vertical
                if row + 3 < 6:
                    line = (board.board[row][col], board.board[row+1][col], board.board[row+2][col], board.board[row+3][col])
                    score += patterns.get(line, 0)
                # Diagonal down-right
                if row + 3 < 6 and col + 3 < 7:
                    line = (board.board[row][col], board.board[row+1][col+1], board.board[row+2][col+2], board.board[row+3][col+3])
                    score += patterns.get(line, 0)
                # Diagonal up-right
                if row - 3 >= 0 and col + 3 < 7:
                    line = (board.board[row][col], board.board[row-1][col+1], board.board[row-2][col+2], board.board[row-3][col+3])
                    score += patterns.get(line, 0)

        return score


# ================================
# Machine Learning Agent (Placeholder)
# ================================
class MLAgent:
    """An AI model trained using machine learning techniques for Connect 4."""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.board_columns = 7  # Connect 4 has 7 columns
        self.board_rows = 6     # Connect 4 has 6 rows

    def train_model(self, data_path):
        """Loads dataset, processes data, and trains the AI model."""
        
        # Define column names
        column_names = ['col' + str(i) for i in range(1, 42)] + ['outcome']

        # Load dataset and suppress warning
        df = pd.read_csv(data_path, names=column_names)

        # Convert all data to numeric where possible (e.g., handling 'pos_01' like values)
        df = df.apply(pd.to_numeric, errors='coerce')

        # Handle potential missing or non-numeric values
        df.fillna(0, inplace=True)  # Replace NaN values with 0 for the board columns

        # Ensure the 'outcome' column is numeric (or map categorical to numeric)
        df['outcome'] = pd.to_numeric(df['outcome'], errors='coerce')
        df['outcome'].fillna(0, inplace=True)  # Replace non-numeric with 0 (loss)

        # Split the data into features and target
        X = df.drop(columns=['outcome'])
        y = df['outcome']

        # Encode the outcomes as 1 (win) and 0 (loss)
        y = self.label_encoder.fit_transform(y)

        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the Random Forest model
        self.model.fit(X_train, y_train)

        # Check the accuracy of the model
        accuracy = self.model.score(X_test, y_test)
        print(f"Model accuracy: {accuracy*100:.2f}%")

    def predict_move(self, board):
        """Predicts the best move for the AI agent."""
        # Flatten the board into a 1D array (to match the model's input format)
        board_flat = self.flatten_board(board)

        # Predict the move using the trained model
        prediction = self.model.predict([board_flat])
        return prediction[0]

    def flatten_board(self, board):
        """Flattens the board into a 1D array for the model input."""
        return [board.board[row][col] for row in range(self.board_rows) for col in range(self.board_columns)]