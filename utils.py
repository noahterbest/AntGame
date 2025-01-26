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
    def __init__(self, map_file, tile_size, default_map_data=None):
        self.tile_size = tile_size

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
        # Load dirt variations correctly sized without scaling
        dirt_variations = [
            load_image('tiles/Dirt1.png', (self.tile_size, self.tile_size)),
            load_image('tiles/Dirt2.png', (self.tile_size, self.tile_size)),
            load_image('tiles/Dirt3.png', (self.tile_size, self.tile_size))
        ]
        dirt_variations = [d for d in dirt_variations]

        # Load other tiles directly with the correct size
        tiles['T'] = load_image('tiles/tunnel.png', (self.tile_size, self.tile_size))
        tiles['A'] = load_image('tiles/air.png', (self.tile_size, self.tile_size))

        # Create a map for dirt tiles
        self.dirt_map = []
        for row in self.map_data:
            dirt_row = []
            for tile in row:
                if tile == 'D':
                    dirt_row.append(random.choice(dirt_variations))
                else:
                    dirt_row.append(None)  # Placeholder for non-dirt tiles
            self.dirt_map.append(dirt_row)

        tiles['D'] = lambda x, y: self.dirt_map[y][x] if self.dirt_map[y][x] else None

        return tiles, self.dirt_map

    def get_tile_image(self, tile_char, x, y):
        if tile_char == 'D':
            return self.tiles[tile_char](x, y)  # Get the pre-randomized dirt tile
        return self.tiles.get(tile_char, None)  # Returns none if tile_char is not found

    # In TileMap's render method, if scaling tiles:
    def render(self, surface, camera_x, camera_y):
        # Calculate the total map height in pixels
        map_pixel_height = len(self.map_data) * self.tile_size
        screen_height = surface.get_height()

        # Only add vertical offset if the map fits within the screen
        vertical_offset = max(0, screen_height - map_pixel_height)

        # Iterate over the map and render only the visible portion
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile != '-':  # Only render visible tiles
                    image = self.get_tile_image(tile, x, y)
                    if image:
                        # Calculate the tile's position on the screen
                        screen_x = x * self.tile_size - camera_x
                        screen_y = y * self.tile_size + vertical_offset - camera_y

                        # Skip rendering tiles outside the screen's view
                        if (-self.tile_size < screen_x < surface.get_width() and
                                -self.tile_size < screen_y < surface.get_height()):
                            surface.blit(image, (screen_x, screen_y))

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.map_width = 0
        self.map_height = 0


    def set_map_dimensions(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, target):
        # Adjust the target's position by the camera's offset, accounting for scaling
        return target.rect.move(-self.x, -self.y)

    def update(self, target):
        # Pan horizontally, center the camera around the target
        self.x = max(0, min(target.rect.x - self.width // 2, self.map_width - self.width))

        # Pan vertically, center the camera around the target
        self.y = max(0, min(target.rect.y - self.height // 2, self.map_height - self.height))
