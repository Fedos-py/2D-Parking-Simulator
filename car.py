from math import sin, radians, degrees, copysign, cos
from pygame.math import Vector2
import pygame
import os


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0, *group):
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

        self.acceleration = 0.0
        self.steering = 0.0

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir + '/Images/Cars/', "car.png")
        self.initial_car_image = pygame.image.load(image_path)
        self.image = self.initial_car_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        #print('vel: {}, acc: {}'.format(self.velocity, self.acceleration))
        self.velocity += self.acceleration * dt
        self.velocity = max(-self.max_velocity, min(self.velocity, self.max_velocity))


        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity / turning_radius
        else:
            angular_velocity = 0

        l = self.velocity * dt * 32
        sin_a = sin(radians(-self.angle))
        cos_a = cos(radians(-self.angle))
        self.position_x += cos_a * l
        self.position_y += sin_a * l
        self.angle += degrees (angular_velocity) * dt


        self.image = pygame.transform.rotate(self.initial_car_image, self.angle)
        self.rect_image = self.image.get_rect(center=(self.position_x, self.position_y))
        self.rect = pygame.Rect(self.position_x - self.rect_image.w // 2 , self.position_y - self.rect_image.h // 2, self.rect_image.w, self.rect_image.h)

