# By Noah TerBest

import pygame
from assets import Ant

version = "2025.1.0"
print(" ")
print("Game version: " + version)

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ant Game")
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Spacebar pressed.")
                    print(Ant.speak(self))
                    pass
                if event.key == pygame.K_UP:
                    print("Up pressed.")
                    pass
                if event.key == pygame.K_DOWN:
                    print("Down pressed.")
                    pass
                if event.key == pygame.K_LEFT:
                    print("Left pressed.")
                    pass
                if event.key == pygame.K_RIGHT:
                    print("Right pressed.")
                    pass

    def update(self):
        # This is where you would update the game state, like moving objects or checking for collisions.
        pass

    def draw(self):
        # Handles rendering. Here, you'd draw sprites, backgrounds, etc.
        self.screen.fill((0, 0, 0)) #Black background
        pass

    def run(self):
        # Main loop keeps it running, and at a certain FPS
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

# Usage
if __name__ == "__main__":
    engine = GameEngine(800, 600)
    engine.run()