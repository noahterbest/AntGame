# By Noah TerBest

import pygame
import os
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from sprites import SpriteManager
from utils import *
from entities import *

version = "2025.1.25"

print()  # Print a blank line for console separation


class GameEngine:
    def __init__(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Ant Game")
            self.clock = pygame.time.Clock()
            self.running = True


            self.sprite_manager = SpriteManager()

            self.map_data = [
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

            self.tile_size = 64

            self.tile_map = TileMap('map.txt', self.tile_size, default_map_data=self.map_data)
            self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.camera.set_map_dimensions(
                len(self.tile_map.map_data[0]) * self.tile_size,
                len(self.tile_map.map_data) * self.tile_size
            )

            self.try_load_background()
            self.try_initialize_ants()



            print(f"Load complete! Running game version: {version}")

        except Exception as e:
            print(f"An error occurred during game initialization: {e}")
            pygame.quit()
            raise

    def try_load_background(self):
        try:
            self.background = load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
            print(f"Background loaded successfully: {self.background}")
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)

    def get_all_valid_spawn_points(self, tile_map):
        valid_spawn_points = []
        map_pixel_height = len(tile_map.map_data) * tile_map.tile_size
        screen_height = pygame.display.get_surface().get_height()
        vertical_offset = screen_height - map_pixel_height  # Vertical offset calculated during rendering

        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile in ['D', 'T']:  # Valid spawn tile types
                    # Calculate tile position adjusted for the rendering offset
                    tiles_below = len(self.map_data) - y - 1
                    adjusted_y = tiles_below * self.tile_size + vertical_offset
                    spawn_x = x * self.tile_size
                    spawn_y = adjusted_y

                    # Ensure these points are valid map positions
                    if self._validate_spawn(spawn_x, spawn_y, tile_map):
                        valid_spawn_points.append((spawn_x, spawn_y))

        return valid_spawn_points

    def _validate_spawn(self, x, y, tile_map):
        """Ensure the spawn point is valid using the same logic as ant movement."""
        for corner in [
            (x, y),
            (x + tile_map.tile_size - 1, y),
            (x, y + tile_map.tile_size - 1),
            (x + tile_map.tile_size - 1, y + tile_map.tile_size - 1)
        ]:
            if not self._is_valid_tile(corner, tile_map):
                return False  # Invalid if any corner is blocked
        return True

    def _is_valid_tile(self, corner, tile_map):
        """Check if a specific corner lies on a valid tile."""
        map_pixel_height = len(tile_map.map_data) * tile_map.tile_size
        screen_height = pygame.display.get_surface().get_height()
        vertical_offset = screen_height - map_pixel_height  # Vertical offset for rendering

        # Adjust for rendering offset
        adjusted_corner_y = corner[1] - vertical_offset
        corner_tile_x = int(corner[0] // tile_map.tile_size)
        corner_tile_y = int(adjusted_corner_y // tile_map.tile_size)

        if (0 <= corner_tile_y < len(tile_map.map_data) and
                0 <= corner_tile_x < len(tile_map.map_data[corner_tile_y]) and
                tile_map.map_data[corner_tile_y][corner_tile_x] not in ['-', 'X', 'O']):
            return True
        return False

    def try_initialize_ants(self):
        map_width = len(self.map_data[0]) * self.tile_size
        map_height = len(self.map_data) * self.tile_size

        try:
            # Collect all valid spawn points
            valid_spawn_points = self.get_all_valid_spawn_points(self.tile_map)

            if not valid_spawn_points:
                raise ValueError("No valid spawn points found on the map!")

            # Randomize Black Ant spawn
            valid_x, valid_y = random.choice(valid_spawn_points)
            self.black_ant = self.sprite_manager.add_ant("BlackAnt", valid_x, valid_y, map_width, map_height)
            valid_spawn_points.remove((valid_x, valid_y))  # Prevent overlap (optional)

            # Randomize Green Ant spawn
            valid_x, valid_y = random.choice(valid_spawn_points)
            self.green_ant = self.sprite_manager.add_ant("GreenAnt", valid_x, valid_y, map_width, map_height)
            valid_spawn_points.remove((valid_x, valid_y))  # Prevent overlap (optional)

            # Randomize Red Ant spawn
            valid_x, valid_y = random.choice(valid_spawn_points)
            self.red_ant = self.sprite_manager.add_ant("RedAnt", valid_x, valid_y, map_width, map_height)
            valid_spawn_points.remove((valid_x, valid_y))  # Prevent overlap (optional)

            print(f"Loaded Ant class version: {Ant.version}")
        except Exception as e:
            print(f"Error initializing characters: {e}")
            self.black_ant = self.green_ant = self.red_ant = None

    def find_valid_spawn(self):
        # Iterate over each row of the map, top-to-bottom
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile in ['D', 'T']:  # Valid spawn tile types
                    # Calculate Y-position based on rows below the current row
                    tiles_below_current_row = len(self.map_data) - y - 1
                    adjusted_y = tiles_below_current_row * self.tile_size
                    # Debug output to check where the spawn is being placed
                    print(
                        f"Tile found at (x: {x}, y: {y}) -> Adjusted spawn position: (x: {x * self.tile_size}, y: {adjusted_y})")
                    return x * self.tile_size, adjusted_y

        # Default spawn location if no valid tile found
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

            if vertical_move != 0:
                self.black_ant.move(0, vertical_move, self.tile_map)
                self.camera.update(self.black_ant)
            if horizontal_move != 0:
                self.black_ant.move(horizontal_move, 0, self.tile_map)
                self.camera.update(self.black_ant)

    def draw(self):
        # 1. Fill the screen with the background first
        self.screen.blit(self.background, (0, 0))

        # 2. Render the tile map
        self.tile_map.render(self.screen, self.camera.x, self.camera.y)

        # 3. Render all ants on the map
        for ant in [self.black_ant, self.green_ant, self.red_ant]:
            if ant:
                adjusted_x = ant.rect.x - self.camera.x
                adjusted_y = ant.rect.y - self.camera.y
                self.screen.blit(ant.image, (adjusted_x, adjusted_y))



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