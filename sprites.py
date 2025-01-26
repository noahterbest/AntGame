# By Noah TerBest

import pygame
import entities

class SpriteManager:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.ants = pygame.sprite.Group()

    def add_ant(self, ant_type, x, y, map_width, map_height):
            ant_class_mapping = {
                'BlackAnt': entities.BlackAnt,
                'GreenAnt': entities.GreenAnt,
                'RedAnt': entities.RedAnt,
            }
            if ant_type not in ant_class_mapping:
                raise ValueError(f"Unknown ant type: {ant_type}")
            ant = ant_class_mapping[ant_type](x, y, map_width, map_height)
            self.all_sprites.add(ant)
            self.ants.add(ant)
            return ant

    def update(self):
        self.all_sprites.update()

    def draw(self, screen):
        self.all_sprites.draw(screen)