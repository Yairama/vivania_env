import sys

import pygame
from engine.utils import Dijkstra
import os, sys
from pygame._sdl2 import Window, Renderer

class RenderCore(pygame.sprite.Group):
    def __init__(self, render_name, path_finder, hidden):
        super().__init__()

        pygame.init()
        self.path_finder = path_finder
        # Screen information
        self.WIDTH = 1280
        self.HEIGHT = 720
        if hidden:
            self.display_surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags=pygame.HIDDEN)
        else:
            self.display_surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        #pygame.event.set_grab(True)
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Comic Sans MS", 12)
        self.drawables = {}
        self.shovels_dict = {}
        self.dumps_dict = {}
        self.animation_speed = 750
        # self.display_surface = pygame.display.get_surface()
        self.render_name = render_name
        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.window_pixel_matrix = None

        # box setup
        self.camera_borders = {'left': 50, 'right': 50, 'top': 50, 'bottom': 50}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # # ground
        # self.ground_surf = pygame.image.load('resources/empty_truck.png').convert_alpha()
        # self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.5

        # zoom
        self.zoom_scale = 0.9
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w + 220
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h - 270

        self.load_spots = list
        self.dump_spots = list
        self.waste_tonnes = 0.
        self.mineral_tonnes = 0.
        self.tonnage = 0.
        self.score = 0.
        self.reward = 0.
        self.queue = 0.
        self.hang = 0.

        pygame.display.set_caption(render_name)

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border, mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos((right_border, mouse.y))
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
                pygame.mouse.set_pos((left_border, top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
                pygame.mouse.set_pos((right_border, top_border))
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
                pygame.mouse.set_pos((left_border, bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
                pygame.mouse.set_pos((right_border, bottom_border))

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x, top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x, bottom_border))

        self.offset += mouse_offset_vector * self.mouse_speed

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.1

    def render(self, **kwargs):
        # self.center_target_camera(player)
        # self.box_target_camera(player)
        # self.keyboard_control()
        self.reward = 0.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # if event.type == pygame.MOUSEWHEEL:
            #     self.zoom_scale += event.y * 0.03

        self.display_surface.fill('#FFFFFF')

        self.update()
        self.draw()
        fps_text = self.font.render(f'{self.render_name} - {round(self.clock.get_fps())} FPS', False, (0, 0, 0))
        self.display_surface.blit(fps_text, (10, 10))
        stats_text = self.font.render(f'Score: {round(self.score,1)}'
                                      f' // Total Queue:{round(self.queue,1)} // Total Hang: {round(self.hang,1)} '
                                      f'// Total Tonnage: {round(self.waste_tonnes+self.mineral_tonnes)}', False, (0, 0, 0))
        self.display_surface.blit(stats_text, (self.WIDTH-610, self.HEIGHT - 50))
        pygame.display.update()
        self.clock.tick(self.FPS)
        self.window_pixel_matrix = pygame.surfarray.array3d(self.display_surface)
        self.window_pixel_matrix = self.window_pixel_matrix.transpose([1, 0, 2])


    def draw(self):
        # self.mouse_control()
        # self.zoom_keyboard_control()

        self.internal_surf.fill('#BBBBBB')

        # ground
        # ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        # self.internal_surf.blit(self.ground_surf, ground_offset)
        for item in self.drawables.values():
            item.draw(self.internal_surf, (- self.offset + self.internal_offset))
        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)

    def get_internal_surface(self):
        return self.internal_surf

    def get_display_surface(self):
        return self.display_surface

    def add_drawables(self, drawables: dict):
        self.drawables.update(drawables)

    def get_delta(self):
        return self.clock.get_time()

    def get_animation_speed(self):
        return self.animation_speed

    def find_path(self, node_root):
        return self.path_finder.naive_dijkstra(node_root)[1]

    def set_shovels(self, shovels_dict):
        self.shovels_dict = shovels_dict

    def set_dumps(self, dumps_dict):
        self.dumps_dict = dumps_dict

    def get_pixel_image(self):
        return self.window_pixel_matrix

    def quit(self):
        pygame.quit()
        sys.exit()
