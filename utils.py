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