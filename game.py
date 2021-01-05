import pygame
import os
from car import *
from obstacle import *
from map_edit import *


TRAINING_AREA_W = 1280
TRAINING_AREA_H = 720
#TRAINING_AREA = ((0, 0,), (TRAINING_AREA_W, TRAINING_AREA_H))

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
        self.show_car_and_velocity = True


    def run(self):
        car = Car(550, 250)
        conus = Obstacle('conus2.png', 400, 450)
        conus2 = Obstacle('stone.png', 850, 450)
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
        top_marg = Margine(horizontal, 0, 0)
        margines.add(top_marg)
        bott_marg = Margine(horizontal, 0, TRAINING_AREA_H - SEGMENT)
        margines.add(bott_marg)
        obstacles = pygame.sprite.Group()
        moveable_obstacles = pygame.sprite.Group()
        moveable_obstacles.add(conus)
        moveable_obstacles.add(conus2)
        obstacles.add(margines, moveable_obstacles)
        #moveable_obstacles.add(margines)

        map_edit = MapEdit((50, 50, TRAINING_AREA_W - 50, TRAINING_AREA_H - 50))
        map_edit.edit_ex(('conus2.png', 1310, 50), ('stone1.png', 1310, 150), ('arrow.png', 1500, 50))

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

            if pressed[pygame.K_MINUS]:
                self.show_car_and_velocity = True
            elif pressed[pygame.K_EQUALS]:
                self.show_car_and_velocity = False
            elif pressed[pygame.K_DELETE]:
                if map_edit.object_moving_mode:
                    map_edit.object_moving_mode = False
                    map_edit.moving_object.kill()

            car.ctrl(pressed, dt)


            car.update(dt)
            # Drawing
            self.screen.fill((0, 0, 0))

            # Перемещение объектов группы moveable_obstacles мышкой по площадке
            pos = ((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))





            if not self.show_car_and_velocity:
                map_edit.drag_copy(pos, moveable_obstacles)
                obstacles.add(moveable_obstacles)
            map_edit.drag(pos, moveable_obstacles)

            obstacles.draw(self.screen)
            print('game', len(moveable_obstacles), len(obstacles), len(map_edit.ex_obstacles))

            if self.show_car_and_velocity:
                text = self.font.render('speed {}'.format(round(car.velocity, 2)), True, pygame.Color('red'))
                self.screen.blit(text, (1285, 5))
                self.screen.blit(car.image, (car.position_x - car.rect.w / 2, car.position_y - car.rect.h / 2))
            else:
                map_edit.ex_obstacles.draw(self.screen)




            pygame.display.flip()
            self.clock.tick(self.ticks)
        pygame.quit()