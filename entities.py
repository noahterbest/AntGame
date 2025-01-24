# By Noah TerBest
import math

import pygame
from utils import load_image
from constants import ANT_SIZE, ANT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


class Ant(pygame.sprite.Sprite):
    version = "25.1.23"
    health = 100

    def __init__(self, x, y, screen_width, screen_height, map_width, map_height, image_path, scale_factor):
        super().__init__()

        self.map_width = map_width
        self.map_height = map_height
        self.scale_factor = scale_factor

        try:
            self.original_image = load_image(image_path, (
            ANT_SIZE * self.scale_factor, ANT_SIZE * self.scale_factor))  # Load at larger size
            # Scale down immediately for rendering
            self.image = pygame.transform.scale(self.original_image, (ANT_SIZE // self.scale_factor, ANT_SIZE // self.scale_factor))
            self.rect = self.image.get_rect()
            self.rect.x = x // self.scale_factor  # Initial position for both rendering and collision
            self.rect.y = y // self.scale_factor

            # Speed should be scaled down since we're rendering smaller but moving on a larger map
            self.speed = ANT_SPEED / self.scale_factor
            self.screen_width = screen_width // self.scale_factor
            self.screen_height = screen_height // self.scale_factor
            self.direction = 0
        except Exception as e:
            print(f"Error initializing Ant with image {image_path}: {e}")
            self.image = pygame.Surface((ANT_SIZE // self.scale_factor, ANT_SIZE // self.scale_factor), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x // self.scale_factor
            self.rect.y = y // self.scale_factor
            self.speed = ANT_SPEED / self.scale_factor
            self.screen_width = screen_width // self.scale_factor
            self.screen_height = screen_height // self.scale_factor

    def move(self, dx, dy, tile_map):
        new_x = self.rect.x + dx * self.speed
        new_y = self.rect.y + dy * self.speed

        # Check collision at the scaled up map size
        corners = [
            (new_x, new_y),
            (new_x + self.rect.width - 1, new_y),  # Right edge
            (new_x, new_y + self.rect.height - 1),  # Bottom edge
            (new_x + self.rect.width - 1, new_y + self.rect.height - 1)  # Bottom-right corner
        ]

        can_move = True
        for corner in corners:
            corner_tile_x = int(corner[0] // (tile_map.tile_size // self.scale_factor))
            corner_tile_y = int(corner[1] // (tile_map.tile_size // self.scale_factor))

            if 0 <= corner_tile_y < len(tile_map.map_data) and 0 <= corner_tile_x < len(tile_map.map_data[corner_tile_y]):
                tile_at_corner = tile_map.map_data[corner_tile_y][corner_tile_x]
                if tile_at_corner in ['-', 'X', 'O']:  # Adjust these based on what blocks movement
                    can_move = False
                    break
            else:
                can_move = False
                break

        if can_move:
            # If movement is allowed, update position
            self.rect.x = new_x
            self.rect.y = new_y

            # Update direction and rotation
            if dx > 0:
                self.direction = 90
            elif dx < 0:
                self.direction = -90
            elif dy < 0:
                self.direction = 0
            elif dy > 0:
                self.direction = 180

            self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (
                ANT_SIZE // self.scale_factor, ANT_SIZE // self.scale_factor)), -self.direction)
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlackAnt(Ant):
    version = "25.1.23"
    health = 100
    def __init__(self, x, y, map_width, map_height, scale_factor):
        try:
            super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'black_ant.png', scale_factor)
        except Exception as e:
            print(f"Error initializing BlackAnt: {e}")

    def speak(self):
        return "Doing Black"


class GreenAnt(Ant):
    version = "25.1.23"
    health = 100
    def __init__(self, x, y, map_width, map_height, scale_factor):
        try:
            super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'green_ant.png', scale_factor)
        except Exception as e:
            print(f"Error initializing GreenAnt: {e}")

    def speak(self):
        return "Doing Green"


class RedAnt(Ant):
    version = "25.1.23"
    health = 100
    def __init__(self, x, y, map_width, map_height, scale_factor):
        try:
            super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'red_ant.png', scale_factor)
        except Exception as e:
            print(f"Error initializing RedAnt: {e}")

    def speak(self):
        return "Doing Red"