import pygame
import os
from car import *


TRAINING_AREA_W = 1280
TRAINING_AREA_H = 720

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.screen = pygame.display.set_mode((TRAINING_AREA_W, TRAINING_AREA_H))
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
        self.mod_on = False

        while not self.exit:
            dt = self.clock.get_time() / 1000
            rotated = pygame.transform.rotate(car_image, car.angle)
            gr = rotated.get_rect()
            rect = pygame.Rect(car.position_x - gr.w // 2, car.position_y - gr.h // 2, gr.w, gr[3])
            #print(rect)


            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                print(rect)
                if rect.x > 0 and rect.y > 0:
                    if car.velocity < 0:
                        car.acceleration = car.brake_deceleration
                    else:
                        car.acceleration += 1 * dt
                else:
                    car.velocity =  0
                    car.position_x += 5
                    car.position_y += 5
                if  rect.x + rect.w < TRAINING_AREA_W and  rect.y + rect.h < TRAINING_AREA_H:
                    if car.velocity < 0:
                        car.acceleration = car.brake_deceleration
                    else:
                        car.acceleration += 1 * dt
                else:
                    car.velocity =  0
                    car.position_x -= 5
                    car.position_y -= 5
            elif pressed[pygame.K_DOWN]:
                print(rect)
                if rect.x > 0 and rect.y > 0:
                    print(1)
                    if car.velocity < 0:
                        car.acceleration = -car.brake_deceleration
                    else:
                        car.acceleration -= 1 * dt
                else:
                    print(2)
                    car.velocity = 0
                    car.position_x += 5
                    car.position_y += 5
                if rect.x + rect.w < TRAINING_AREA_W and rect.y + rect.h < TRAINING_AREA_H:
                    print(3)
                    if car.velocity < 0:
                        car.acceleration = -car.brake_deceleration
                    else:
                        print(123)
                        car.acceleration -= 1 * dt
                else:
                    print(4)
                    car.velocity = 0
                    car.position_x -= 5
                    car.position_y -= 5
            elif pressed[pygame.K_SPACE]: # тормозим
                if abs(car.velocity) > dt * car.brake_deceleration: # не можем затормозить за 1 кадр
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity)
                else: # можем затормозить за 1 кадр
                    car.acceleration = -car.velocity / dt
            else: # ни одна клавиша не нажата
                if abs(car.velocity) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_MINUS]:
                print('включили невидимку')
                self.mod_on = True
                print(self.mod_on)

            if pressed[pygame.K_EQUALS]:
                print('выключили невидимку')
                self.mod_on = False
                print(self.mod_on)

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))



            # Logic

            car.update(dt)

            #print(rect)
            if rect.x > 0 and rect.y > 0:
                if car.velocity < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            else:
                car.velocity = 0
                car.position_x += 5
                car.position_y += 5
            if rect.x + rect.w < TRAINING_AREA_W and rect.y + rect.h < TRAINING_AREA_H:
                if car.velocity < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            else:
                car.velocity = 0
                car.position_x -= 5
                car.position_y -= 5
            #print(rect.x)
            if rect.x + 5 + rect.w // 2 >= TRAINING_AREA_W or rect.y + 5 >= TRAINING_AREA_H:
                car.position_x = 250
                car.position_y = 250
            # Drawing
            self.screen.fill((0, 0, 0))
            if self.mod_on:
                font = pygame.font.Font('13888.otf', 100)
                text = font.render('speed: {}'.format(round(car.velocity, 2)), True, pygame.Color('red'))
                self.screen.blit(text, (10, 10))
            pygame.draw.rect(self.screen, pygame.Color('red'), rect, 3)
            #print(car.position_x, car.position_y)
            self.screen.blit(rotated, (car.position_x * ppu - rect[2] / 2, car.position_y * ppu - rect[3] / 2))
            #pygame.draw.rect(self.screen, pygame.Color('white'), (15, 15, 100, 100), 20)
            pygame.display.flip()
            #print(i)
            i += 1
            if i == 0:
                self.plus_nos = rect[2] // 2


            self.clock.tick(self.ticks)
        pygame.quit()