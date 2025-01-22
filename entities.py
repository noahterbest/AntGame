# By Noah TerBest
import math

import pygame
from utils import load_image
from constants import ANT_SIZE, ANT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


class Ant(pygame.sprite.Sprite):
    version = "25.1.21"
    health = 100
    def __init__(self, x, y, screen_width, screen_height, map_width, map_height, image_path):
        super().__init__()

        self.map_width = map_width
        self.map_height = map_height

        try:
            self.original_image = load_image(image_path, (ANT_SIZE, ANT_SIZE))
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = ANT_SPEED
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.direction = 0  # angle of rotation for image
        except Exception as e:
            print(f"Error initializing Ant with image {image_path}: {e}")
            self.image = pygame.Surface((ANT_SIZE, ANT_SIZE), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = ANT_SPEED
            self.screen_width = screen_width
            self.screen_height = screen_height

    def move(self, dx, dy):
        new_x = self.rect.x + dx * self.speed
        new_y = self.rect.y + dy * self.speed

        # Directly map movement to rotation:
        if dx > 0:  # Moving right, face up
            self.direction = 90
        elif dx < 0:  # Moving left, face down
            self.direction = -90  # or 270
        elif dy < 0:  # Moving up, face right
            self.direction = 0
        elif dy > 0:  # Moving down, face left
            self.direction = 180

        # Rotate the image based on the new direction
        self.image = pygame.transform.rotate(self.original_image, -self.direction)
        self.rect = self.image.get_rect(center=self.rect.center)  # Ensure rotation around center

        # Check if new position is within map boundaries
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= self.map_height - self.rect.height:
            self.rect.y = new_y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlackAnt(Ant):
    version = "25.1.19.1"
    health = 100
    def __init__(self, x, y, map_width, map_height):
        try:
            super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'black_ant.png')
        except Exception as e:
            print(f"Error initializing BlackAnt: {e}")

    def speak(self):
        return "Doing Black"


class GreenAnt(Ant):
    version = "25.1.19.1"
    health = 100
    def __init__(self, x, y, map_width, map_height):
        try:
            super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'green_ant.png')
        except Exception as e:
            print(f"Error initializing GreenAnt: {e}")

    def speak(self):
        return "Doing Green"


class RedAnt(Ant):
    version = "25.1.19.1"
    health = 100
    def __init__(self, x, y, map_width, map_height):
        try:
            super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'red_ant.png')
        except Exception as e:
            print(f"Error initializing RedAnt: {e}")

    def speak(self):
        return "Doing Red"