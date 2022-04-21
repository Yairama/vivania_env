import pygame, sys

from components.Worker import Worker


class Truck(pygame.sprite.Sprite):
    def __init__(self, pos, group, worker: Worker, efficiency: float):
        super().__init__(group)
        self.image = pygame.image.load('resources/truck.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed
