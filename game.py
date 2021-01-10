import pygame
import os
import sqlite3
from car import *
from obstacle import *
from map_edit import *
import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QDialog

TRAINING_AREA_W = 1280
TRAINING_AREA_H = 720
#TRAINING_AREA = ((0, 0,), (TRAINING_AREA_W, TRAINING_AREA_H))

SEGMENT = 50


class MyWidget(QDialog):
    def __init__(self, game):
        super().__init__()
        uic.loadUi('name.ui', self)
        self.game = game
        self.pushButton.clicked.connect(self.run)


    def run(self):
        name = self.lineEdit.text()
        self.game.user_name = name
        self.label.setText(f'Приятной игры, {name}!')
        self.lineEdit.setReadOnly(True)
        self.pushButton.setEnabled(False)
        self.game.run()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.screen = pygame.display.set_mode((TRAINING_AREA_W + 300, TRAINING_AREA_H))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.font = pygame.font.Font('13888.otf', 50)
        self.small_font = pygame.font.Font('13888.otf', 30)
        self.show_car_and_velocity = True
        self.notification_mode = False
        self.notification_message = 'тут ваше уведомление'
        self.second_notification_message = 'чтобы продолжить нажмите Enter'
        self.special_notification_message = ''
        self.died = False
        self.new_game_circle = False
        self.user_name = ''
        #self.finish_point = pygame.Rect(695, 125, 12, 12)

    def clear_groups(self, *groups):
        for group in groups:
            for obj in group:
                obj.kill()

    def run(self):
        car = Car(550, 250)
        #conus = Obstacle('conus2.png', 400, 450, 0)
        #conus2 = Obstacle('conus2.png', 850, 450, 180)
        #start_zone = Obstacle('start_rect_2.png', 100, 100, 0)
        #finish_zone = Obstacle('finish_rect_2.png', 900, 100, 0)
        ppu = 1
        i = 0
        r = False

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


        finish_point = Obstacle('finish_point.png', 80, 80, 0)
        start_point = Obstacle('start_rect_2.png', 300, 100, 0)

        start_finish_points = pygame.sprite.Group(start_point, finish_point)

        obstacles = pygame.sprite.Group()
        moveable_obstacles = pygame.sprite.Group()
        moveable_obstacles.add(finish_point)
        #moveable_obstacles.add(conus)
        #moveable_obstacles.add(conus2)
        #moveable_obstacles.add(start_zone, finish_zone)
        obstacles.add(margines)#, moveable_obstacles)
        background_obstacles = pygame.sprite.Group()
        #moveable_obstacles.add(margines)
        editable_objects = pygame.sprite.Group()
        editable_objects.add(start_finish_points)

        map_edit = MapEdit((50, 50, TRAINING_AREA_W - 50, TRAINING_AREA_H - 50))
        map_edit.edit_ex(('conus2.png', 1310, 50, 0), ('stone1.png', 1310, 150, 0), ('arrow.png', 1500, 50, 0))
        rot = False

        now_lvl = 1
        ticks = 0
        self.died = False
        level_loaded = False

        while not self.exit:
            ticks += 1
            dt = self.clock.get_time() / 1000
            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                if event.type == pygame.KEYDOWN:
                    down = True
                if event.type == pygame.KEYUP:
                    up = False
                    rot = False

            if not level_loaded:
                name = f'{now_lvl}lvl.csv'
                self.died = False
                print(name)
                loaded_obstacles, start_point, finish_point = map_edit.load_level(car, name)
                car.health = 100
                level_loaded = True

                car.position_x = start_point.rect.x + 5
                car.position_y = start_point.rect.y + 35

                for elem in editable_objects:
                    elem.kill()
                start_finish_points.add(start_point, finish_point)
                editable_objects.add(loaded_obstacles, start_point, finish_point)

                moveable_obstacles.add(loaded_obstacles)
                #                editable_objects = moveable_obstacles
                obstacles.add(loaded_obstacles)




            #  User input
            pressed = pygame.key.get_pressed()
            # Проверим, не достигли ли мы финиша
            if car.health > 0:
                if not self.notification_mode and (pygame.sprite.collide_mask(car, finish_point)):
                    con = sqlite3.connect('levels.sqlite')
                    cur = con.cursor()
                    max_id = cur.execute(f"""select id from levels""").fetchall()[-1][0]
                    car.velocity = 0
                    level_loaded = False
                    print(now_lvl)
                    max_res = cur.execute(f"""select record from levels where id = {now_lvl}""").fetchone()[0]
                    owner = cur.execute(f"""select record_owner from levels where id = {now_lvl}""").fetchone()[0]
                    print('max', max_res)
                    if car.health > max_res:
                        print(1121212)
                        cur.execute(f"""update levels set record={car.health} where id={now_lvl}""")
                        cur.execute(f"""update levels set record_owner='{self.user_name}' where id={now_lvl}""")
                    con.commit()
                    con.close()
                    if max_id > now_lvl:
                        self.notification(f'вы успешно прошли {now_lvl} lvl', 'чтобы продолжить нажмите Enter',
                                          f'вы набрали {car.health} очков, рекорд {max_res}({owner})')
                    else:
                        self.notification('вы прошли все уровни. хотите пройти заново?', 'для подтверждения нажмите enter', f'вы набрали {car.health} очков, рекорд {max_res}({owner})')
                        now_lvl = 1
                        self.new_game_circle = True


                for elem in obstacles: #обработка столкновений машинки с препятствиями
                    self.col = pygame.sprite.collide_mask(car, elem)
                    if self.col:
                        print('crash')
                        v = car.velocity
                        car.velocity = copysign(10, -v)
                        i=0
                        while pygame.sprite.collide_mask(car, elem):
                            i+=1
                            if i == 3:
                                car.health -= 25
                            print('crash ', i)
                            car.update(0.001)

                        car.velocity = 0

                if pressed[pygame.K_MINUS]:
                    self.show_car_and_velocity = True
                elif pressed[pygame.K_EQUALS]:
                    self.show_car_and_velocity = False
                elif pressed[pygame.K_s]:
                    editable_objects.add(moveable_obstacles, start_finish_points)
                    map_edit.save_level(editable_objects)
                elif pressed[pygame.K_f]:
                    print(ticks)
                    if car.rect.colliderect(self.finish_point) == 1:
                        self.notification()
                elif pressed[pygame.K_l]:
                    loaded_obstacles, start_point, finish_point = map_edit.load_level(car)
                    print(start_point.rect.x, start_point.rect.y)

                    car.position_x = start_point.rect.x + 5
                    car.position_y = start_point.rect.y + 35
                    for elem in editable_objects:
                        elem.kill()
                    start_finish_points.add(start_point, finish_point)
                    editable_objects.add(loaded_obstacles, start_point, finish_point)

                    moveable_obstacles.add(loaded_obstacles)
        #                editable_objects = moveable_obstacles
                    obstacles.add(loaded_obstacles)
                elif pressed[pygame.K_n]:
                    self.notification()
                elif pressed[pygame.K_DELETE]:
                    if map_edit.object_moving_mode:
                        map_edit.object_moving_mode = False
                        map_edit.moving_object.kill()
                elif pressed[pygame.K_INSERT]:

                    if map_edit.object_moving_mode and rot == False:
                        print('rotate')
                        map_edit.moving_object.rotate(45)
                        rot = True
                elif pressed[pygame.K_c]:
                    car.change_car()
                    # else:
                    # r=Fals
            else:
                self.died = True
                self.notification('вы не смогли пройти уровень', 'чтобы повторить попытку нажмите enter')
                car.health += 10

            if pressed[pygame.K_RETURN]:
                if self.notification_mode:
                    self.notification_off()
                    if not self.died:
                        print('закончили уровень')
                        con = sqlite3.connect('levels.sqlite')
                        cur = con.cursor()
                        #max_res = cur.execute(f"""select id from levels""").fetchall()[-1][0]
                        name = cur.execute(f"""select file from levels where id = {now_lvl}""").fetchone()[0]
                        if not self.new_game_circle:
                            now_lvl += 1
                        else:
                            self.new_game_circle = False
                        con.commit()
                        con.close()
                        print(False)
                    else:
                        name = f'{now_lvl}lvl.csv'
                        self.died = False
                        print(True)

                    level_loaded = False



            car.ctrl(pressed, dt)


            car.update(dt)
            # Drawing
            self.screen.fill((0, 0, 0))

            # Перемещение объектов группы moveable_obstacles мышкой по площадке
            pos = ((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

            if not self.show_car_and_velocity:# or not self.notification_mode:
                map_edit.drag_copy(pos, moveable_obstacles)
                obstacles.add(moveable_obstacles)
            if not self.notification_mode:
                map_edit.drag(pos, editable_objects)#moveable_obstacles
                moveable_obstacles.draw(self.screen)
                start_finish_points.draw(self.screen)
                obstacles.draw(self.screen)
            # print('game', len(moveable_obstacles), len(obstacles), len(map_edit.ex_obstacles))

            if self.show_car_and_velocity:
                # если режим добавления обьектов не включён:
                if not self.notification_mode:
                    # если режим показа уведомления не включён, то отображаем машинку, скорость и здоровье.
                    text = self.font.render('{} lvl'.format(now_lvl), True, pygame.Color('red'))
                    self.screen.blit(text, (1285, 5))
                    text = self.font.render('speed {}'.format(round(car.velocity, 2)), True, pygame.Color('red'))
                    self.screen.blit(text, (1285, 55))
                    text = self.font.render('health {}'.format(car.health), True, pygame.Color('red'))
                    self.screen.blit(text, (1285, 105))
                    self.screen.blit(car.image, (car.position_x - car.rect.w / 2, car.position_y - car.rect.h / 2))
                else:
                    # если режим показа уведомления включён, то показываем уведомление.
                    text = self.small_font.render(self.special_notification_message, True, pygame.Color('green'))
                    self.screen.blit(text, (100, 240))
                    text = self.font.render(self.notification_message, True, pygame.Color('red'))
                    self.screen.blit(text, (100, 300))
                    text = self.small_font.render(self.second_notification_message, True, pygame.Color('red'))
                    self.screen.blit(text, (560, 360))
            else:
                # если режим добавления обьектов включён:
                if not self.notification_mode:
                    # если режим показа уведомления выключён, то отображаем палитру препятствий.
                    map_edit.ex_obstacles.draw(self.screen)

            #pygame.draw.rect(self.screen, pygame.Color('red'), car.rect, 3)
            #pygame.draw.rect(self.screen, pygame.Color('purple'), self.finish_point, 10)

            pygame.display.flip()
            self.clock.tick(self.ticks)
        pygame.quit()

    def notification(self, message='вы успешно прошли уровень', second_message='чтобы продолжить нажмите Enter', special_message=''):
        if not self.notification_mode:
            self.notification_mode = True
            self.notification_message = message
            self.second_notification_message = second_message
            self.special_notification_message = special_message


    def notification_off(self):
        if self.notification_mode:
            self.notification_mode = False