#By Noah TerBest

import pygame
import os

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
    def __init__(self, map_data, tile_size):
        self.map_data = map_data
        self.tile_size = tile_size
        self.width = len(map_data[0])
        self.height = len(map_data)
        self.tiles = self.load_tiles()

    def load_tiles(self):
        tiles = {}
        # Load tiles from images. Here, we're using a placeholder for simplicity
        tiles['D'] = pygame.image.load('assets/tiles/dirt.png').convert_alpha() #Dark Dirt Tile
        tiles['T'] = pygame.image.load('assets/tiles/tunnel.png').convert_alpha() #Tunnel Tile
        tiles['A'] = pygame.image.load('assets/tiles/air.png').convert_alpha() # Air Tile
        return tiles

    def get_tile_image(self, tile_char):
        return self.tiles.get(tile_char, None) #Returns none if tile_char is not found

    def render(self, surface, camera_x, camera_y):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile != '-':
                    image = self.get_tile_image(tile)
                    if image:
                        surface.blit(image, (x * self.tile_size - camera_x, y * self.tile_size - camera_y))

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.map_width = 0

    def set_map_width(self, map_width):
        self.map_width = map_width

    def apply(self, target):
        return target.rect.move(-self.x, -self.y)

    def update(self, target):
        # Basic camera follow; you'll want to adjust this for more complex behavior
        new_x = max(0, min(target.rect.x - self.width // 2, self.map_width * 64 - self.width))
        self.x = new_x