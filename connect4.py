import pygame
from game_board import GameBoard
from agents import RandomAgent, SmartAgent, MiniMaxAgent
import time
from agents import MLAgent
import os
from music import MusicPlayer
from game_logic import PLAYER1, PLAYER2






# ================================
# Game Loop 
# ================================
def get_human_move():
    """Handles human player's input with validation."""
    while True:
        try:
            col = int(input("Choose a column (0-6): "))
            if 0 <= col <= 6:
                return col
            else:
                print("Invalid column. Please enter a number between 0 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid number between 0 and 6.")

def play_game(agent1, agent2):
    """Runs a game between two players (human or AI)."""
    pygame.init()  # Initialize pygame before the game loop
    game_board = GameBoard()
    current_player = PLAYER1
    music_player.play_music()   # Start music before the game loop

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                music_player.change_music_forward()  # Play new music track when the current one ends

            # ✅ Added music controls using arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:      # Play music
                    music_player.play_music()
                elif event.key == pygame.K_DOWN:  # Stop music
                    music_player.stop_music()
                elif event.key == pygame.K_LEFT:  # Previous track
                    music_player.change_music_backward()
                elif event.key == pygame.K_RIGHT: # Next track
                    music_player.change_music_forward()

        if current_player == PLAYER1:
            print("Player1's turn (Human) - ●")
            col = get_human_move()  # Get valid input from human player
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
        game_board = GameBoard()  # Reset the game board for a new game
        play_game(agent1, agent2)  # Restart the game if 'Y' is selected
    else:
        print("Thanks for playing!")

    pygame.quit()  # Clean up and quit pygame when the game ends

# ================================
# Main Execution 
# ================================
if __name__ == "__main__":
    # Define paths for the dataset files
    data_path = "C:/Users/Admin/OneDrive/Desktop/Connect4AIProject/src/connect4_dataset/connect-4.data.csv"
    #names_path = "C:/Users/Admin/OneDrive/Desktop/Connect4AIProject/src/connect4_dataset/connect-4.names"


    # Create an instance of MLAgent
    agent1 = MLAgent()  # ML-based player using the machine learning agent
    agent2 = MiniMaxAgent()  # Replace with another agent (e.g., RandomAgent, SmartAgent)

    # Train the ML agent with the dataset
    agent1.train_model(data_path)  # Provide the path to the dataset

    print("Model training complete. Now initializing music player...")
    # Initialize music player
    music_player = MusicPlayer()

    # Play the game with agent1 (MLAgent) and agent2 (MiniMaxAgent or another agent)
    play_game(agent1, agent2)
