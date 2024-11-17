from game.island_detection import detect_islands, average_height_of_island

def get_clicked_island(click_pos, islands, grid):
    x, y = click_pos  # Directly use the clicked coordinates
    
    # First, print the height of the clicked grid cell
    height = grid[x][y]  # The height of the clicked grid cell
    print(f"Height of cell ({x}, {y}): {height}")
    
    # Loop through the islands and check if the clicked position belongs to any of them
    for index, island in enumerate(islands):
        if (x, y) in island:  # Check if the clicked position is within the island
            print(f"Found island with index {index} for grid coordinates: ({x}, {y})")
            return island  # Return the island if it contains the clicked position
    
    print("Clicked outside of any island")
    return None  # Return None if the click is not on any island


def handle_click(map_matrix, islands, click_pos, max_island):
    # Find the island that was clicked
    clicked_island = get_clicked_island(click_pos, islands, map_matrix)

    # If an island was clicked, check if it is the one with the highest average height
    if clicked_island:
        if clicked_island == max_island:
            print("You clicked the island with the highest average height!")
            return True  # Return True if the correct island is clicked
        else:
            print(f"The island you clicked on is not the highest island.")
    else:
        print("You clicked outside of any island.")
    
    return False  # Return False if the wrong island was clicked or no island was clicked
