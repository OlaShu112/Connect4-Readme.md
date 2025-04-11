import pygame
import random
from Connect4Console.music import MusicPlayer

# ================================
# Game Board Class
# ================================

class GameBoard:
    """Represents the Connect Four game board."""
    
    def __init__(self):
        """Initializes an empty 6x7 game board."""
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.music_player = MusicPlayer()  # Create music player instance

    def start_music(self):
        """Starts playing music after the game is ready."""
        self.music_player.play_music()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event for music ending

    def print_board(self):
        """Prints the game board with each entry inside a box."""
        print("\n  0   1   2   3   4   5   6  ")
        print("+" + "---+" * 7) 

        for row in self.board:
            print("| " + " | ".join(row) + " |")
            print("+" + "---+" * 7)

    def is_full(self):
        """Checks if the board is completely filled."""
        return all(' ' not in row for row in self.board)

    def is_winning(self, player):
        """Determines if the given player has won the game."""
        for row in range(6):
            for col in range(7):
                if self.check_win(player, row, col):
                    return True
        return False

    def check_win(self, player, row, col):
        """Checks if a player has four connected pieces in any direction."""
        if col + 3 < 7 and all(self.board[row][col + i] == player for i in range(4)):
            return True
        if row + 3 < 6 and all(self.board[row + i][col] == player for i in range(4)):
            return True
        if row + 3 < 6 and col + 3 < 7 and all(self.board[row + i][col + i] == player for i in range(4)):
            return True
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
# Game Loop (Main)
# ================================

def main():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Connect 4 Game with Music")

    # Initialize the game board
    game_board = GameBoard()

    # ===== TRAINING LOGIC GOES HERE BEFORE MUSIC STARTS =====
    print("Training AI model... (Simulated delay removed)")  
    # If there's AI training, place it here

    # Start music AFTER training is done
    game_board.start_music()

    current_player = 'X'
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle music controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Increase volume
                    game_board.music_player.set_volume(min(1.0, pygame.mixer.music.get_volume() + 0.1))
                elif event.key == pygame.K_DOWN:  # Decrease volume
                    game_board.music_player.set_volume(max(0.0, pygame.mixer.music.get_volume() - 0.1))
                elif event.key == pygame.K_LEFT:  # Change track backward
                    game_board.music_player.change_music_backward()
                elif event.key == pygame.K_RIGHT:  # Change track forward
                    game_board.music_player.change_music_forward()
                elif event.key == pygame.K_p:  # Pause music
                    game_board.music_player.pause_music()
                elif event.key == pygame.K_r:  # Resume music
                    game_board.music_player.resume_music()

            # Detect track end event and play the next song
            if event.type == pygame.USEREVENT:
                game_board.music_player.handle_music_end()

            # Handle game actions
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[0]
                column = mouse_x // (800 // 7)
                if column in game_board.available_moves():
                    game_board.drop_disc(column, current_player)
                    game_board.print_board()

                    # Check for a winner after the move
                    if game_board.is_winning(current_player):
                        print(f"Player {current_player} wins!")
                        running = False  

                    # Switch to the other player
                    current_player = 'O' if current_player == 'X' else 'X'

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
