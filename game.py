import pygame
import os
from car import *
from obstacle import *


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
        car = Car(550, 250)
        conus = Obstacle('conus2.png', 400, 450)
        conus2 = Obstacle('conus2.png', 850, 450)
        ppu = 1
        i = 0
        self.plus_nos = 0
        self.mod_on = False

        margines = pygame.sprite.Group()

        vertical = pygame.Surface((50, TRAINING_AREA_H))
        vertical.fill(pygame.Color('orange'))
        horizontal = pygame.Surface((TRAINING_AREA_W, 50))
        horizontal.fill(pygame.Color('orange'))
        left_marg = Margine(vertical, 0, 0)
        margines.add(left_marg)
        right_marg = Margine(vertical, TRAINING_AREA_W - 50, 0)
        margines.add(right_marg)
        verh_marg = Margine(horizontal, 0, 0)
        margines.add(verh_marg)
        verh_marg = Margine(horizontal, 0, TRAINING_AREA_H - 50)
        margines.add(verh_marg)


        area_distance = 50

        training_area = Area(area_distance, area_distance, TRAINING_AREA_W - area_distance * 2, TRAINING_AREA_H - area_distance * 2)
        lev_vert = pygame.Rect(50, 50, 5, 620)
        prav_vert = pygame.Rect(1230, 50, 5, 620)
        verh_gor = pygame.Rect(50, 50, 1180, 5)
        niz_gor = pygame.Rect(50, 670, 1185, 5)
        obstacles = pygame.sprite.Group()
        obstacles2 = list()
        obstacles.add(conus)
        obstacles.add(conus2)
        obstacles.add(margines)



        while not self.exit:
            dt = self.clock.get_time() / 1000


            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            for elem in obstacles: #обработка столкновений машинки с препятствиями
                self.col = pygame.Rect.colliderect(car.rect, elem)
                if self.col:
                    print('crash')
                    v = car.velocity
                    car.velocity = copysign(10, -v)
                    i=0
                    while pygame.Rect.colliderect(car.rect, elem):
                        i+=1
                        print('crash ', i)
                        car.update(0.001)

                    car.velocity = 0

            car.ctrl(pressed, dt)

            if pressed[pygame.K_MINUS]:
                print('включили невидимку')
                self.mod_on = True
                print(self.mod_on)

            if pressed[pygame.K_EQUALS]:
                print('выключили невидимку')
                self.mod_on = False
                print(self.mod_on)


            car.update(dt)
            conus.update()
            if car.rect.x > 0 and car.rect.y > 0:
                if car.velocity < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            else:
                car.velocity = 0
                car.position_x += 5
                car.position_y += 5
            if car.rect.x + car.rect.w < TRAINING_AREA_W and car.rect.y + car.rect.h < TRAINING_AREA_H:
                if car.velocity < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            else:
                car.velocity = 0
                car.position_x -= 5
                car.position_y -= 5
            '''if car.rect.x + 5 + car.rect.w // 2 >= TRAINING_AREA_W or car.rect.y + 5 >= TRAINING_AREA_H:
                car.position_x = 250
                car.position_y = 250
            '''
            # Drawing
            self.screen.fill((0, 0, 0))
            if self.mod_on:
                font = pygame.font.Font('13888.otf', 100)
                text = font.render('speed: {}'.format(round(car.velocity, 2)), True, pygame.Color('red'))
                self.screen.blit(text, (10, 10))
            pygame.draw.rect(self.screen, pygame.Color('red'), car.rect, 3)
            obstacles.draw(self.screen)
            self.screen.blit(car.image, (car.position_x - car.rect.w / 2, car.position_y - car.rect.h / 2))
            pygame.display.flip()
            i += 1
            if i == 0:
                self.plus_nos = car.rect[2] // 2


            self.clock.tick(self.ticks)
        pygame.quit()