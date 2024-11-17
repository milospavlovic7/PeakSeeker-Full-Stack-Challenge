import pygame
import config
from ui.menu import draw_button  # Import the draw_button function from menu.py

def display_map_selection(screen):
    # Load and display the background image
    background_image = pygame.image.load(config.BACKGROUND_IMAGE_DARK_PATH)
    screen.blit(background_image, (0, 0))  # Stretch the image to fit the screen

    # Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Title text
    font = pygame.font.Font(None, 48)  # Set the font size for the title
    title_text = font.render("Choose Map Generation", True, (255, 255, 255))  # White text color
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4 - 50))  # Center the title near the top
    screen.blit(title_text, title_rect)  # Render the title to the screen

    # Button dimensions
    button_width, button_height = 200, 50  # Width and height for buttons
    button_spacing = 20  # Spacing between buttons

    # Center positions for each button
    nordeus_pos = (screen.get_width() // 2 - button_width // 2, screen.get_height() // 2 - button_height - button_spacing)
    procedural_pos = (screen.get_width() // 2 - button_width // 2, screen.get_height() // 2)
    back_pos = (screen.get_width() // 2 - button_width // 2, screen.get_height() // 2 + button_height + button_spacing)

    # Draw the "Nordeus" button with hover effect
    is_hovered_nordeus = nordeus_pos[0] < mouse_pos[0] < nordeus_pos[0] + button_width and nordeus_pos[1] < mouse_pos[1] < nordeus_pos[1] + button_height
    draw_button(screen, "Nordeus", nordeus_pos[0], nordeus_pos[1], button_width, button_height, is_hovered_nordeus)

    # Draw the "Procedural" button with hover effect
    is_hovered_procedural = procedural_pos[0] < mouse_pos[0] < procedural_pos[0] + button_width and procedural_pos[1] < mouse_pos[1] < procedural_pos[1] + button_height
    draw_button(screen, "Procedural", procedural_pos[0], procedural_pos[1], button_width, button_height, is_hovered_procedural)

    # Draw the "Back" button with hover effect
    is_hovered_back = back_pos[0] < mouse_pos[0] < back_pos[0] + button_width and back_pos[1] < mouse_pos[1] < back_pos[1] + button_height
    draw_button(screen, "Back", back_pos[0], back_pos[1], button_width, button_height, is_hovered_back)

    pygame.display.flip()  # Update the display to show the buttons and background

    # Return the positions of the buttons for click detection in the event handler
    return nordeus_pos, procedural_pos, back_pos

def handle_map_selection_event(event, nordeus_pos, procedural_pos, back_pos):
    # Handle mouse click events to check if any button was clicked
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos  # Get the coordinates of the mouse click

        # Check if the Nordeus button was clicked
        if nordeus_pos[0] < x < nordeus_pos[0] + 200 and nordeus_pos[1] < y < nordeus_pos[1] + 50:
            return "nordeus"  # Return the action for "Nordeus"

        # Check if the Procedural button was clicked
        elif procedural_pos[0] < x < procedural_pos[0] + 200 and procedural_pos[1] < y < procedural_pos[1] + 50:
            return "procedural"  # Return the action for "Procedural"

        # Check if the Back button was clicked
        elif back_pos[0] < x < back_pos[0] + 200 and back_pos[1] < y < back_pos[1] + 50:
            return "back"  # Return the action for "Back"

    return None  # Return None if no button was clicked
