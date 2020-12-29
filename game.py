import pygame
import os
from car import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False


    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir + '/Images/Cars/', "car.png")
        car_image = pygame.image.load(image_path)
        car = Car(250, 250)
        ppu = 1
        i = 0
        self.plus_nos = 0

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.position_y > 0 - self.plus_nos and car.position_y < 720.00 + self.plus_nos and car.position_x > 0 - self.plus_nos and car.position_x < 1280.0 + self.plus_nos:
                    if car.velocity < 0:
                        car.acceleration = car.brake_deceleration
                    else:
                        car.acceleration += 1 * dt
                else:
                    car.velocity =  0
            elif pressed[pygame.K_DOWN]:
                if car.velocity > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity)
                else:
                    car.acceleration = -car.velocity / dt
            else:
                if abs(car.velocity) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity)
                elif car.position_y > 50.0:
                    car.velocity = 0
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic

            car.update(dt)

            # Drawing
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, car.angle)
            gr = rotated.get_rect()
            rect = (car.position_x - gr.w // 2, car.position_y - gr.h // 2, gr.w, gr[3])
            print(rect)
            pygame.draw.rect(self.screen, pygame.Color('red'), rect, 1)
            print(car.position_x, car.position_y)
            self.screen.blit(rotated, (car.position_x * ppu - rect[2] / 2, car.position_y * ppu - rect[3] / 2))
            #pygame.draw.rect(self.screen, pygame.Color('white'), (15, 15, 100, 100), 20)
            pygame.display.flip()
            print(i)
            i += 1
            if i == 0:
                self.plus_nos = rect[2] // 2


            self.clock.tick(self.ticks)
        pygame.quit()