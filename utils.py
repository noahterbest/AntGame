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
    def __init__(self, map_file, tile_size, default_map_data=None):
        self.tile_size = tile_size
        if os.path.exists(os.path.join(os.environ.get('ASSET_PATH', 'assets'), map_file)):
            self.map_data = self.load_map_from_file(map_file)
        else:
            print(f"Map file '{map_file}' not found, using default map data.")
            self.map_data = default_map_data
        self.width = len(self.map_data[0])
        self.height = len(self.map_data)
        self.tiles = self.load_tiles()

    def load_map_from_file(self, map_file):
        asset_path = os.environ.get('ASSET_PATH', 'assets')
        full_path = os.path.join(asset_path, map_file)
        with open(full_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def load_tiles(self):
        tiles = {}
        # Load tiles from images. Here, we're using a placeholder for simplicity
        tiles['D'] = pygame.image.load('assets/tiles/dirt.png').convert_alpha() #Dark Dirt Tile
        tiles['T'] = pygame.image.load('assets/tiles/tunnel.png').convert_alpha() #Tunnel Tile
        tiles['A'] = pygame.image.load('assets/tiles/air.png').convert_alpha() # Air Tile
        tiles['H'] = pygame.image.load('assets/tiles/horizon.png').convert_alpha()  # Air Tile
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
        self.map_height = 0

    def set_map_dimensions(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, target):
        # Adjust the target's position by the camera's offset
        return target.rect.move(-self.x, -self.y)

    def update(self, target):
        # Update camera position based on target's position but within the map bounds
        new_x = max(0, min(target.rect.x - self.width // 2, self.map_width - self.width))
        new_y = max(0, min(target.rect.y - self.height // 2, self.map_height - self.height))
        self.x = new_x
        self.y = new_y