# By Noah TerBest

import pygame
from entities import BlackAnt, GreenAnt, RedAnt
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class SpriteManager:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.ants = pygame.sprite.Group()

    def add_ant(self, ant_type, x, y, map_width, map_height, scale_factor):
        ant = None
        if ant_type == "BlackAnt":
            ant = BlackAnt(x, y, map_width, map_height, scale_factor)
        elif ant_type == "GreenAnt":
            ant = GreenAnt(x, y, map_width, map_height, scale_factor)
        elif ant_type == "RedAnt":
            ant = RedAnt(x, y, map_width, map_height, scale_factor)

        if ant:
            self.all_sprites.add(ant)
            self.ants.add(ant)
        return ant

    def update(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Ant):
                # Use original_position for game logic if needed
                pass
        self.all_sprites.update()

    def draw(self, screen):
        # Ensure drawing uses the scaled rect for rendering
        self.all_sprites.draw(screen)