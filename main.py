# By Noah TerBest

import pygame
from assets import Ant, doShit, greenAnt

version = "2025.1.0.2"

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ant Game")
        self.clock = pygame.time.Clock()
        self.running = True

        #Load background
        self.background = pygame.image.load("assets/background.png")
        self.background = pygame.transform.scale(self.background, (width, height))
        self.original_background = self.background.copy()
        self.original_width, self.original_height = self.screen.get_size()

        #Load Character
        self.character = Ant(400, 300, width, height)
        print("Loaded Ant version: " + Ant.version)

        #Load Green Ant
        self.greenAnt = greenAnt(200, 100, width, height)
        print("Loaded Green Ant version: " + greenAnt.version)

        ##END OF CODE
        print("Load complete! Running game version: " + version)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Spacebar pressed.")
                    print(Ant.speak(self))
                if event.key == pygame.K_ESCAPE:
                    print("User initiated shutdown procedure.")
                    print("Shutting down..")
                    self.running = False
                    pass

    def update(self):
        # This is where you would update the game state, like moving objects or checking for collisions.
        keys = pygame.key.get_pressed()

        #Black ant character movement
        if keys[pygame.K_UP]:
            self.character.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.character.move(0, 1)
        if keys[pygame.K_LEFT]:
            self.character.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.character.move(1, 0)

        #Green ant character movement
        if keys[pygame.K_w]:
            self.greenAnt.move(0, -1)
        if keys[pygame.K_s]:
            self.greenAnt.move(0, 1)
        if keys[pygame.K_a]:
            self.greenAnt.move(-1, 0)
        if keys[pygame.K_d]:
            self.greenAnt.move(1, 0)
        pass

    def draw(self):
        # Handles rendering. Here, you'd draw sprites, backgrounds, etc.
        self.screen.blit(self.background, (0, 0))
        self.character.draw(self.screen)
        self.greenAnt.draw(self.screen)
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