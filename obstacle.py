from math import sin, radians, degrees, copysign, cos
import pygame
import os


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, name, x, y, *group):
        super().__init__(*group)
        self.name = name
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir + '/Images/Obstacles/', self.name)
        self.image = pygame.image.load(image_path)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.pos = (x, y)

        self.moveable = False
        #pygame.draw.rect(self.screen, pygame.Color('white'), self.rect, 4)
        #print('загрузили конус')

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        pass
        #print('конус на поле')

class Area(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, *group):
        super().__init__(*group)
        surf = pygame.Surface((w, h))
        pygame.draw.rect(surf, pygame.Color('pink'), (x, y, w, h), 3)

        #self.screen.blit(car_image, car_pos)
        self.image = surf
        self.rect = self.image.get_rect()
        self.area_mask = pygame.mask.from_surface(surf)
        self.pos = (0, 0)


class Margine(pygame.sprite.Sprite):
    def __init__(self, image, x, y, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
