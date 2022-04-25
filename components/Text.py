import pygame
from pygame.math import Vector2, Vector3


class Text(pygame.sprite.Sprite):
    def __init__(self, group, text, size, color, width, height, pos):
        # Call the parent class (Sprite) constructor
        super().__init__(group)
        # pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width / 2 - W / 2, height / 2 - H / 2])
        self.pos = pos
        self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))

    def update_pos(self, pos):
        self.pos = pos + Vector3(20, 15, 0)
        self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))
