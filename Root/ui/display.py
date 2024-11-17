import pygame
import config

CELL_SIZE = config.CELL_SIZE  # Dimension of each cell
GRID_SIZE = config.GRID_SIZE  # Number of cells in the grid (30x30)

# Function for interpolating between two colors with clamping values
def lerp_color(color1, color2, t):
    r = int(color1[0] + (color2[0] - color1[0]) * t)  # Interpolate red component
    g = int(color1[1] + (color2[1] - color1[1]) * t)  # Interpolate green component
    b = int(color1[2] + (color2[2] - color1[2]) * t)  # Interpolate blue component
    # Ensure the color values stay between 0 and 255
    return (max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255)))

# Function that returns a color based on the height of a cell
def get_color_for_height(height):
    if height <= 0:
        return (0, 0, 255)  # Blue (water)
    
    color_low = (0, 255, 0)     # Green
    color_mid = (255, 255, 0)    # Yellow
    color_high = (139, 69, 19)   # Brown
    color_peak = (255, 255, 255) # White

    max_height = 1000  # Maximum height value
    t = min(max(height / max_height, 0), 1)  # Normalize height value to a range [0, 1]

    # Interpolate between colors based on the height
    if t <= 0.2:
        return lerp_color(color_low, color_mid, t / 0.2)
    elif t <= 0.5:
        return lerp_color(color_mid, color_high, (t - 0.2) / 0.3)
    else:
        return lerp_color(color_high, color_peak, (t - 0.5) / 0.5)

# Function for drawing the grid with hover effect and island borders
def draw_grid(screen, map_matrix, islands, mouse_pos):
    font = pygame.font.SysFont(None, 16)  # Font for displaying text
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            height = map_matrix[x][y]  # Get the height of the current cell
            color = get_color_for_height(height)  # Get color for the cell based on its height
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Draw the cell

    # Determine hover cell coordinates based on mouse position
    hover_x, hover_y = mouse_pos[0] // CELL_SIZE, mouse_pos[1] // CELL_SIZE

    # Display borders around each cell in the island where it’s adjacent to water
    island_under_cursor = get_island_under_cursor(hover_x, hover_y, islands)
    if island_under_cursor:
        for x, y in island_under_cursor:
            # Check neighboring cells to draw borders only where adjacent to water
            if y > 0 and map_matrix[x][y - 1] == 0:  # Top neighbor
                pygame.draw.line(screen, (255, 255, 255), 
                                 (x * CELL_SIZE, y * CELL_SIZE), 
                                 ((x + 1) * CELL_SIZE, y * CELL_SIZE), 3)
            if y < GRID_SIZE - 1 and map_matrix[x][y + 1] == 0:  # Bottom neighbor
                pygame.draw.line(screen, (255, 255, 255), 
                                 (x * CELL_SIZE, (y + 1) * CELL_SIZE), 
                                 ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), 3)
            if x > 0 and map_matrix[x - 1][y] == 0:  # Left neighbor
                pygame.draw.line(screen, (255, 255, 255), 
                                 (x * CELL_SIZE, y * CELL_SIZE), 
                                 (x * CELL_SIZE, (y + 1) * CELL_SIZE), 3)
            if x < GRID_SIZE - 1 and map_matrix[x + 1][y] == 0:  # Right neighbor
                pygame.draw.line(screen, (255, 255, 255), 
                                 ((x + 1) * CELL_SIZE, y * CELL_SIZE), 
                                 ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), 3)

# Function that detects which island is under the cursor (if any)
def get_island_under_cursor(x, y, islands):
    for island in islands:
        if (x, y) in island:  # Check if the cursor is on the island
            return island  # Return the island if the cell is part of it
    return None  # Return None if no island is under the cursor

# Function to draw the score and lives on the screen
def draw_score_and_lives(screen, scoring_system):
    font = pygame.font.Font(None, 36)  # Font for displaying score and lives

    # Render score text and position it on the top right of the screen
    score_text = font.render(f"Score: {scoring_system.correct_attempts}", True, (255, 255, 255))
    score_rect = score_text.get_rect(topright=(screen.get_width() - 20, 20))
    screen.blit(score_text, score_rect)  # Draw the score on the screen

    # Render lives text and position it just below the score
    lives_text = font.render(f"Lives: {scoring_system.lives}", True, (255, 0, 0))
    lives_rect = lives_text.get_rect(topright=(screen.get_width() - 20, 60))
    screen.blit(lives_text, lives_rect)  # Draw the lives on the screen
