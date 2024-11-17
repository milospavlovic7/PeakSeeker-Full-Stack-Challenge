import pygame  # Import the pygame library for game development
import config  # Import the config module for configuration values, like music file paths

class MusicManager:
    """Class to manage background music for the game."""

    def __init__(self):
        """Initialize the MusicManager with no music playing initially."""
        self.music_playing = None  # Keeps track of which music is currently playing (menu or game)

    def play_menu_music(self):
        """Play the menu music if it's not already playing."""
        if self.music_playing != 'menu':  # Check if the menu music is not already playing
            pygame.mixer.music.load(config.MENU_MUSIC_PATH)  # Load the menu music file
            pygame.mixer.music.play(-1)  # Play music indefinitely (-1 means loop forever)
            self.music_playing = 'menu'  # Update the music state to 'menu'

    def play_game_music(self):
        """Play the game music if it's not already playing."""
        if self.music_playing != 'game':  # Check if the game music is not already playing
            pygame.mixer.music.load(config.GAME_MUSIC_PATH)  # Load the game music file
            pygame.mixer.music.play(-1)  # Play music indefinitely (-1 means loop forever)
            self.music_playing = 'game'  # Update the music state to 'game'

    def stop_music(self):
        """Stop the currently playing music."""
        pygame.mixer.music.stop()  # Stop any currently playing music
        self.music_playing = None  # Reset the music state to None (no music playing)
