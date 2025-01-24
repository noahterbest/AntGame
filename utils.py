#By Noah TerBest

import pygame
import os
import random

def load_image(path, size):
    asset_path = os.environ.get('ASSET_PATH', 'assets')
    full_path = os.path.join(asset_path, path)
    try:
        image = pygame.image.load(full_path).convert_alpha()
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image from {full_path}: {e}")
        # Return a placeholder image
        placeholder = pygame.Surface(size, pygame.SRCALPHA)
        placeholder.fill((255, 0, 0))  # Red for visibility
        return placeholder


class TileMap:
    def __init__(self, map_file, tile_size, default_map_data=None, scale_factor=1):
        self.tile_size = tile_size
        self.scale_factor = scale_factor
        if os.path.exists(os.path.join(os.environ.get('ASSET_PATH', 'assets'), map_file)):
            self.map_data = self.load_map_from_file(map_file)
        else:
            print(f"Map file '{map_file}' not found, using default map data.")
            self.map_data = default_map_data
        self.width = len(self.map_data[0])
        self.height = len(self.map_data)

        # Load tiles once here
        self.tiles, self.dirt_map = self.load_tiles()

    def load_map_from_file(self, map_file):
        asset_path = os.environ.get('ASSET_PATH', 'assets')
        full_path = os.path.join(asset_path, map_file)
        with open(full_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def load_tiles(self):
        tiles = {}
        # Load dirt variations at twice the size then scale down for rendering
        dirt_variations = [
            load_image('tiles/Dirt1.png', (self.tile_size, self.tile_size)),
            load_image('tiles/Dirt2.png', (self.tile_size, self.tile_size)),
            load_image('tiles/Dirt3.png', (self.tile_size, self.tile_size))
        ]
        dirt_variations = [pygame.transform.scale(d, (self.tile_size // self.scale_factor, self.tile_size // self.scale_factor)) for d in dirt_variations]

        # Load other tiles at twice the size then scale down for rendering
        tiles['T'] = pygame.transform.scale(load_image('tiles/tunnel.png', (self.tile_size, self.tile_size)), (self.tile_size // self.scale_factor, self.tile_size // self.scale_factor))
        tiles['A'] = pygame.transform.scale(load_image('tiles/air.png', (self.tile_size, self.tile_size)), (self.tile_size // self.scale_factor, self.tile_size // self.scale_factor))

        # Create a map for dirt tiles
        dirt_map = []
        for row in self.map_data:
            dirt_row = []
            for tile in row:
                if tile == 'D':
                    dirt_row.append(random.choice(dirt_variations))
                else:
                    dirt_row.append(None)  # Placeholder for non-dirt tiles
            dirt_map.append(dirt_row)

        tiles['D'] = lambda x, y: dirt_map[y][x] if dirt_map[y][x] else None

        return tiles, dirt_map

    def get_tile_image(self, tile_char, x, y):
        if tile_char == 'D':
            return self.tiles[tile_char](x, y)  # Get the pre-randomized dirt tile
        return self.tiles.get(tile_char, None)  # Returns none if tile_char is not found

    # In TileMap's render method, if scaling tiles:
    def render(self, surface, camera_x, camera_y):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile != '-':
                    image = self.get_tile_image(tile, x, y)
                    if image:
                        # Scale the tile if needed, or adjust rendering for scaled view:
                        scaled_image = pygame.transform.scale(image, (self.tile_size // self.scale_factor, self.tile_size // self.scale_factor))
                        surface.blit(scaled_image, ((x * self.tile_size) // self.scale_factor - camera_x // self.scale_factor,
                                                    (y * self.tile_size) // self.scale_factor - camera_y // self.scale_factor))

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.map_width = 0
        self.map_height = 0
        self.scale_factor = 1  # Default scale factor, updated by GameEngine

    def set_map_dimensions(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, target):
        # Adjust the target's position by the camera's offset, accounting for scaling
        scaled_target_rect = target.rect.copy()
        scaled_target_rect.x *= self.scale_factor
        scaled_target_rect.y *= self.scale_factor
        return scaled_target_rect.move(-self.x, -self.y)

    def update(self, target):
        new_x = max(0, min(target.rect.x * self.scale_factor - self.width // 2, self.map_width - self.width))
        new_y = max(0, min(target.rect.y * self.scale_factor - self.height // 2, self.map_height - self.height))
        self.x = new_x
        self.y = new_y