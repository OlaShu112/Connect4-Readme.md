import pygame
import sys
import numpy as np


from connect4.music_player import play_music, stop_music, next_track, previous_track  
from connect4.agents import minimax_agent, random_agent, smart_agent, ml_agent, make_move, check_win, valid_move
from connect4.agents import block_player_move

# Initialize Pygame
pygame.init()

# Constants for game
SQUARE_SIZE = 100  
COLUMN_COUNT = 7  
ROW_COUNT = 6  
WIDTH = COLUMN_COUNT * SQUARE_SIZE  
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE  

# Colours
WHITE = (255, 255, 255)
BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up display
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")

# Font for text
font = pygame.font.SysFont("Arial", 40)

def create_board():
    return [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

def draw_board(board, current_turn):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

            # Draw player pieces
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    # Draw the hovering ball with color based on the current turn
    hover_color = YELLOW if current_turn == 1 else RED
    pygame.draw.circle(screen, hover_color, (pygame.mouse.get_pos()[0] // SQUARE_SIZE * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    pygame.display.flip()

def drop_piece(board, col, player):
    # Ensure col is a valid integer
    col = int(float(col))  # handles both '5' and '5.0'
    if col < 0 or col >= COLUMN_COUNT:
        return -1  # Invalid column index

    for row in range(ROW_COUNT - 1, -1, -1):  # Start from the bottom of the board
        if board[row][col] == 0:  # If the space is empty
            board[row][col] = player  # Drop the piece
            return row  # Return the row where the piece was placed
    return -1  # If the column is full

def main_menu():
    while True:
        screen.fill(BLACK)

        # Display options for 2-Player Game, AI vs AI, and Player vs AI
        text1 = font.render("Press 1 for 2-Player Game", True, WHITE)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3))

        text2 = font.render("Press 2 for AI vs AI", True, WHITE)
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))

        text3 = font.render("Press 3 for Player vs AI", True, WHITE)  # Added Player vs AI option
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 1.5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'human'  # 2-Player Game
                elif event.key == pygame.K_2:
                    return 'ai_vs_ai'  # AI vs AI
                elif event.key == pygame.K_3:
                    return 'player_vs_ai'  # Player vs AI

def difficulty_menu():
    while True:
        screen.fill(BLACK)

        # Display options for Easy, Medium, Hard difficulty, and ML agent
        text1 = font.render("Press 1 for Easy (Random Agent)", True, WHITE)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3))

        text2 = font.render("Press 2 for Medium (Smart Agent)", True, WHITE)
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))

        text3 = font.render("Press 3 for Hard (Minimax Agent)", True, WHITE)
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 1.5))

        text4 = font.render("Press 4 for ML Agent (Advanced AI)", True, WHITE)  # New ML agent option
        screen.blit(text4, (WIDTH // 2 - text4.get_width() // 2, HEIGHT // 1.2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return random_agent  # Easy, Random Agent
                elif event.key == pygame.K_2:
                    return smart_agent  # Medium, Smart Agent
                elif event.key == pygame.K_3:
                    return minimax_agent  # Hard, Minimax Agent
                elif event.key == pygame.K_4:
                    return ml_agent  # ML Agent (Advanced AI)

def display_message(message):
    text = font.render(message, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def ask_play_again():
    while True:
        screen.fill(BLACK)
        text = font.render("Play Again? (Y/N)", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # Continue playing
                if event.key == pygame.K_n:
                    return False  # Go back to the main menu

def game_loop(game_mode, player1_agent, player2_agent):
    while True:
        board = create_board()
        running = True
        turn = 1  # Player 1 starts
        draw_board(board, turn)  # Draw the board with Player 1's color

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        play_music()
                    elif event.key == pygame.K_s:
                        stop_music()
                    elif event.key == pygame.K_RIGHT:
                        next_track()
                    elif event.key == pygame.K_LEFT:
                        previous_track()

                if game_mode == 'human' and event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // SQUARE_SIZE
                    if valid_move(board, col):
                        row = drop_piece(board, col, turn)
                        if row != -1:  # Ensure the move is valid
                            if check_win(board, turn):
                                draw_board(board, turn)
                                display_message(f"Player {turn} wins!")
                                running = False
                            turn = 2 if turn == 1 else 1
                            draw_board(board, turn)

                # AI Logic for AI vs AI
                elif game_mode == 'ai_vs_ai' and turn == 1:
                    col = player1_agent(board, 1)

                    try:
                        col = int(float(col))
                    except (ValueError, TypeError):
                        print(f"Invalid column received from AI Player 1: {col}")
                        col = -1

                    if col == -1:
                        print("Player 1 (Minimax Agent) couldn't find a valid move. Skipping turn.")
                        turn = 2
                    pygame.time.wait(1000)
                    if col != -1:  # Fixed the indentation here
                        row = drop_piece(board, col, turn)
                        if row != -1:
                            if check_win(board, turn):
                                draw_board(board, turn)
                                display_message(f"Player {turn} (Minimax Agent) wins!")
                                running = False
                            turn = 2
                            draw_board(board, turn)
                        pygame.time.wait(1000)

                # Player vs AI Logic
                elif game_mode == 'player_vs_ai' and turn == 1:
                    # Human's turn
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = event.pos[0] // SQUARE_SIZE
                        if valid_move(board, col):
                            row = drop_piece(board, col, turn)
                            if row != -1 and check_win(board, turn):  # Ensure valid drop
                                draw_board(board, turn)
                                display_message(f"Player {turn} wins!")
                                running = False
                            turn = 2  # AI's turn
                            draw_board(board, turn)
                            pygame.time.wait(1000)

                elif game_mode == 'player_vs_ai' and turn == 2:
                    col = player2_agent(board, 2)
                    row = drop_piece(board, col, turn)
                    if row != -1 and check_win(board, turn):  # Ensure valid drop
                        draw_board(board, turn)
                        display_message(f"Player {turn} wins!")
                        running = False
                    turn = 1
                    draw_board(board, turn)
                    pygame.time.wait(1000)

            if not running:  # If game ends, ask for replay
                if ask_play_again():
                    break  # Continue playing
                else:
                    # Go back to main menu
                    game_mode = main_menu()  # This will reset game mode
                    # You may need to reinitialize agents here if necessary
                    player1_agent = difficulty_menu()  # Choose agent for player 1
                    player2_agent = random_agent if game_mode == 'ai_vs_ai' else minimax_agent  # Choose agent for player 2
                    break  # Break the game loop to return to main menu



if __name__ == "__main__":
    game_mode = main_menu()
    player1_agent = difficulty_menu()

    # Default to AI agent for second player (AI vs AI)
    player2_agent = random_agent if game_mode == 'ai_vs_ai' else minimax_agent

    game_loop(game_mode, player1_agent, player2_agent)
