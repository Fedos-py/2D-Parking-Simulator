from math import sin, radians, degrees, copysign, cos
from pygame.math import Vector2


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
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

    def update(self, dt):
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
        self.angle += degrees(angular_velocity) * dt