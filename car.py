from file_operations import *
from math import sin, radians, degrees, copysign, cos
from pygame.math import Vector2
import pygame
import os


TRAINING_AREA_W = 1280
TRAINING_AREA_H = 720
MAX_ACCELERATION = 9.0

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=50.0, *group):
        super().__init__(*group)
        self.position_x = x
        self.position_y = y
        self.velocity = 0.0
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2
        self.health = 100
        self.start_point = (0, 0)
        self.finish_point = (0, 0)

        self.acceleration = 0.0
        self.steering = 0.0

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir + '/Images/Cars/', "car.png")
        self.initial_car_image = pygame.image.load(image_path)
        self.image = self.initial_car_image
        self.rect = self.image.get_rect()
        print(self.rect)
        self.longer()
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        #print('vel: {}, acc: {}'.format(self.velocity, self.acceleration))
        self.velocity += self.acceleration * dt
        self.velocity = max(-self.max_velocity, min(self.velocity, self.max_velocity))


        if self.steering: # если рулёжка
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity / turning_radius
        else: # не рулёжка
            angular_velocity = 0

        l = self.velocity * dt * 32
        sin_a = sin(radians(-self.angle))
        cos_a = cos(radians(-self.angle))
        self.position_x += cos_a * l
        self.position_y += sin_a * l
        self.angle += degrees (angular_velocity) * dt


        self.image = pygame.transform.rotate(self.initial_car_image, self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect_image = self.image.get_rect(center=(self.position_x, self.position_y))
        self.rect = pygame.Rect(self.position_x - self.rect_image.w // 2 , self.position_y - self.rect_image.h // 2, self.rect_image.w, self.rect_image.h)

    def ctrl(self, pressed, dt):
        if pressed[pygame.K_UP]: # набираем скорость
            if self.velocity < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration = MAX_ACCELERATION
        elif pressed[pygame.K_DOWN]: # останавливаемся под силой трения или разгоняемся назад.
            if self.velocity < 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= 1 * dt
        elif pressed[pygame.K_LCTRL]:  # тормозим
            if abs(self.velocity) > dt * self.brake_deceleration:  # не можем затормозить за 1 кадр
                self.acceleration = -copysign(self.brake_deceleration, self.velocity)
            else:  # можем затормозить за 1 кадр
                self.acceleration = -self.velocity / dt
        else:  # ни одна клавиша не нажата
            if abs(self.velocity) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity / dt
        if pressed[pygame.K_RIGHT]:
            self.steering -= 30 * dt
        elif pressed[pygame.K_LEFT]:
            self.steering += 30 * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))


    def change_car(self):
        current_dir = fileopen(title="Please select a file", initialdir=f'{os.path.dirname(os.path.abspath(__file__))}/Images/Cars',
                               filetypes=[('Game levels', '*.png'), ('All files', '*.*')])
        image_path = os.path.join(current_dir)
        self.initial_car_image = pygame.image.load(image_path)
        self.image = self.initial_car_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def longer(self, k=2):
        surf = pygame.Surface((self.rect.w * k, self.rect.h))
        surf.blit(self.image, (self.rect.w * (k - 1), 0))
        surf.set_colorkey(pygame.Color('Black'))
        self.initial_car_image = surf