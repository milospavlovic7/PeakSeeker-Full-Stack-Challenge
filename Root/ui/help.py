import pygame
import config
import sys

# Colors for buttons and text
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER_COLOR = (200, 200, 200)

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

# Function to draw a button with hover effect
def draw_button(screen, text, x, y, width, height, is_hovered):
    font = pygame.font.Font(None, 36)  # Font for button text
    button_color = HOVER_COLOR if is_hovered else WHITE  # Change color on hover
    pygame.draw.rect(screen, button_color, (x, y, width, height))  # Draw button rectangle
    text_surface = font.render(text, True, BLACK)  # Render text on the button
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  # Center text on button
    screen.blit(text_surface, text_rect)  # Blit the text onto the button

# Function to display the help screen
def display_help(screen, width, height):
    # Load and display the background image (fits the screen)
    background_image = pygame.image.load(config.BACKGROUND_IMAGE_DARK_PATH)
    screen.blit(background_image, (0, 0))

    # Set fonts for title and instructions
    title_font = pygame.font.Font(None, 60)  # Larger font for title
    text_font = pygame.font.Font(None, 24)  # Smaller font for instructions
    color_font = pygame.font.Font(None, 24)  # Font for color legend

    # Display title
    title_text = title_font.render("Help", True, WHITE)
    title_rect = title_text.get_rect(center=(width // 2, height // 8))  # Center the title
    screen.blit(title_text, title_rect)

    # List of instructions to display
    instructions = [
        "Instructions:",
        "- Click on islands to identify the one with the highest average height.",
        "- Correct selections award points, incorrect ones deduct lives.",
        "- The game ends when you run out of lives.",
        "",
        "",
        "Legend: Height and Color Representation:"
    ]
    # Render instructions and display them
    for i, line in enumerate(instructions):
        instruction_text = text_font.render(line, True, WHITE)
        screen.blit(instruction_text, (50, height // 8 + 60 + i * 30))  # Adjust position for each line

    # Display color legend with labels and colors
    color_legend = [
        ("Water", (0, 0, 255)),
        ("Low Land (Green)", (0, 255, 0)),
        ("Medium Land (Yellow)", (255, 255, 0)),
        ("High Land (Brown)", (139, 69, 19)),
        ("Mountain Peak (White)", (255, 255, 255))
    ]
    for i, (label, color) in enumerate(color_legend):
        color_box = pygame.Rect(50, height // 2 + i * 30, 20, 20)  # Create a colored square for each label
        pygame.draw.rect(screen, color, color_box)  # Draw the colored box
        color_text = color_font.render(label, True, WHITE)  # Render the label text
        screen.blit(color_text, (80, height // 2 + i * 30))  # Display the label next to the color box

    # Back button positioning
    back_x = (width - BUTTON_WIDTH) // 2  # Center the back button horizontally
    back_y = height - BUTTON_HEIGHT - 20  # Position it near the bottom

    # Detect mouse hover over the back button
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = back_x < mouse_pos[0] < back_x + BUTTON_WIDTH and back_y < mouse_pos[1] < back_y + BUTTON_HEIGHT

    # Draw the "Back" button with hover effect
    draw_button(screen, "Back", back_x, back_y, BUTTON_WIDTH, BUTTON_HEIGHT, is_hovered)

    pygame.display.flip()  # Update the display to show the content

    # Define the rectangle area for the "Back" button (for click detection)
    back_rect = pygame.Rect(back_x, back_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    return back_rect  # Return the button's clickable area for event handling

# Function to handle events on the help screen
def handle_help_event(event, back_rect):
    # Handle quit event (closing the window)
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    # Handle mouse button clicks (left click on the "Back" button)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
        if back_rect.collidepoint(event.pos):  # Check if click is inside the back button area
            return "back"  # Return the action to go back

    return None  # Return None if no action was triggered
