import random 
import copy 

# Constants for the players
PLAYER1 = '●'  # Human player
PLAYER2 = '○'  # AI player
# ================================ 
# Game Board Class 
# ================================

# Game Board Class
class GameBoard:
    """Represents the Connect Four game board."""
    def __init__(self):
     """Initialises an empty 6x7 game board."""
     self.board = [[' ' for _ in range(7)] for _ in range(6)]
        
    def print_board(self):
        """Prints the current game board to the console."""
        print('\n'.join(['|'.join(row) for row in self.board]))
        print('-' * 15)
    
    def is_full(self):
        """Checks if the board is completely filled."""
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    def is_winning(self, player):
        """Determines if the given player has won the game."""
        # Check horizontal, vertical, and diagonal for a win
        for row in range(6):
            for col in range(7):
                if self.check_win(player, row, col):
                    return True
        return False
    
    def check_win(self, player, row, col):
        """Checks if a player has four connected pieces in any direction."""
        # Horizontal
        if col + 3 < 7 and all(self.board[row][col + i] == player for i in range(4)):
            return True
        # Vertical
        if row + 3 < 6 and all(self.board[row + i][col] == player for i in range(4)):
            return True
        # Diagonal (down-right)
        if row + 3 < 6 and col + 3 < 7 and all(self.board[row + i][col + i] == player for i in range(4)):
            return True
        # Diagonal (up-right)
        if row - 3 >= 0 and col + 3 < 7 and all(self.board[row - i][col + i] == player for i in range(4)):
            return True
        return False

    def available_moves(self):
        """Returns a list of columns where a move can be made."""
        return [col for col in range(7) if self.board[0][col] == ' ']
    
    def drop_disc(self, col, player):
        """Places a player's disc in the lowest available row of the selected column."""
        for row in range(5, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = player
                return row, col

# ================================ 
# Random AI Agent 
# ================================
# Random Agent
class RandomAgent:
    """An AI that selects a random available move."""

    def get_move(self, game_board):
        """Chooses a random column from available moves."""
        available = game_board.available_moves()
        return random.choice(available)

# ================================ 
# Smart AI Agent (Rule-Based) 
# ================================
# Smart Agent (Rule-based)
class SmartAgent:
    """A rule-based AI that prioritises winning moves and blocking the opponent."""
    def get_move(self, game_board):
        """Decides the best move using a simple rule-based strategy.""" 

        # Step 1: Check if AI can win in the next move
        for col in game_board.available_moves():
            temp_board = copy.deepcopy(game_board)
            row, _ = temp_board.drop_disc(col, PLAYER2)
            if temp_board.is_winning(PLAYER2):
                return col

        # Step 2: Block opponent's winning move
        for col in game_board.available_moves():
            temp_board = copy.deepcopy(game_board)
            row, _ = temp_board.drop_disc(col, PLAYER1)
            if temp_board.is_winning(PLAYER1):
                return col
        
        # Step 3: No immediate win or block, so pick any valid move
        return random.choice(game_board.available_moves())

# ================================ 
# MiniMax AI Agent (With Alpha-Beta Pruning)
 # ================================
class MiniMaxAgent:
    """An AI that uses the MiniMax algorithm with alpha-beta pruning for decision-making."""
    def __init__(self, depth=3):
        """Initialises the AI with a given search depth."""
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
        """MiniMax algorithm with alpha-beta pruning to optimise move selection."""

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
        """Evaluates the board to assign a score to the current state."""
        if board.is_winning(PLAYER2):
            return 1000 # AI win
        elif board.is_winning(PLAYER1):
            return -1000 # Opponent win
        else:
            return 0  # Basic heuristic, can be improved

# ================================ 
# Machine Learning Agent (Placeholder)
 # ================================
class MLAgent:
    """A placeholder for an AI model trained using machine learning techniques."""
    def __init__(self):
        pass

    def train_model(self, data):
        """Placeholder method for training an ML model."""
        pass

    def get_move(self, game_board):
        """Selects a move randomly (to be replaced with ML-based decision-making)."""
        return random.choice(game_board.available_moves())

# ================================
 # Game Loop 
# ================================
def play_game(agent1, agent2):
    """Runs a game between two players (human or AI)."""
    game_board = GameBoard()
    current_player = PLAYER1
    while True:
        if current_player == PLAYER1:
            print("Player1's turn (Human) - ●")
            col = int(input("Choose a column (0-6): ")) # Human input
        else:
            print(f"Player2's turn ({agent2.__class__.__name__})")
            col = agent2.get_move(game_board) # AI decision
        
        if col not in game_board.available_moves():
            print("Invalid move. Try again.")
            continue
        
        row, col = game_board.drop_disc(col, current_player)
        game_board.print_board()

# Check for win or draw conditions
        if game_board.is_winning(current_player):
            print(f"Player {current_player} wins!")
            break
        elif game_board.is_full():
            print("The game is a draw.")
            break
     
# Switch turns   
        current_player = PLAYER1 if current_player == PLAYER2 else PLAYER2
# ================================ 
# Main Execution 
# ================================
if __name__ == "__main__":
    agent1 = RandomAgent()  # Replace with SmartAgent or MiniMaxAgent as needed
    agent2 = MiniMaxAgent()  # Replace with MLAgent for the ML-based player

    play_game(agent1, agent2)
