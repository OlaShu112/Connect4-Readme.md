import random
import copy
import pygame
import time


# Initialize pygame mixer
pygame.mixer.init()

# Constants for the players
PLAYER1 = '●'  # Human player
PLAYER2 = '○'  # AI player

# List of music files with absolute or relative paths
music_files = [
    "assets/AyraStar_Music.wav",
    "assets/Cr&AS_Ngozi_Music.wav",
    "assets/DarkooFtRema_Music.wav",
    "assets/MohBad_Music.wav",
    "assets/music.wav",
    "assets/Teni_Malaika_Music.wav"
]

def play_background_music():
    """Plays a random music file and ensures continuous looping."""
    try:
        music_file = random.choice(music_files)
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        print(f"Now playing: {music_file}")

        # Set an event when music ends
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    except pygame.error as e:
        print(f"Error loading or playing music file '{music_file}': {e}")



# ================================
# Game Board Class
# ================================

class GameBoard:
    """Represents the Connect Four game board."""
    
    def __init__(self):
        """Initializes an empty 6x7 game board."""
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
    
    def print_board(self):
        """Prints the game board with each entry inside a box."""
        print("\n  0   1   2   3   4   5   6  ")  # Column indices for reference
        print("+" + "---+" * 7)  # Top border

        for row in self.board:
            print("| " + " | ".join(row) + " |")  # Each cell inside a box
            print("+" + "---+" * 7)  # Row separator

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
    play_background_music()  # Start music before the game loop

    running = True
    while running:
        # Check if music has stopped, then play another track
        if not pygame.mixer.music.get_busy():
            play_background_music()

        if current_player == PLAYER1:
            print("Player1's turn (Human) - ●")
            col = int(input("Choose a column (0-6): "))  # Human input
        else:
            print(f"Player2's turn ({agent2.__class__.__name__})")
            col = agent2.get_move(game_board)  # AI decision

        if col not in game_board.available_moves():
            print("Invalid move. Try again.")
            continue

        row, col = game_board.drop_disc(col, current_player)
        game_board.print_board()

        # Check for win or draw conditions
        if game_board.is_winning(current_player):
            print(f"Player {current_player} wins!")
            running = False  # Stop the game loop
            break
        elif game_board.is_full():
            print("The game is a draw.")
            running = False  # Stop the game loop
            break

        # Switch turns
        current_player = PLAYER1 if current_player == PLAYER2 else PLAYER2

        time.sleep(0.1)  # Small delay to avoid high CPU usage

    # After the game ends, ask the user if they want to play again
    play_again = input("Do you want to play again? (Y/N): ").lower()
    if play_again == 'y':
        play_game(agent1, agent2)  # Restart the game if 'Y' is selected
    else:
        print("Thanks for playing!")

# Assuming the rest of the game logic, including GameBoard, PLAYER1, PLAYER2, and agent classes are implemented properly.

# ================================ 
# Main Execution 
# ================================
if __name__ == "__main__":
    agent1 = RandomAgent()  # Replace with SmartAgent or MiniMaxAgent as needed
    agent2 = MiniMaxAgent()  # Replace with MLAgent for the ML-based player

    play_game(agent1, agent2)
