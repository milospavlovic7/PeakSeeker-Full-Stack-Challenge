import pygame  # Import the pygame library for game development
import config  # Import the config module for configuration values like background image paths
import sys  # Import the sys module to handle system-level functions (e.g., exit the game)

# Colors for UI elements (buttons, text, etc.)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER_COLOR = (200, 200, 200)  # Color when hovering over a button

# Button dimensions
BUTTON_WIDTH = 200  # Button width
BUTTON_HEIGHT = 50  # Button height
BUTTON_SPACING = 20  # Space between buttons

def draw_button(screen, text, x, y, width, height, is_hovered):
    """Draw a button with specified dimensions, text, and hover effect."""
    font = pygame.font.Font(None, 36)  # Create a font for the button text
    button_color = HOVER_COLOR if is_hovered else WHITE  # Change color when hovered
    pygame.draw.rect(screen, button_color, (x, y, width, height))  # Draw the button rectangle
    text_surface = font.render(text, True, BLACK)  # Render the text on the button
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  # Center the text
    screen.blit(text_surface, text_rect)  # Draw the text on the button

def display_menu(screen):
    """Display the menu screen with background, title, and buttons."""
    # Load and display the background image
    background_image = pygame.image.load(config.BACKGROUND_IMAGE_PATH)
    screen.blit(background_image, (0, 0))  # Stretch the image to fit the screen
    
    # Center the buttons on the screen
    screen_width, screen_height = screen.get_size()
    total_height = (4 * BUTTON_HEIGHT) + (3 * BUTTON_SPACING)  # Calculate total height for buttons
    start_y = (screen_height - total_height) // 2  # Center the buttons vertically
    start_x = (screen_width - BUTTON_WIDTH) // 2  # Center the buttons horizontally

    # Title settings (display the game title)
    title_font = pygame.font.Font(None, 48)  # Font for the title
    title_text = "PeakSeeker"  # Title text
    title_surface = title_font.render(title_text, True, WHITE)  # Render title text
    title_rect = title_surface.get_rect(center=(screen_width // 2, screen.get_height() // 4 - 50))  # Center the title
    screen.blit(title_surface, title_rect)  # Draw the title on the screen
    
    # Define the buttons and their actions
    buttons = [
        {"text": "Play", "action": "play"},
        {"text": "Help", "action": "help"},
        {"text": "Settings", "action": "settings"},
        {"text": "Quit", "action": "quit"}
    ]
    
    # Draw each button and check for hover and click events
    mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
    actions = {}  # Dictionary to store actions for buttons
    for i, button in enumerate(buttons):
        x, y = start_x, start_y + i * (BUTTON_HEIGHT + BUTTON_SPACING)  # Button position
        is_hovered = x < mouse_pos[0] < x + BUTTON_WIDTH and y < mouse_pos[1] < y + BUTTON_HEIGHT  # Check if button is hovered
        draw_button(screen, button["text"], x, y, BUTTON_WIDTH, BUTTON_HEIGHT, is_hovered)  # Draw the button
        
        # Store if the button is hovered, to use in event handling
        actions[button["action"]] = is_hovered
    
    pygame.display.flip()  # Update the screen with the drawn elements
    return actions  # Return the actions dictionary to handle button clicks later

def handle_menu_events():
    """Handle events in the menu, like quitting or clicking buttons."""
    for event in pygame.event.get():  # Loop through all events in the event queue
        if event.type == pygame.QUIT:  # Check if the window is closed
            pygame.quit()  # Quit pygame
            sys.exit()  # Exit the program
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
            return True  # Return True to indicate that a click event occurred
    return False  # Return False if no relevant event occurred
