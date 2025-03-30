import pygame
import random

class MusicPlayer:
    def __init__(self):
        """Initializes the music player with a list of music files."""
        self.music_files = [
            "C:/Users/Admin/OneDrive/Desktop/Connect4AIProject/assets/music.wav",
            "C:/Users/Admin/OneDrive/Desktop/Connect4AIProject/assets/AyraStar_Music.wav",
            "C:/Users/Admin/OneDrive/Desktop/Connect4AIProject/assets/Cr&AS_Ngozi_Music.wav",
            "C:/Users/Admin/OneDrive/Desktop/Connect4AIProject/assets/DarkooFtRema_Music.wav",
            "C:/Users/Admin/OneDrive/Desktop/Connect4AIProject/assets/MohBad_Music.wav",
            "C:/Users/Admin/OneDrive/Desktop/Connect4AIProject/assets/Teni_Malaika_Music.wav"
        ]
        self.current_music_index = random.randint(0, len(self.music_files) - 1)  # Start with a random track
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Event triggered when a song ends
        self.play_music()  # Play the first song

    def play_music(self):
        """Play the selected track."""
        music_file = self.music_files[self.current_music_index]
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        print(f"Now playing: {music_file}")

    def stop_music(self):
        """Stop the current track."""
        pygame.mixer.music.stop()
        print("Music stopped.")

    def pause_music(self):
        """Pause the current track."""
        pygame.mixer.music.pause()
        print("Music paused.")

    def resume_music(self):
        """Resume the current track."""
        pygame.mixer.music.unpause()
        print("Music resumed.")

    def change_music_forward(self):
        """Change to the next track in the playlist."""
        self.current_music_index = (self.current_music_index + 1) % len(self.music_files)
        self.play_music()

    def change_music_backward(self):
        """Change to the previous track in the playlist."""
        self.current_music_index = (self.current_music_index - 1) % len(self.music_files)
        self.play_music()

    def handle_music_end(self):
        """Automatically play the next track when the current one ends."""
        self.change_music_forward()

    def set_volume(self, volume):
        """Sets the music volume (range from 0.0 to 1.0)."""
        pygame.mixer.music.set_volume(volume)
        print(f"Volume set to: {volume}")

    def shuffle_playlist(self):
        """Shuffles the playlist for random order on each game start."""
        random.shuffle(self.music_files)
        self.current_music_index = 0  # Reset to the first track after shuffling
        self.play_music()
