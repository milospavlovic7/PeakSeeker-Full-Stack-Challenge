import requests

# Function to send a GET request to the URL and parse the data
def fetch_map(url):
    try:
        # Sending GET request to the provided URL
        response = requests.get(url)
        response.raise_for_status()  # If an error occurs, an exception will be raised
        
        # Parsing the data into a 30x30 matrix
        map_data = response.text.split('\n')  # Split the response text by lines
        map_matrix = [list(map(int, row.split())) for row in map_data]  # Convert each row into a list of integers
        return map_matrix
    except requests.exceptions.RequestException as e:
        # Handle errors that occur during the request
        print(f"Error while fetching the map: {e}")
        return None
    except ValueError as e:
        # Handle errors that occur during data parsing
        print(f"Error while parsing the data: {e}")
        return None

# Testing the function - calling it and printing the results
if __name__ == "__main__":
    url = "https://jobfair.nordeus.com/jf24-fullstack-challenge/test"  # Example URL
    map_matrix = fetch_map(url)  # Calling the function with the URL
    if map_matrix:
        # If the map is successfully fetched, print each row
        for row in map_matrix:
            print(row)  # Print the map matrix row by row
