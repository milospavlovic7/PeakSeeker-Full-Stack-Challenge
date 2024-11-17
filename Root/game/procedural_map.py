from perlin_noise import PerlinNoise
import config
import time

def generate_map():
    """
    Generates a procedural map using Perlin noise with water (0) and islands with heights from 1 to 1000.
    The map will look like islands with lots of water and groups of cells representing islands.
    """
    
    grid_size = config.GRID_SIZE
    scale = 30.0  # Control the size of the noise features (lower values = larger features, more island-like)
    octaves = 6  # Number of layers of noise (higher = more detail)

    # Generate a dynamic seed based on time to get different results each time
    seed = int(time.time())
    
    # Create a PerlinNoise instance with dynamic seed
    noise = PerlinNoise(octaves=octaves, seed=seed)  # Only pass `octaves` and `seed`

    # Create an empty map
    map_matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Generate the map using Perlin noise
    for y in range(grid_size):
        for x in range(grid_size):
            # Generate Perlin noise at each point
            nx = x / scale
            ny = y / scale
            noise_value = noise([nx, ny])  # Generate noise at point (nx, ny)
            
            # Map noise value to a height between 0 and 1000
            height = int(noise_value * 500 + 500)  # This scales the value between -500 and +500, then shifts to [0, 1000]

            # Use a threshold to create "islands" (higher values = land, lower = water)
            if height < 524:  # Consider values below 500 as water (0)
                height = 0
            else:
                # Increase the height of land islands by using a higher scaling factor
                height = int((height - 524) * 4)  # Scaling factor increased to 3 to make islands higher

            map_matrix[y][x] = height

    return map_matrix
