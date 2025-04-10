import pygame
import sys



from music_player import play_music, stop_music, next_track, previous_track # type: ignore
from agents import minimax_agent, random_agent, smart_agent, ml_agent, make_move, check_win, valid_move
from agents import block_player_move


# Initialize Pygame
pygame.init()

# Constants for game
SQUARE_SIZE = 70  
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

def draw_board(board):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    pygame.display.flip()

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
                    return True
                if event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()


def game_loop(game_mode):
    while True:
        board = create_board()
        running = True
        turn = 1
        draw_board(board)

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
                        row = make_move(board, col, turn)
                        if check_win(board, turn):
                            draw_board(board)
                            display_message(f"Player {turn} wins!")
                            running = False
                        turn = 2 if turn == 1 else 1
                        draw_board(board)

                # AI Logic for AI vs AI
                elif game_mode == 'ai_vs_ai' and turn == 1:
                    col = minimax_agent(board, 1)
                    row = make_move(board, col, turn)
                    if check_win(board, turn):
                        draw_board(board)
                        display_message(f"Player {turn} (Minimax Agent) wins!")
                        running = False
                    turn = 2
                    draw_board(board)
                    pygame.time.wait(1000)  # Delay between AI turns

                elif game_mode == 'ai_vs_ai' and turn == 2:
                    col = random_agent(board, 2)
                    row = make_move(board, col, turn)
                    if check_win(board, turn):
                        draw_board(board)
                        display_message(f"Player {turn} (Random Agent) wins!")
                        running = False
                    turn = 1
                    draw_board(board)
                    pygame.time.wait(1000)  # Delay between AI turns

                # Player vs AI Logic
                elif game_mode == 'player_vs_ai' and turn == 1:
                    # Human's turn
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = event.pos[0] // SQUARE_SIZE
                        if valid_move(board, col):
                            row = make_move(board, col, turn)
                            if check_win(board, turn):
                                draw_board(board)
                                display_message(f"Player {turn} wins!")
                                running = False
                            turn = 2  # Switch to AI
                            draw_board(board)

                elif game_mode == 'player_vs_ai' and turn == 2:
                    # AI's turn (AI will block player's winning move if possible)
                    block_col = block_player_move(board, 1)  # Check if the player has a winning move
                    if block_col is not None:
                        col = block_col  # Block the player's winning move
                    else:
                        col = minimax_agent(board, 2)  # Otherwise, AI plays using Minimax

                    row = make_move(board, col, turn)
                    if check_win(board, turn):
                        draw_board(board)
                        display_message(f"Player {turn} (AI) wins!")
                        running = False
                    turn = 1  # Switch to Player
                    draw_board(board)
                    pygame.time.wait(1000)  # Delay between AI turns

        if not ask_play_again():
            break

# Start the game
mode = main_menu()
game_loop(mode)
