import pygame

def doShit():
    return "Doing Shit"

class Ant:
    version = "25.1.0"
    def __init__(self, x, y, screen_width, screen_height):
        self.image = pygame.transform.scale(pygame.image.load('assets/ant.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, dx, dy):
        new_x = self.rect.x + dx * self.speed
        new_y = self.rect.y + dy * self.speed

        #Check if new position is within screen boundaries
        if 0 <= new_x <= self.screen_width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= self.screen_height - self.rect.height:
            self.rect.y = new_y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def speak(self):
        return "Doing Ant"

class greenAnt:
    version = "25.1.0"
    def __init__(self, x, y, screen_width, screen_height):
        self.image = pygame.transform.scale(pygame.image.load('assets/green_ant.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, dx, dy):
        new_x = self.rect.x + dx * self.speed
        new_y = self.rect.y + dy * self.speed

        #Check if new position is within screen boundaries
        if 0 <= new_x <= self.screen_width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= self.screen_height - self.rect.height:
            self.rect.y = new_y

    def draw(self, surface):
            surface.blit(self.image, self.rect)

    def speak(self):
            return "Doing Green"