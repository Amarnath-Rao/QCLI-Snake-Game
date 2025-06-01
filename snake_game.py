#!/usr/bin/env python3
"""
Terminal-based Snake Game
A classic Snake game implementation using Python's curses library.
"""
import curses
import random
import time

class SnakeGame:
    """Main Snake game class that handles all game logic and rendering."""
    
    def __init__(self, screen):
        """Initialize the game with the given curses screen."""
        self.screen = screen
        self.setup_screen()
        self.init_game()
    
    def setup_screen(self):
        """Configure the terminal screen for the game."""
        curses.curs_set(0)  # Hide the cursor
        self.screen.timeout(100)  # Set input timeout (controls game speed)
        self.height, self.width = self.screen.getmaxyx()
        
        # Create game window with a border
        self.game_win = curses.newwin(self.height, self.width, 0, 0)
        self.game_win.keypad(1)  # Enable special key input
        self.game_win.timeout(100)  # Set input timeout
        
    def init_game(self):
        """Initialize or reset the game state."""
        # Initialize snake in the middle-left of the screen
        self.snake_x = self.width // 4
        self.snake_y = self.height // 2
        
        # Create initial snake body (3 segments)
        self.snake = [
            [self.snake_y, self.snake_x],
            [self.snake_y, self.snake_x - 1],
            [self.snake_y, self.snake_x - 2]
        ]
        
        # Set initial direction (right)
        self.direction = curses.KEY_RIGHT
        
        # Initialize score
        self.score = 0
        
        # Create initial food
        self.create_food()
        
        # Clear the screen
        self.game_win.clear()
        self.draw_border()
    
    def create_food(self):
        """Create a new food item at a random position."""
        self.food = None
        while self.food is None:
            # Generate random position (accounting for border)
            nf = [
                random.randint(2, self.height - 3),
                random.randint(2, self.width - 3)
            ]
            # Make sure food doesn't appear on the snake
            self.food = nf if nf not in self.snake else None
    
    def draw_border(self):
        """Draw a border around the game area."""
        self.game_win.border(0)
    
    def draw_ui(self):
        """Draw all UI elements including score, snake, and food."""
        # Draw score
        score_text = f" Score: {self.score} "
        self.game_win.addstr(0, 2, score_text)
        
        # Draw food
        self.game_win.addch(self.food[0], self.food[1], '*')
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            char = '@' if i == 0 else '#'  # Different character for head
            self.game_win.addch(segment[0], segment[1], char)
    
    def handle_input(self):
        """Handle keyboard input for controlling the snake."""
        # Get next key press (non-blocking)
        key = self.game_win.getch()
        
        # Update direction if a valid key was pressed
        if key != -1:
            # Prevent 180-degree turns (can't go directly opposite)
            if key == curses.KEY_DOWN and self.direction != curses.KEY_UP:
                self.direction = key
            elif key == curses.KEY_UP and self.direction != curses.KEY_DOWN:
                self.direction = key
            elif key == curses.KEY_LEFT and self.direction != curses.KEY_RIGHT:
                self.direction = key
            elif key == curses.KEY_RIGHT and self.direction != curses.KEY_LEFT:
                self.direction = key
            elif key == ord('q'):  # Allow quitting with 'q'
                return False
        
        return True
    
    def update_game_state(self):
        """Update the game state for the current frame."""
        # Calculate new head position based on current direction
        if self.direction == curses.KEY_DOWN:
            new_head = [self.snake[0][0] + 1, self.snake[0][1]]
        elif self.direction == curses.KEY_UP:
            new_head = [self.snake[0][0] - 1, self.snake[0][1]]
        elif self.direction == curses.KEY_LEFT:
            new_head = [self.snake[0][0], self.snake[0][1] - 1]
        elif self.direction == curses.KEY_RIGHT:
            new_head = [self.snake[0][0], self.snake[0][1] + 1]
        
        # Add new head to the snake
        self.snake.insert(0, new_head)
        
        # Check for collisions with border or self
        if (
            self.snake[0][0] in [0, self.height - 1] or
            self.snake[0][1] in [0, self.width - 1] or
            self.snake[0] in self.snake[1:]
        ):
            # Game over - reset the game
            self.init_game()
            return
        
        # Check if snake ate the food
        if self.snake[0] == self.food:
            # Increase score
            self.score += 1
            
            # Create new food
            self.create_food()
            
            # Speed up the game slightly as score increases
            new_timeout = max(50, 100 - (self.score // 5) * 5)
            self.game_win.timeout(new_timeout)
        else:
            # Remove tail segment if no food was eaten
            tail = self.snake.pop()
            # Erase the tail segment from the screen
            self.game_win.addch(tail[0], tail[1], ' ')
    
    def run(self):
        """Main game loop."""
        while True:
            # Draw the game UI
            self.draw_border()
            self.draw_ui()
            
            # Handle user input
            if not self.handle_input():
                break  # Exit if user quits
            
            # Update game state
            self.update_game_state()
            
            # Refresh the screen
            self.game_win.refresh()

def main():
    """Entry point for the Snake game."""
    # Use curses wrapper to handle terminal setup/cleanup
    curses.wrapper(lambda screen: SnakeGame(screen).run())

if __name__ == "__main__":
    main()
