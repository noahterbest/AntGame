# By Noah TerBest
import math
import pygame
from utils import load_image
from constants import ANT_SIZE, ANT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT



class Ant(pygame.sprite.Sprite):
    version = "25.1.25"
    health = 100

    def __init__(self, x, y, screen_width, screen_height, map_width, map_height, image_path):
        super().__init__()
        self.map_width, self.map_height = map_width, map_height

        try:
            self.original_image = load_image(image_path, (ANT_SIZE, ANT_SIZE))
            self.image = self.original_image
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.speed = ANT_SPEED
            self.screen_width, self.screen_height = screen_width, screen_height
            self.direction = 0
        except Exception as e:
            print(f"Error initializing Ant with image {image_path}: {e}")
            self._handle_image_error()

    def _handle_image_error(self):
        self.image = pygame.Surface((ANT_SIZE, ANT_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y
        self.speed = ANT_SPEED
        self.screen_width = self.screen_width
        self.screen_height = self.screen_height

    def move(self, dx, dy, tile_map):
        new_x, new_y = self.rect.x + dx * self.speed, self.rect.y + dy * self.speed
        print(
            f"Attempting move to: (x: {new_x}, y: {new_y}) from (x: {self.rect.x}, y: {self.rect.y}) with dx={dx}, dy={dy}")
        if self._can_move(new_x, new_y, tile_map):
            print(f"Move valid. Updating to: (x: {new_x}, y: {new_y})")
            self.rect.x, self.rect.y = new_x, new_y
            self._update_direction(dx, dy)
            self._rotate_image()
            return True
        else:
            print("Move blocked!")
        return False

    def _can_move(self, new_x, new_y, tile_map):
        # Ensure ant stays within map bounds
        if new_x < 0 or new_x + self.rect.width > self.map_width:
            print(f"Blocked: Outside horizontal map bounds. new_x={new_x}")
            return False
        if new_y < 0 or new_y + self.rect.height > self.map_height:
            print(f"Blocked: Outside vertical map bounds. new_y={new_y}")
            return False

        # Check collisions with tiles
        for corner in self._get_corners(new_x, new_y):
            print(f"Checking corner at: {corner}")
            if not self._is_valid_move(corner, tile_map):
                print(f"Blocked: Invalid tile at corner {corner}")
                return False

        print("All corners are valid. Move allowed.")
        return True

    def _get_corners(self, new_x, new_y):
        return [
            (new_x, new_y),
            (new_x + self.rect.width - 1, new_y),
            (new_x, new_y + self.rect.height - 1),
            (new_x + self.rect.width - 1, new_y + self.rect.height - 1)
        ]

    def _is_valid_move(self, corner, tile_map):
        # Get the total height of the map in pixels
        map_pixel_height = len(tile_map.map_data) * tile_map.tile_size
        screen_height = pygame.display.get_surface().get_height()

        # Calculate the vertical offset (if the map height is less than the screen height)
        vertical_offset = max(0, screen_height - map_pixel_height)

        # Adjust Y-coordinate for bottom-aligned map
        adjusted_corner_y = corner[1] - vertical_offset

        # Convert the corner's screen position to map tile coordinates
        corner_tile_x = int(corner[0] // tile_map.tile_size)
        corner_tile_y = int(adjusted_corner_y // tile_map.tile_size)

        # Debugging output for visibility (optional, you can remove this later)
        print(
            f"Corner: {corner}, Adjusted Y: {adjusted_corner_y}, maps to tile: (x: {corner_tile_x}, y: {corner_tile_y})"
        )

        # Check if the coordinates are within map bounds and valid tiles are walkable
        if (0 <= corner_tile_y < len(tile_map.map_data) and
                0 <= corner_tile_x < len(tile_map.map_data[corner_tile_y]) and
                tile_map.map_data[corner_tile_y][corner_tile_x] not in ['-', 'X', 'O']):
            return True

        return False

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
        self.image = pygame.transform.rotate(self.original_image, -self.direction)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlackAnt(Ant):
    version = "25.1.25"
    health = 100
    def __init__(self, x, y, map_width, map_height):
        super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'black_ant.png')

    def speak(self):
        return "Doing Black"


class GreenAnt(Ant):
    version = "25.1.25"
    health = 100
    def __init__(self, x, y, map_width, map_height):
        super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'green_ant.png')

    def speak(self):
        return "Doing Green"


class RedAnt(Ant):
    version = "25.1.25"
    health = 100
    def __init__(self, x, y, map_width, map_height):
        super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height, 'red_ant.png')

    def speak(self):
        return "Doing Red"