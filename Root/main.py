import pygame  # Import the pygame library for game development
import config  # Import the config module for configuration values (e.g., grid size, cell size)
from game.scene_manager import SceneManager  # Import the SceneManager class to manage game scenes

pygame.init()  # Initialize the pygame library

# Set the window size based on grid size and cell size
WINDOW_SIZE = config.GRID_SIZE * config.CELL_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # Create the game window
pygame.display.set_caption("PeakSeeker")  # Set the window title

def main():
    scene_manager = SceneManager(screen)  # Create a SceneManager instance to manage game scenes
    scene_manager.run()  # Start running the game loop using the SceneManager

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
