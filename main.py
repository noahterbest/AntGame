# By Noah TerBest

import pygame
from assets import Ant, doShit, greenAnt

version = "2025.1.0.2"

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        try:
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Ant Game")
            self.clock = pygame.time.Clock()
            self.running = True

            # Load background
            try:
                self.background = pygame.image.load("assets/background.png").convert()
                self.background = pygame.transform.scale(self.background, (width, height))
                self.original_background = self.background.copy()
                self.original_width, self.original_height = self.screen.get_size()
            except pygame.error as e:
                print(f"Error loading background image: {e}")
                # Fallback to a solid color if background image fails to load
                self.background = pygame.Surface((width, height))
                self.background.fill((0, 0, 0))  # Black background

            # Load Character
            try:
                self.character = Ant(400, 300, width, height)
                print("Loaded Ant version: " + Ant.version)
            except Exception as e:
                print(f"Error initializing Ant: {e}")
                self.character = None  # Handle the case where Ant initialization fails

            # Load Green Ant
            try:
                self.greenAnt = greenAnt(200, 100, width, height)
                print("Loaded Green Ant version: " + greenAnt.version)
            except Exception as e:
                print(f"Error initializing Green Ant: {e}")
                self.greenAnt = None  # Handle the case where Green Ant initialization fails

            ##END OF CODE
            print("Load complete! Running game version: " + version)
        except Exception as e:
            print(f"An error occurred during game initialization: {e}")
            pygame.quit()
            raise  # Re-raise the exception to stop the program if initialization fails

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.character:  # Check if character was successfully initialized
                        print("Spacebar pressed.")
                        print(self.character.speak())
                if event.key == pygame.K_ESCAPE:
                    print("User initiated shutdown procedure.")
                    print("Shutting down..")
                    self.running = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Black ant character movement
        if self.character:  # Only move if character exists
            if keys[pygame.K_UP]:
                self.character.move(0, -1)
            if keys[pygame.K_DOWN]:
                self.character.move(0, 1)
            if keys[pygame.K_LEFT]:
                self.character.move(-1, 0)
            if keys[pygame.K_RIGHT]:
                self.character.move(1, 0)

        # Green ant character movement
        if self.greenAnt:  # Only move if greenAnt exists
            if keys[pygame.K_w]:
                self.greenAnt.move(0, -1)
            if keys[pygame.K_s]:
                self.greenAnt.move(0, 1)
            if keys[pygame.K_a]:
                self.greenAnt.move(-1, 0)
            if keys[pygame.K_d]:
                self.greenAnt.move(1, 0)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.character:
            self.character.draw(self.screen)
        if self.greenAnt:
            self.greenAnt.draw(self.screen)

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                pygame.display.flip()
                self.clock.tick(60)
        except Exception as e:
            print(f"An error occurred during the game loop: {e}")
        finally:
            pygame.quit()

# Usage
if __name__ == "__main__":
    try:
        engine = GameEngine(800, 600)
        engine.run()
    except Exception as e:
        print(f"Fatal error in game execution: {e}")