import numpy as np
from collections import deque

# Function to check if coordinates are within the map boundaries
def is_valid(x, y, grid_size):
    return 0 <= x < grid_size and 0 <= y < grid_size

# BFS function for identifying connected islands
def bfs(grid, start_x, start_y, visited, grid_size):
    # List to store island cells
    island_cells = []
    
    # Movement directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Use deque as a queue for BFS
    queue = deque([(start_x, start_y)])
    visited[start_x][start_y] = True
    
    while queue:
        x, y = queue.popleft()  # Get the next cell to process
        island_cells.append((x, y))  # Add the current cell to the island
        
        # Check neighboring cells
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, grid_size) and not visited[nx][ny] and grid[nx][ny] > 0:
                visited[nx][ny] = True
                queue.append((nx, ny))
    
    return island_cells

# Function to detect all islands on the grid
def detect_islands(grid, grid_size):
    visited = np.zeros((grid_size, grid_size), dtype=bool)  # Matrix to track visited cells
    islands = []  # List to store islands
    
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x][y] > 0 and not visited[x][y]:  # If the cell is part of an island and not visited
                # Detect the island using BFS
                island_cells = bfs(grid, x, y, visited, grid_size)
                islands.append(island_cells)
    
    return islands

# Function to calculate the average height of an island
def average_height_of_island(island_cells, grid):
    total_height = 0
    for x, y in island_cells:
        total_height += grid[x][y]
    return total_height / len(island_cells) if island_cells else 0

# Function that detects islands and calculates their average height
def detect_islands_and_average_heights(grid, grid_size):
    islands = detect_islands(grid, grid_size)
    island_heights = []
    
    for island in islands:
        avg_height = average_height_of_island(island, grid)
        island_heights.append(avg_height)
    
    return islands, island_heights

# Function to handle clicks on the map and output information about the clicked area
def handle_click_on_map(screen_x, screen_y, grid_size, grid, islands, island_heights, cell_size=30, grid_offset_x=0, grid_offset_y=0):
    # Convert screen coordinates to grid coordinates
    grid_x = screen_x // cell_size  # Calculate the x-coordinate on the grid
    grid_y = screen_y // cell_size  # Calculate the y-coordinate on the grid
    
    print(f"Clicked at screen coordinates: ({screen_x}, {screen_y}), corresponding grid coordinates: ({grid_x}, {grid_y})")
    
    # Check if the coordinates are within the grid
    if not is_valid(grid_x, grid_y, grid_size):
        print("You clicked outside the map.")
        return
    
    # Output the height of the clicked cell
    height = grid[grid_x][grid_y]
    print(f"Height of clicked cell ({grid_x}, {grid_y}): {height}")
    
    # Check if the clicked area is part of an island
    island_found = False
    for idx, island in enumerate(islands):
        if (grid_x, grid_y) in island:
            print(f"You clicked on island {idx} with an average height of {island_heights[idx]}")
            print(f"Island {idx} consists of the following coordinates:")
            for island_x, island_y in island:
                island_height = grid[island_x][island_y]
                print(f"Coordinates: ({island_x}, {island_y}), Height: {island_height}")
            island_found = True
            break
    
    if not island_found:
        print("You clicked outside any island.")
