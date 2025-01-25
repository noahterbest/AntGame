# By Noah TerBest

import pygame
from entities import BlackAnt, GreenAnt, RedAnt

class SpriteManager:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.ants = pygame.sprite.Group()

    def add_ant(self, ant_type, x, y, map_width, map_height, scale_factor):
        ant_classes = {
            "BlackAnt": BlackAnt,
            "GreenAnt": GreenAnt,
            "RedAnt": RedAnt
        }
        if ant_type in ant_classes:
            ant = ant_classes[ant_type](x, y, map_width, map_height, scale_factor)
            self.all_sprites.add(ant)
            self.ants.add(ant)
            return ant
        return None

    def update(self):
        self.all_sprites.update()

    def draw(self, screen):
        self.all_sprites.draw(screen)