#By Noah TerBest

import pygame
from entities import Ant, GreenAnt, BlackAnt, RedAnt
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class SpriteManager:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.ants = pygame.sprite.Group()

    def add_ant(self, ant_type, x, y):
        ant = None
        if ant_type == "BlackAnt":
            ant = BlackAnt(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif ant_type == "GreenAnt":
            ant = GreenAnt(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif ant_type == "RedAnt":
            ant = RedAnt(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)

        if ant:
            self.all_sprites.add(ant)
            self.ants.add(ant)
        return ant

    def update(self):
        self.all_sprites.update()

    def draw(self, screen):
        self.all_sprites.draw(screen)