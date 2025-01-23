#By Noah TerBest

import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from sprites import SpriteManager
from utils import *
from entities import *

version = "2025.1.22"

print(" ") # this is just to add a space between my console output vs pygame's

class GameEngine:
    def __init__(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Ant Game")
            self.clock = pygame.time.Clock()
            self.running = True

            self.sprite_manager = SpriteManager()

            #Tile Map Loader
            self.map_data = [
                'AAAAAAAAAAAAAAAAAAAAAAAAAA',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'TTTTTTTTTTTTTTTTTTTTTTTTTT',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD',
                'DDDDDDDDDDDDDDDDDDDDDDDDDD'
            ]

            self.tile_size = 64
            self.tile_map = TileMap('map.txt', self.tile_size, default_map_data=self.map_data)
            self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.camera.set_map_dimensions(len(self.tile_map.map_data[0]) * self.tile_size, len(self.tile_map.map_data) * self.tile_size)

            # Load background
            try:
                self.background = load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
            except Exception as e:
                print(f"Error loading background: {e}")
                self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.background.fill(BLACK)

            # Load Characters
            try:
                # Calculate map dimensions based on your map_data
                map_width = len(self.map_data[0]) * self.tile_size
                map_height = len(self.map_data) * self.tile_size

                self.black_ant = self.sprite_manager.add_ant("BlackAnt", 400, 300, map_width, map_height)
                self.green_ant = self.sprite_manager.add_ant("GreenAnt", 200, 100, map_width, map_height)
                self.red_ant = self.sprite_manager.add_ant("RedAnt", 100, 150, map_width, map_height)
                print(f"Loaded Ant class version: {Ant.version}")

            except Exception as e:
                print(f"Error initializing characters: {e}")
                self.black_ant = None
                self.green_ant = None
                self.red_ant = None  # Ensure red_ant is set to None if there's an error

            print(f"Load complete! Running game version: {version}")
        except Exception as e:
            print(f"An error occurred during game initialization: {e}")
            pygame.quit()
            raise

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.black_ant:  # Changed to black_ant since self.character was not defined
                    print("Spacebar pressed.")
                    print(self.black_ant.speak())
                if event.key == pygame.K_ESCAPE:
                    print("User initiated shutdown procedure.")
                    print("Shutting down..")
                    self.running = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Black ant character movement with both arrow keys and WASD
        if self.black_ant:
            # Vertical movement
            vertical_move = 0
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                vertical_move = -1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                vertical_move = 1

            # Horizontal movement
            horizontal_move = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                horizontal_move = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                horizontal_move = 1

            # Apply movement
            if vertical_move != 0:
                self.black_ant.move(0, vertical_move, self.tile_map)
            if horizontal_move != 0:
                self.black_ant.move(horizontal_move, 0, self.tile_map)

            self.camera.update(self.black_ant)

    def draw(self):
        self.screen.fill(BLACK)
        self.tile_map.render(self.screen, self.camera.x, self.camera.y)

        # Draw characters or other game objects with camera offset
        if self.black_ant:
            self.screen.blit(self.black_ant.image, self.camera.apply(self.black_ant))
        if self.green_ant:
            self.screen.blit(self.green_ant.image, self.camera.apply(self.green_ant))
        if self.red_ant:
            self.screen.blit(self.red_ant.image, self.camera.apply(self.red_ant))

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
        engine = GameEngine()
        engine.run()
    except Exception as e:
        print(f"Fatal error in game execution: {e}")