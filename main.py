# main.py

import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
pygame.mixer.init() # Initialize the sound mixer

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game engine instance
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Game Logic
        engine.handle_input()
        if engine.should_exit:
            running = False
            
        engine.update()

        # Rendering
        SCREEN.fill(BLACK)
        engine.render(SCREEN)
        
        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()