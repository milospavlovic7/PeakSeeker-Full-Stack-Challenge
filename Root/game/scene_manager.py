import pygame
import config
from ui.menu import display_menu, handle_menu_events
from ui.map_selection import display_map_selection, handle_map_selection_event
from ui.help import display_help, handle_help_event
from ui.settings import display_settings, handle_settings_event
from ui.game_over import display_game_over, handle_game_over_event
from ui.display import draw_grid, draw_score_and_lives
from ui.events import handle_click
from ui.music import MusicManager
from game.scoring import ScoringSystem
from game.procedural_map import generate_map
from game.island_detection import detect_islands_and_average_heights
from backend.fetch_map import fetch_map


class SceneManager:
    def __init__(self, screen):
        """Initializes the SceneManager with the game screen, and default settings."""
        self.screen = screen
        self.running = True  # Game is running by default
        self.current_scene = "menu"  # Default scene is the menu
        self.scoring_system = ScoringSystem()  # Initialize scoring system
        self.map_matrix = None  # Placeholder for the game map
        self.islands = None  # Placeholder for the detected islands
        self.max_island = None  # Placeholder for the island with the highest average height
        self.mouse_pos = (0, 0)  # Track mouse position for hovering
        self.music_manager = MusicManager()  # Music manager to handle game music
        self.music_on = True  # Default music state is 'on'
        self.is_nordeus = True  # Flag to indicate if the map is from Nordeus or procedural

    def start_new_level(self):
        """Starts a new level by fetching or generating a map and detecting islands."""
        if self.is_nordeus:
            # Fetch the map from the backend if Nordeus is selected
            self.map_matrix = fetch_map(config.MAP_URL)
            if self.map_matrix is None:
                print("Map could not be loaded.")
                return False
        else:
            # Generate a procedural map if the procedural option is selected
            self.map_matrix = generate_map()  # Generate blank map
            if self.map_matrix is None:
                print("Map could not be generated.")
                return False

        # Detect islands and calculate average heights
        self.islands, island_heights = detect_islands_and_average_heights(self.map_matrix, config.GRID_SIZE)
        self.max_island = self.islands[island_heights.index(max(island_heights))] if self.islands else None
        return True

    def handle_menu(self):
        """Handles user interaction in the menu scene."""
        # Play menu music if enabled
        self.music_manager.play_menu_music() if self.music_on else self.music_manager.stop_music()
        actions = display_menu(self.screen)  # Display the menu
        if handle_menu_events():
            if actions["play"]:
                self.current_scene = "map_selection"  # Go to map selection scene
            elif actions["quit"]:
                self.running = False  # Exit the game
            elif actions["help"]:
                self.current_scene = "help"  # Go to help scene
            elif actions["settings"]:
                self.current_scene = "settings"  # Go to settings scene

    def handle_map_selection(self):
        """Handles user interaction in the map selection scene."""
        # Display map selection options
        nordeus_pos, random_pos, back_pos = display_map_selection(self.screen)
        
        for event in pygame.event.get():
            selection = handle_map_selection_event(event, nordeus_pos, random_pos, back_pos)
            if selection == "nordeus":
                self.is_nordeus = True  # Select Nordeus map
                self.current_scene = "game"
                self.start_new_level()  # Start a new level
            elif selection == "procedural":
                self.is_nordeus = False  # Select procedural map
                self.current_scene = "game"
                self.start_new_level()  # Start a new level
            elif selection == "back":
                self.current_scene = "menu"  # Navigate back to the main menu

    def handle_help(self):
        """Handles user interaction in the help scene."""
        self.music_manager.play_menu_music() if self.music_on else self.music_manager.stop_music()
        back_rect = display_help(self.screen, self.screen.get_width(), self.screen.get_height())
        for event in pygame.event.get():
            action = handle_help_event(event, back_rect)
            if action == "back":
                self.current_scene = "menu"  # Go back to the menu

    def handle_game(self):
        """Handles the gameplay scene."""
        self.music_manager.play_game_music() if self.music_on else self.music_manager.stop_music()
        self.scoring_system.reset_score()  # Reset the score at the start of a new game
        if not self.start_new_level():  # Initialize the map and islands
            self.running = False
            return

        running_game = True  # Variable to keep the game loop running
        is_game_over = False  # Flag to check if the game is over

        while running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_game = False
                    self.running = False  # Stop the game loop when quitting
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # If the Escape key is pressed, return to menu
                        self.current_scene = "menu"
                        running_game = False
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = pygame.mouse.get_pos()  # Update mouse position for hovering
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle mouse click for selecting islands
                    click_pos = (event.pos[0] // config.CELL_SIZE, event.pos[1] // config.CELL_SIZE)
                    is_win = handle_click(self.map_matrix, self.islands, click_pos, self.max_island)
                    self.scoring_system.increment_attempts(is_win)

                    if is_win:
                        print("You guessed the island with the highest average height!")
                        if not self.start_new_level():  # Start a new level if the guess is correct
                            is_game_over = True

                    if self.scoring_system.lives <= 0:  # If no lives are left, game is over
                        is_game_over = True

            if is_game_over:
                # Show the game over screen
                retry_rect, menu_rect = display_game_over(self.screen, self.screen.get_width(), self.screen.get_height())
                for event in pygame.event.get():
                    action = handle_game_over_event(event, retry_rect, menu_rect)
                    if action == "retry":
                        self.scoring_system.reset_score()
                        if not self.start_new_level():
                            self.running = False
                            break
                        is_game_over = False
                    elif action == "menu":
                        self.music_manager.stop_music()  # Stop game music when game is over
                        self.current_scene = "menu"
                        running_game = False
                        
            else:
                # Drawing the game grid and score during the game loop
                self.screen.fill((0, 0, 0))  # Clear screen
                draw_grid(self.screen, self.map_matrix, self.islands, self.mouse_pos)  # Draw grid
                draw_score_and_lives(self.screen, self.scoring_system)  # Display score and lives
                pygame.display.flip()  # Update the screen display

    def handle_settings(self):
        """Handles user interaction in the settings scene."""
        back_rect, checkbox_rect, self.music_on = display_settings(self.screen, self.music_on)
        for event in pygame.event.get():
            action, self.music_on = handle_settings_event(event, back_rect, checkbox_rect, self.music_on)
            if action == "back":
                self.current_scene = "menu"  # Go back to the menu
            elif action == "toggle_music":
                # Toggle music state
                if self.music_on:
                    self.music_manager.play_menu_music()
                else:
                    self.music_manager.stop_music()

    def run(self):
        """Main game loop that runs the current scene and handles transitions."""
        while self.running:
            if self.current_scene == "menu":
                self.handle_menu()
            elif self.current_scene == "help":
                self.handle_help()
            elif self.current_scene == "map_selection":
                self.handle_map_selection()
            elif self.current_scene == "game":
                self.handle_game()
            elif self.current_scene == "settings":
                self.handle_settings()

        pygame.quit()  # Quit pygame when the game ends
