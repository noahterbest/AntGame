#By Noah TerBest

import pygame
from utils import load_image
from constants import ANT_SIZE, ANT_SPEED


class Ant(pygame.sprite.Sprite):
    version = "25.1.0"
    health = 100
    def __init__(self, x, y, screen_width, screen_height, image_path):
        super().__init__()
        try:
            # Note the order: path first, then size
            self.image = load_image(image_path, (ANT_SIZE, ANT_SIZE))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = ANT_SPEED
            self.screen_width = screen_width
            self.screen_height = screen_height
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

        # Check if new position is within screen boundaries
        if 0 <= new_x <= self.screen_width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= self.screen_height - self.rect.height:
            self.rect.y = new_y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlackAnt(Ant):
    version = "25.1.19.1"
    health = 100
    def __init__(self, x, y, screen_width, screen_height):
        try:
            super().__init__(x, y, screen_width, screen_height, 'black_ant.png')
        except Exception as e:
            print(f"Error initializing BlackAnt: {e}")
            # If the parent class initialization fails, we'll just use a default Ant

    def speak(self):
        return "Doing Black"


class GreenAnt(Ant):
    version = "25.1.19.1"
    health = 100
    def __init__(self, x, y, screen_width, screen_height):
        try:
            super().__init__(x, y, screen_width, screen_height, 'green_ant.png')
        except Exception as e:
            print(f"Error initializing GreenAnt: {e}")
            # If the parent class initialization fails, we'll just use a default Ant

    def speak(self):
        return "Doing Green"


class RedAnt(Ant):
    version = "25.1.19.1"
    health = 100
    def __init__(self, x, y, screen_width, screen_height):
        try:
            super().__init__(x, y, screen_width, screen_height, 'red_ant.png')
        except Exception as e:
            print(f"Error initializing RedAnt: {e}")
            # If the parent class initialization fails, we'll just use a default Ant

    def speak(self):
        return "Doing Red"