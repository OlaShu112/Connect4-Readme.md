import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize Pygame mixer for music

if not pygame.mixer.get_init():
    print("Error: Pygame mixer failed to initialise")
else:
    print("Pygame mixer initialised successfully")

# Constants
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

# List of music files with absolute paths
music_files = [
    "C:/xampp/htdocs/Connect4AIProject/assets/AyraStar_Music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/Cr&AS_Ngozi_Music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/DarkooFtRema_Music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/MohBad_Music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/Teni_Malaika_Music.wav"
]


music_index = 0  # Start with the first track
playing = False  # Music is off initially

# Font
font = pygame.font.SysFont("Arial", 40)

# Create game board
def create_board():
    return [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

# Draw board
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

# Play/Pause music function
def play_music():
    global playing
    track = music_files[music_index]
    
    if not playing:
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)  # Play on loop
        playing = True
    else:
        pygame.mixer.music.pause()
        playing = False

# Stop music function
def stop_music():
    pygame.mixer.music.stop()
    global playing
    playing = False

# Next track
def next_track():
    global music_index
    music_index = (music_index + 1) % len(music_files)
    pygame.mixer.music.load(music_files[music_index])
    pygame.mixer.music.play(-1)

# Previous track
def previous_track():
    global music_index
    music_index = (music_index - 1) % len(music_files)
    pygame.mixer.music.load(music_files[music_index])
    pygame.mixer.music.play(-1)

# Check valid move
def valid_move(board, col):
    return board[0][col] == 0

# Place piece
def make_move(board, col, player):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return row
    return None

# Check for win
def check_win(board, player):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    for row in range(3, ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Display message
def display_message(message):
    text = font.render(message, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Ask to play again
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

# AI move (random)
def ai_move(board):
    while True:
        col = random.randint(0, COLUMN_COUNT - 1)
        if valid_move(board, col):
            return col

# Main Menu
def main_menu():
    while True:
        screen.fill(BLACK)
        text = font.render("Press 1 for 2-Player Game", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

        text = font.render("Press 2 for Player vs AI", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'human'
                elif event.key == pygame.K_2:
                    return 'ai'

# Game loop
def game_loop(game_mode):
    while True:
        board = create_board()
        running = True
        turn = 1  # Player 1 starts
        while running:
            draw_board(board)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        play_music()
                    if event.key == pygame.K_s:
                        stop_music()
                    if event.key == pygame.K_RIGHT:
                        next_track()
                    if event.key == pygame.K_LEFT:
                        previous_track()

                # Mouse click for player's move
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_x, mouse_y = event.pos
                        col = mouse_x // SQUARE_SIZE

                        if valid_move(board, col):
                            row = make_move(board, col, turn)
                            if check_win(board, turn):
                                display_message("Player {} wins!".format(turn))
                                running = False
                            turn = 3 - turn  # Switch player

            # AI move if playing against AI
            if game_mode == 'ai' and turn == 2:
                col = ai_move(board)
                make_move(board, col, 2)
                if check_win(board, 2):
                    display_message("AI wins!")
                    running = False
                turn = 1  # Switch to player 1

        if not ask_play_again():
            break

# Run main menu and start game
def run_game():
    game_mode = main_menu()  
    game_loop(game_mode)

if __name__ == "__main__":
    run_game()
