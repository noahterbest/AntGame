# By Noah TerBest
import math
import pygame
from utils import load_image
from constants import ANT_SIZE, ANT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


class Ant(pygame.sprite.Sprite):
    version = "25.1.24"
    health = 100

    def __init__(self, x, y, screen_width, screen_height, map_width, map_height, image_path, scale_factor):
        super().__init__()
        self.map_width, self.map_height = map_width, map_height
        self.scale_factor = scale_factor

        try:
            self.original_image = load_image(image_path, (ANT_SIZE * self.scale_factor, ANT_SIZE * self.scale_factor))
            self.image = pygame.transform.scale(self.original_image, (ANT_SIZE // self.scale_factor, ANT_SIZE // self.scale_factor))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x // self.scale_factor, y // self.scale_factor
            self.speed = ANT_SPEED / self.scale_factor
            self.screen_width, self.screen_height = screen_width // self.scale_factor, screen_height // self.scale_factor
            self.direction = 0
        except Exception as e:
            print(f"Error initializing Ant with image {image_path}: {e}")
            self._handle_image_error()

    def _handle_image_error(self):
        self.image = pygame.Surface((ANT_SIZE // self.scale_factor, ANT_SIZE // self.scale_factor), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x //= self.scale_factor
        self.rect.y //= self.scale_factor
        self.speed = ANT_SPEED / self.scale_factor
        self.screen_width //= self.scale_factor
        self.screen_height //= self.scale_factor

    def move(self, dx, dy, tile_map):
        new_x, new_y = self.rect.x + dx * self.speed, self.rect.y + dy * self.speed
        if self._can_move(new_x, new_y, tile_map):
            self.rect.x, self.rect.y = new_x, new_y
            self._update_direction(dx, dy)
            self._rotate_image()
            return True
        return False

    def _can_move(self, new_x, new_y, tile_map):
        for corner in self._get_corners(new_x, new_y):
            if not self._is_valid_move(corner, tile_map):
                return False
        return True

    def _get_corners(self, new_x, new_y):
        return [
            (new_x, new_y),
            (new_x + self.rect.width - 1, new_y),
            (new_x, new_y + self.rect.height - 1),
            (new_x + self.rect.width - 1, new_y + self.rect.height - 1)
        ]

    def _is_valid_move(self, corner, tile_map):
        corner_tile_x = int(corner[0] // (tile_map.tile_size // self.scale_factor))
        corner_tile_y = int(corner[1] // (tile_map.tile_size // self.scale_factor))
        return (0 <= corner_tile_y < len(tile_map.map_data) and
                0 <= corner_tile_x < len(tile_map.map_data[corner_tile_y]) and
                tile_map.map_data[corner_tile_y][corner_tile_x] not in ['-', 'X', 'O'])

    def _update_direction(self, dx, dy):
        if dx > 0:
            self.direction = 90
        elif dx < 0:
            self.direction = -90
        elif dy < 0:
            self.direction = 0
        elif dy > 0:
            self.direction = 180

    def _rotate_image(self):
        self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (ANT_SIZE // self.scale_factor, ANT_SIZE // self.scale_factor)), -self.direction)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlackAnt(Ant):
    version = "25.1.24"
    health = 100
    def __init__(self, x, y, map_width, map_height, scale_factor):
        super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'black_ant.png', scale_factor)

    def speak(self):
        return "Doing Black"


class GreenAnt(Ant):
    version = "25.1.24"
    health = 100
    def __init__(self, x, y, map_width, map_height, scale_factor):
        super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'green_ant.png', scale_factor)

    def speak(self):
        return "Doing Green"


class RedAnt(Ant):
    version = "25.1.24"
    health = 100
    def __init__(self, x, y, map_width, map_height, scale_factor):
        super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'red_ant.png', scale_factor)

    def speak(self):
        return "Doing Red"