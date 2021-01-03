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
        car = Car(250, 250)
        conus = Obstacle('conus2.png', 400, 250)
        ppu = 1
        i = 0
        self.plus_nos = 0
        self.mod_on = False

        area_distance = 50
        '''surf = pygame.Surface((TRAINING_AREA_W, TRAINING_AREA_H))
        pygame.draw.rect(surf, pygame.Color('pink'), (area_distance, area_distance, area[0], area[1]), 3)
        surf.set_colorkey(pygame.Color('black'))
        area_mask = pygame.mask.from_surface(surf)
        '''
        training_area = Area(area_distance, area_distance, TRAINING_AREA_W - area_distance * 2, TRAINING_AREA_H - area_distance * 2)
        obstacles = pygame.sprite.Group()
        obstacles.add(conus)
        #obstacles.add(area_mask)



        while not self.exit:
            dt = self.clock.get_time() / 1000
            #gr = car_image.get_rect()
            #rect = pygame.Rect(car.position_x - gr.w // 2, car.position_y - gr.h // 2, gr.w, gr[3])
            #print(rect)
            #car_pos = (car.position_x * ppu - rect[2] / 2, car.position_y * ppu - rect[3] / 2)


            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            self.col = pygame.Rect.colliderect(car.rect, conus.rect)
            print(self.col, car.rect, conus.rect)
            if self.col == 1:
                print('crash')
                car.velocity = 0
                car.position_x -= 5
                car.position_y -= 5

            #print(pygame.sprite.collide_mask(car, conus))
            '''
            for elem in obstacles:
                print(pygame.sprite.collide_mask(car, elem))
            offset = (int(conus.pos[1] - car.position_y), int(conus.pos[0] - car.position_x))
            if car.mask.overlap_area(conus.mask, offset) > 0:
                car.velocity = 0
                car.position_x -= 5
                car.position_y -= 5
                print('crash')
            '''




            if pressed[pygame.K_UP]:
                #print(rect)
                if car.rect.x > 0 and car.rect.y > 0:
                    if car.velocity < 0:
                        car.acceleration = car.brake_deceleration
                    else:
                        car.acceleration += 1 * dt
                else:
                    car.velocity =  0
                    car.position_x += 5
                    car.position_y += 5
                if car.rect.x + car.rect.w < TRAINING_AREA_W and car.rect.y + car.rect.h < TRAINING_AREA_H:
                    if car.velocity < 0:
                        car.acceleration = car.brake_deceleration
                    else:
                        car.acceleration += 1 * dt
                else:
                    car.velocity =  0
                    car.position_x -= 5
                    car.position_y -= 5
            elif pressed[pygame.K_DOWN]:
                #print(rect)
                if car.rect.x > 0 and car.rect.y > 0:
                    if car.velocity < 0:
                        car.acceleration = -car.brake_deceleration
                    else:
                        car.acceleration -= 1 * dt
                else:
                    car.velocity = 0
                    car.position_x += 5
                    car.position_y += 5
                if car.rect.x + car.rect.w < TRAINING_AREA_W and car.rect.y + car.rect.h < TRAINING_AREA_H:
                    if car.velocity < 0:
                        car.acceleration = -car.brake_deceleration
                    else:
                        car.acceleration -= 1 * dt
                else:
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
            conus.update()

            #print(rect)
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
            #print(rect.x)
            if car.rect.x + 5 + car.rect.w // 2 >= TRAINING_AREA_W or car.rect.y + 5 >= TRAINING_AREA_H:
                car.position_x = 250
                car.position_y = 250
            # Drawing
            self.screen.fill((0, 0, 0))
            if self.mod_on:
                font = pygame.font.Font('13888.otf', 100)
                text = font.render('speed: {}'.format(round(car.velocity, 2)), True, pygame.Color('red'))
                self.screen.blit(text, (10, 10))
            pygame.draw.rect(self.screen, pygame.Color('red'), car.rect, 3)
            pygame.draw.rect(self.screen, pygame.Color('pink'), (50, 50, 1180, 620), 5)
            #pygame.draw.rect(self.screen, pygame.Color('pink'), area, 5)
            #print(car.position_x, car.position_y)
#            self.screen.blit(training_area, (0, 0))
#            self.screen.blit(conus_image, conus_pos)
#            all_sprites.draw(screen)
            obstacles.draw(self.screen)
            self.screen.blit(car.image, (car.position_x - car.rect.w / 2, car.position_y - car.rect.h / 2))
            #pygame.draw.rect(self.screen, pygame.Color('white'), (15, 15, 100, 100), 20)
            pygame.draw.rect(self.screen, pygame.Color('white'), conus.rect, 4)
            pygame.display.flip()
            #print(i)
            i += 1
            if i == 0:
                self.plus_nos = car.rect[2] // 2


            self.clock.tick(self.ticks)
        pygame.quit()