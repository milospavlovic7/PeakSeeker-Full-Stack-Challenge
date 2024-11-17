class ScoringSystem:
    def __init__(self, initial_lives=3):
        """Initializes the scoring system with a given number of lives."""
        self.correct_attempts = 0  # Number of correct attempts made
        self.lives = initial_lives  # Number of lives the player starts with

    def reset_score(self):
        """Resets the score and number of lives for a new level."""
        self.correct_attempts = 0  # Reset correct attempts
        self.lives = 3  # Reset lives to 3 for the new level

    def increment_attempts(self, is_correct):
        """Increments the number of attempts. If the attempt is correct, 
        increases the correct attempts count. Otherwise, decreases lives."""
        if is_correct:
            self.correct_attempts += 1  # Increase correct attempts if the attempt was correct
        else:
            self.lives -= 1  # Decrease lives if the attempt was incorrect

    def is_game_over(self):
        """Checks if the game is over (i.e., if all lives have been used)."""
        return self.lives <= 0  # Return True if no lives are left

    def get_score(self):
        """Returns the current score, including the number of correct attempts and remaining lives."""
        return {
            "correct_attempts": self.correct_attempts,  # Number of correct attempts
            "lives": self.lives  # Remaining lives
        }

    def print_score(self):
        """Optionally displays the score in the terminal or on screen."""
        print(f"Correct attempts: {self.correct_attempts}, Remaining lives: {self.lives}")
