import pygame
import sys

# Colors
WHITE = (255, 255, 255)
HOVER_COLOR = (200, 200, 200)

# Function to draw a button with hover effect
def draw_button(screen, text, x, y, width, height, is_hovered):
    font = pygame.font.Font(None, 36)  # Font for button text
    button_color = HOVER_COLOR if is_hovered else WHITE  # Change color if hovered
    pygame.draw.rect(screen, button_color, (x, y, width, height))  # Draw button background
    text_surface = font.render(text, True, (0, 0, 0))  # Render the text on the button
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  # Center text on the button
    screen.blit(text_surface, text_rect)  # Display the text on the button

# Function to display the game over screen
def display_game_over(screen, width, height):
    screen.fill((0, 0, 0))  # Set the background to black

    # Display the "Game Over" title
    font = pygame.font.Font(None, 74)  # Large font for "Game Over"
    text = font.render("Game Over", True, (255, 0, 0))  # Red color for the text
    text_rect = text.get_rect(center=(width // 2, height // 3))  # Center the title
    screen.blit(text, text_rect)

    # Button positions
    button_width, button_height = 200, 50
    retry_pos = (width // 2 - button_width // 2, height // 2)  # Center the Retry button
    menu_pos = (width // 2 - button_width // 2, height // 2 + 80)  # Center the Menu button below Retry

    # Detect if the mouse is hovering over the buttons
    mouse_x, mouse_y = pygame.mouse.get_pos()
    is_hovered_retry = retry_pos[0] < mouse_x < retry_pos[0] + button_width and retry_pos[1] < mouse_y < retry_pos[1] + button_height
    is_hovered_menu = menu_pos[0] < mouse_x < menu_pos[0] + button_width and menu_pos[1] < mouse_y < menu_pos[1] + button_height

    # Draw the "Retry" and "Menu" buttons with hover effect
    draw_button(screen, "Retry", retry_pos[0], retry_pos[1], button_width, button_height, is_hovered_retry)
    draw_button(screen, "Menu", menu_pos[0], menu_pos[1], button_width, button_height, is_hovered_menu)

    pygame.display.flip()  # Update the display to show the buttons

    # Return the clickable areas for the buttons (as pygame.Rect objects)
    return pygame.Rect(retry_pos[0], retry_pos[1], button_width, button_height), pygame.Rect(menu_pos[0], menu_pos[1], button_width, button_height)

# Function to handle events on the game over screen
def handle_game_over_event(event, retry_rect, menu_rect):
    # Handle quit event
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    # Handle mouse click events on the "Retry" or "Menu" buttons
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if retry_rect.collidepoint(event.pos):  # Check if the click is inside the Retry button area
            return "retry"  # Return "retry" action if clicked
        elif menu_rect.collidepoint(event.pos):  # Check if the click is inside the Menu button area
            return "menu"  # Return "menu" action if clicked

    return None  # Return None if no button was clicked
