import pygame  # Import the pygame library for game development
import config  # Import the config module for configuration values, like background image path

# Define color constants (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER_COLOR = (200, 200, 200)  # Color when the button is hovered over

# Define button dimensions and spacing
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

def draw_button(screen, text, x, y, width, height, is_hovered):
    """Draws a button on the screen with a hover effect."""
    font = pygame.font.Font(None, 36)  # Create a font object for the button text
    button_color = HOVER_COLOR if is_hovered else WHITE  # Change color if hovered
    pygame.draw.rect(screen, button_color, (x, y, width, height))  # Draw the button rectangle
    text_surface = font.render(text, True, BLACK)  # Render the text to be displayed on the button
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  # Position the text at the center
    screen.blit(text_surface, text_rect)  # Draw the text on the screen

def display_settings(screen, music_on):
    """Displays the settings screen with music toggle and a 'Back' button."""
    # Load and display the background image
    background_image = pygame.image.load(config.BACKGROUND_IMAGE_DARK_PATH)
    screen.blit(background_image, (0, 0))  # Stretch the image to fit the entire screen
    
    # Center the buttons on the screen
    screen_width, screen_height = screen.get_size()
    total_height = (2 * BUTTON_HEIGHT) + BUTTON_SPACING  # Total height for buttons and spacing
    start_y = (screen_height - total_height) // 2  # Vertical start position to center the buttons
    start_x = (screen_width - BUTTON_WIDTH) // 2  # Horizontal center position for the button
    
    # Display the music toggle text ("Music: On" or "Music: Off")
    music_text = "Music: On" if music_on else "Music: Off"
    font = pygame.font.Font(None, 36)
    text_surface = font.render(music_text, True, WHITE)  # Render the music state text
    text_rect = text_surface.get_rect(center=(start_x + BUTTON_WIDTH // 2, start_y + BUTTON_HEIGHT // 2))
    screen.blit(text_surface, text_rect)  # Display the text
    
    # Detect mouse hover for the "Back" button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    is_hovered_back = start_x < mouse_x < start_x + BUTTON_WIDTH and start_y + BUTTON_HEIGHT + BUTTON_SPACING < mouse_y < start_y + BUTTON_HEIGHT + BUTTON_SPACING + BUTTON_HEIGHT
    
    # Draw the "Back" button with hover effect
    draw_button(screen, "Back", start_x, start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, is_hovered_back)
    
    pygame.display.flip()  # Update the screen with the changes

    # Define the clickable areas (rectangles) for the buttons
    back_rect = pygame.Rect(start_x, start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT)
    music_text_rect = pygame.Rect(start_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT)  # Area for the music toggle

    return back_rect, music_text_rect, music_on

def handle_settings_event(event, back_rect, music_text_rect, music_on):
    """Handles events in the settings screen, including button clicks and music toggling."""
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if event.type == pygame.QUIT:  # Quit event
        pygame.quit()

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
        # If the "Back" button is clicked, return the "back" action
        if back_rect.collidepoint(mouse_x, mouse_y):
            return "back", music_on  
        # If the music toggle area is clicked, change the music state and return the toggle action
        elif music_text_rect.collidepoint(mouse_x, mouse_y):
            music_on = not music_on  # Toggle the music state (on/off)
            return "toggle", music_on  # Return the updated music state

    return None, music_on  # Return None if no action is triggered
