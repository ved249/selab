# game_engine.py

import pygame
import numpy as np  # Import numpy to generate sound data
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

def generate_beep_sound(frequency=440, duration=0.1, sample_rate=44100):
    """Generates a numpy array representing a beep sound."""
    samples = int(sample_rate * duration)
    t = np.linspace(0., duration, samples, endpoint=False)
    # Generate a sine wave
    wave = np.sin(2. * np.pi * frequency * t)
    # Normalize to 16-bit signed integers
    wave = (wave * 32767).astype(np.int16)
    # Pygame's mixer works best with stereo, so we duplicate the channel
    stereo_wave = np.column_stack((wave, wave))
    # Create the sound object from the numpy array buffer
    return pygame.mixer.Sound(buffer=stereo_wave)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5
        self.winner_text = ""

        # Fonts
        self.score_font = pygame.font.SysFont("Arial", 30)
        self.winner_font = pygame.font.SysFont("Arial", 60)
        self.menu_font = pygame.font.SysFont("Arial", 24)
        
        # --- Sound Effects (Generated using NumPy) ---
        # No external files are needed now.
        self.paddle_hit_sound = generate_beep_sound(frequency=440, duration=0.05) # A4 note
        self.wall_bounce_sound = generate_beep_sound(frequency=330, duration=0.05) # E4 note
        self.score_sound = generate_beep_sound(frequency=660, duration=0.1)     # E5 note


        # Game State Management
        self.state = "PLAYING"
        self.should_exit = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if self.state == "PLAYING":
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
        
        elif self.state == "GAME_OVER":
            if keys[pygame.K_3]:
                self.reset_game(3)
            elif keys[pygame.K_5]:
                self.reset_game(5)
            elif keys[pygame.K_7]:
                self.reset_game(7)
            elif keys[pygame.K_ESCAPE]:
                self.should_exit = True

    def update(self):
        if self.state == "PLAYING":
            if self.ball.move(): # Ball hit a wall
                self.wall_bounce_sound.play()
            
            if self.ball.check_collision(self.player, self.ai): # Ball hit a paddle
                self.paddle_hit_sound.play()

            # Scoring logic
            scored = False
            if self.ball.x <= 0:
                self.ai_score += 1
                scored = True
            elif self.ball.x >= self.width:
                self.player_score += 1
                scored = True
            
            if scored:
                self.score_sound.play()
                self.ball.reset()
            
            self.ai.auto_track(self.ball, self.height)
            self.check_for_winner()

    def check_for_winner(self):
        if self.player_score >= self.winning_score:
            self.winner_text = "Player Wins!"
            self.state = "GAME_OVER"
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI Wins!"
            self.state = "GAME_OVER"
            
    def reset_game(self, score_limit):
        """Resets the game for a new match with a new score limit."""
        self.winning_score = score_limit
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.reset()
        self.ai.reset()
        self.state = "PLAYING"

    def render(self, screen):
        if self.state == "GAME_OVER":
            # Display winner text
            win_text_surface = self.winner_font.render(self.winner_text, True, WHITE)
            text_rect = win_text_surface.get_rect(center=(self.width / 2, self.height / 2 - 50))
            screen.blit(win_text_surface, text_rect)

            # Display menu options
            y_offset = self.height / 2 + 20
            options = [
                "Best of 3 (Press 3)",
                "Best of 5 (Press 5)",
                "Best of 7 (Press 7)",
                "Exit (Press ESC)"
            ]
            for i, option in enumerate(options):
                menu_surface = self.menu_font.render(option, True, WHITE)
                menu_rect = menu_surface.get_rect(center=(self.width / 2, y_offset + i * 40))
                screen.blit(menu_surface, menu_rect)
        else: # Render the game being played
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width/2, 0), (self.width/2, self.height))

            player_text = self.score_font.render(str(self.player_score), True, WHITE)
            ai_text = self.score_font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width/4, 20))
            screen.blit(ai_text, (self.width * 3/4, 20))