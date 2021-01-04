import pygame
import os
from car import *
from obstacle import *


TRAINING_AREA_W = 1280
TRAINING_AREA_H = 720

SEGMENT = 50

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.screen = pygame.display.set_mode((TRAINING_AREA_W + 300, TRAINING_AREA_H))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.font = pygame.font.Font('13888.otf', 45)


    def run(self):
        car = Car(550, 250)
        conus = Obstacle('conus2.png', 400, 450)
        conus2 = Obstacle('conus2.png', 850, 450)
        ppu = 1
        i = 0

        margines = pygame.sprite.Group()
        vertical = pygame.Surface((SEGMENT, TRAINING_AREA_H))
        vertical.fill(pygame.Color('orange'))
        horizontal = pygame.Surface((TRAINING_AREA_W, SEGMENT))
        horizontal.fill(pygame.Color('orange'))
        left_marg = Margine(vertical, 0, 0)
        margines.add(left_marg)
        right_marg = Margine(vertical, TRAINING_AREA_W - SEGMENT, 0)
        margines.add(right_marg)
        verh_marg = Margine(horizontal, 0, 0)
        margines.add(verh_marg)

        niz_marg = Margine(horizontal, 0, TRAINING_AREA_H - SEGMENT)
        margines.add(niz_marg)
        obstacles = pygame.sprite.Group()
        moveable_obstacles = pygame.sprite.Group()
        moveable_obstacles.add(conus)
        moveable_obstacles.add(conus2)
        obstacles.add(margines, moveable_obstacles)
        moveable_obstacles.add(margines)

        elem_moving_mode = False


        while not self.exit:
            dt = self.clock.get_time() / 1000
            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            # User input
            pressed = pygame.key.get_pressed()
            for elem in obstacles: #обработка столкновений машинки с препятствиями
                self.col = pygame.sprite.collide_mask(car, elem)
                if self.col:
                    print('crash')
                    v = car.velocity
                    car.velocity = copysign(10, -v)
                    i=0
                    while pygame.sprite.collide_mask(car, elem):
                        i+=1
                        print('crash ', i)
                        car.update(0.001)

                    car.velocity = 0

            car.ctrl(pressed, dt)


            car.update(dt)
            # Drawing
            self.screen.fill((0, 0, 0))

            # Перемещение объектов группы moveable_obstacles мышкой по площадке
            pos = ((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            if not elem_moving_mode: # Сейчас у нас нет перемещаемого объект
                if pygame.mouse.get_pressed()[0]: # Выбираем перемещаемый объект нажатием левой кнопки мышки
                    for elem in moveable_obstacles:
                        if pos[0] > elem.rect.x and pos[0] < elem.rect.x + elem.rect.w and\
                                pos[1] > elem.rect.y and pos[1] < elem.rect.y + elem.rect.h:
                            elem_moving_mode = True
                            moving_elem = elem
                            print(f'взяли обьект {elem} с координатами {elem.rect.x}, {elem.rect.y}')
            else:      #  Сейчас у нас есть перемещаем объект moving_elem
                moving_elem.rect.x = pos[0]
                moving_elem.rect.y = pos[1]
                if pygame.mouse.get_pressed()[2]: # Ставим перемещаемый объект нажатием правой кнопки мышки
                    print(f'поставили обьект обьект {moving_elem} на координаты {pos}')
                    elem_moving_mode = False

            text = self.font.render('speed {}'.format(round(car.velocity, 2)), True, pygame.Color('red'))
            self.screen.blit(text, (1285, 5))
            obstacles.draw(self.screen)
            self.screen.blit(car.image, (car.position_x - car.rect.w / 2, car.position_y - car.rect.h / 2))
            pygame.display.flip()
            self.clock.tick(self.ticks)
        pygame.quit()