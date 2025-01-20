import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from sprites import SpriteManager
from utils import load_image
from entities import *

version = "2025.1.19.2"

class GameEngine:
    def __init__(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Ant Game")
            self.clock = pygame.time.Clock()
            self.running = True

            self.sprite_manager = SpriteManager()

            # Load background
            try:
                self.background = load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
            except Exception as e:
                print(f"Error loading background: {e}")
                self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.background.fill(BLACK)

            # Load Characters
            try:
                self.black_ant = self.sprite_manager.add_ant("BlackAnt", 400, 300)
                self.green_ant = self.sprite_manager.add_ant("GreenAnt", 200, 100)
                self.red_ant = self.sprite_manager.add_ant("RedAnt", 100, 150)
                if self.black_ant:
                    print(f"Loaded Ant version: {BlackAnt.version}")
                if self.green_ant:
                    print(f"Loaded Green Ant version: {GreenAnt.version}")
                if self.red_ant:
                    print(f"Loaded Red Ant version: {RedAnt.version}")
            except Exception as e:
                print(f"Error initializing characters: {e}")
                self.black_ant = None
                self.green_ant = None

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
                if event.key == pygame.K_SPACE and self.character:
                    print("Spacebar pressed.")
                    print(self.character.speak())
                if event.key == pygame.K_ESCAPE:
                    print("User initiated shutdown procedure.")
                    print("Shutting down..")
                    self.running = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Black ant character movement
        if self.black_ant:
            self.black_ant.move(0, -1 if keys[pygame.K_UP] else 1 if keys[pygame.K_DOWN] else 0)
            self.black_ant.move(-1 if keys[pygame.K_LEFT] else 1 if keys[pygame.K_RIGHT] else 0, 0)

        # Green ant character movement
        if self.green_ant:
            self.green_ant.move(0, -1 if keys[pygame.K_w] else 1 if keys[pygame.K_s] else 0)
            self.green_ant.move(-1 if keys[pygame.K_a] else 1 if keys[pygame.K_d] else 0, 0)

        self.sprite_manager.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.sprite_manager.draw(self.screen)

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