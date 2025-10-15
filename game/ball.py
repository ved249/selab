# ball.py

import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        """Moves the ball and returns True if a wall bounce occurs."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            return True # Wall bounce occurred
        return False # No bounce

    def check_collision(self, player, ai):
        """Checks for paddle collision and returns True if a hit occurs."""
        collided = False
        # Player collision (left paddle)
        if self.velocity_x < 0 and self.rect().colliderect(player.rect()):
            self.velocity_x *= -1
            self.x = player.x + player.width
            collided = True

        # AI collision (right paddle)
        if self.velocity_x > 0 and self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1
            self.x = ai.x - self.width
            collided = True
        
        return collided

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)