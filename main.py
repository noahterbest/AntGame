# By Noah TerBest

import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from sprites import SpriteManager
from utils import *
from entities import *

version = "2025.1.24"

print()  # Print a blank line for console separation


class GameEngine:
    def __init__(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Ant Game")
            self.clock = pygame.time.Clock()
            self.running = True
            self.scale_factor = 2

            self.sprite_manager = SpriteManager()

            self.map_data = [
                'AAAAAAAAAAAAAAAAAAAAAAAAAA',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'TTTTTTTTTTTTT',
                'DDDDDDDDDDDDD',
                'DDDDDDDDDDDDD',
                'DDDDDDDDDDDDD',
                'DDDDDDDDDDDDD',
                'DDDDDDDDDDDDD',
                'DDDDDDDDDDDDD',
                'DDDDDDDDDDDDD',
                'DDDDDDDDDDDDD'
            ]

            self.tile_size = 32
            self.tile_map = TileMap('map.txt', self.tile_size * self.scale_factor, default_map_data=self.map_data,
                                    scale_factor=self.scale_factor)
            self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.camera.scale_factor = self.scale_factor
            self.camera.set_map_dimensions(
                len(self.tile_map.map_data[0]) * self.tile_size * self.scale_factor,
                len(self.tile_map.map_data) * self.tile_size * self.scale_factor
            )

            self.try_load_background()
            self.try_initialize_ants()

            self.scaled_surface = pygame.Surface(
                (SCREEN_WIDTH // self.scale_factor, SCREEN_HEIGHT // self.scale_factor))

            print(f"Load complete! Running game version: {version}")

        except Exception as e:
            print(f"An error occurred during game initialization: {e}")
            pygame.quit()
            raise

    def try_load_background(self):
        try:
            self.background = load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)

    def try_initialize_ants(self):
        map_width = len(self.map_data[0]) * self.tile_size
        map_height = len(self.map_data) * self.tile_size
        try:
            valid_x, valid_y = self.find_valid_spawn()
            self.black_ant = self.sprite_manager.add_ant("BlackAnt", valid_x // self.scale_factor, valid_y // self.scale_factor, map_width, map_height, self.scale_factor)
            self.green_ant = self.sprite_manager.add_ant("GreenAnt", 200 // self.scale_factor, 100 // self.scale_factor, map_width, map_height, self.scale_factor)
            self.red_ant = self.sprite_manager.add_ant("RedAnt", 100 // self.scale_factor, 150 // self.scale_factor, map_width, map_height, self.scale_factor)
            print(f"Loaded Ant class version: {Ant.version}")
        except Exception as e:
            print(f"Error initializing characters: {e}")
            self.black_ant = self.green_ant = self.red_ant = None

    def find_valid_spawn(self):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile in ['D', 'T']:
                    return x * self.tile_size, y * self.tile_size
        return 0, 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.black_ant:
                    print("Spacebar pressed.")
                    print(self.black_ant.speak())
                elif event.key == pygame.K_ESCAPE:
                    print("User initiated shutdown procedure.")
                    print("Shutting down..")
                    self.running = False

    def update(self):
        if self.black_ant:
            keys = pygame.key.get_pressed()
            vertical_move = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
            horizontal_move = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])

            if vertical_move != 0 and self.black_ant.move(0, vertical_move, self.tile_map):
                self.camera.update(self.black_ant)
            if horizontal_move != 0 and self.black_ant.move(horizontal_move, 0, self.tile_map):
                self.camera.update(self.black_ant)

    def draw(self):
        self.scaled_surface.fill(BLACK)
        self.tile_map.render(self.scaled_surface, self.camera.x // self.scale_factor,
                             self.camera.y // self.scale_factor)

        for ant in [self.black_ant, self.green_ant, self.red_ant]:
            if ant:
                adjusted_x = ant.rect.x - (self.camera.x // self.scale_factor)
                adjusted_y = ant.rect.y - (self.camera.y // self.scale_factor)
                self.scaled_surface.blit(ant.image, (adjusted_x, adjusted_y))

        scaled_scene = pygame.transform.scale(self.scaled_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_scene, (0, 0))

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                pygame.display.flip()
                self.clock.tick(FPS)
        except Exception as e:
            print(f"An error occurred during the game loop: {e}")
        finally:
            pygame.quit()


if __name__ == "__main__":
    try:
        GameEngine().run()
    except Exception as e:
        print(f"Fatal error in game execution: {e}")