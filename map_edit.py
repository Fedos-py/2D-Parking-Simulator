import pygame
from obstacle import *
from game import *
from file_operations import *
import csv
import os
from tkinter.filedialog import askopenfilename
from tkinter import *

class MapEdit:
    def __init__(self, area):
        self.object_moving_mode = False
        self.moving_object = None
        self.area = area

    def take(self, pos, from_group):
        if not self.object_moving_mode:  # Сейчас у нас нет перемещаемого объекта
            if pygame.mouse.get_pressed()[0]:  # Выбираем перемещаемый объект нажатием левой кнопки мышки
                for object in from_group:
                    if pygame.Rect.collidepoint(object.rect, pos):
                        # мышка на объекте
                        self.object_moving_mode = True
                        self.moving_object = object
                        #print(f'взяли обьект {object.name} с координатами {object.rect.x}, {object.rect.y}')
                        return self.moving_object

    def put(self, pos):
        if self.object_moving_mode:
            # Сейчас у нас есть перемещаемй объект self.moving_object
            if pos[0] < self.area[0]:
                self.moving_object.rect.x = self.area[0]
            elif pos[0] > self.area[2] - self.moving_object.rect.w:
                self.moving_object.rect.x = self.area[2] - self.moving_object.rect.w
            else:
                self.moving_object.rect.x = pos[0]

            if pos[1] < self.area[1]:
                self.moving_object.rect.y = self.area[1]
            elif pos[1] > self.area[3] - self.moving_object.rect.h:
                self.moving_object.rect.y = self.area[3] - self.moving_object.rect.h
            else:
                self.moving_object.rect.y = pos[1]

            if pygame.mouse.get_pressed()[2]:
                # Ставим перемещаемый объект нажатием правой кнопки мышки
                #print(f'поставили обьект обьект {self.moving_object.name} на координаты {pos}')
                self.object_moving_mode = False

    def drag(self, pos, objects_group):
        self.take(pos, objects_group)
        self.put(pos)

    def drag_copy(self, pos, to_group):
        obj = self.take(pos, self.ex_obstacles)
        if obj:
            self.moving_object = Obstacle(obj.name, pos[0], pos[1], 0)
            to_group.add(self.moving_object )
        self.put(pos)


    def save_level(self, obstacles):
        print('сохраняем уровень')
        print(obstacles)
        info = list()
        for elem in obstacles:
            info.append([elem.name, elem.rect.x, elem.rect.y, elem.angle])
        print(info)
        current_dir = filesave(title="Please select a file", initialdir=f'{os.path.dirname(os.path.abspath(__file__))}/Levels' ,
                                  filetypes=[('Game levels', '*.csv'), ('All files', '*.*')])
        #filename = input("введите название файла для записи ")
        #print(f'записываем в файл {filename} значения {info}')
        #current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(current_dir, 'w') as csvfile:
            fieldnames = ['filename', 'position_x', 'position_y', 'angle', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            for elem in info:
                print(elem[0])
                if elem[0] != 'start_rect_2.png' and elem[0] != 'finish_rect_2.png':
                    etype = 'simple'
                elif elem[0] == 'start_rect_2.png':
                    etype = 'start'
                elif elem[0] == 'finish_rect_2.png':
                    etype = 'finish'
                writer.writerow({'filename': elem[0], 'position_x': elem[1], 'position_y': elem[2], 'angle': elem[3], 'type': etype})



    def load_level(self, car, needed_lvl=None):
        print('загружаем уровень')
        #filename = input('введите название файла с загружаемым уровнем ')
        if needed_lvl == None:
            current_dir = fileopen(title="Please select a file",
                                   initialdir=f'{os.path.dirname(os.path.abspath(__file__))}/Levels',
                                   filetypes=[('Game levels', '*.csv'), ('All files', '*.*')])
        else:
            current_dir = f'{os.path.dirname(os.path.abspath(__file__))}/Levels/{needed_lvl}'
        #current_dir = os.path.dirname(os.path.abspath(__file__))
        print(current_dir)
        obstacles = pygame.sprite.Group()
        start_stop_obstacles = pygame.sprite.Group()
        #with open(f'{current_dir}/Levels/{filename}.csv', "r") as File:
        with open(current_dir, "r") as File:
            reader = csv.reader(File)
            for row in reader:
                if row != [] and row != ['', '', '', '', ''] and row != "['', '', '', '', '']":
                    row = row[0].split(';')
                    print(row)
                    if row[4] == 'start':
                        print(int(row[1]))
                        car.position_x = int(row[1]) + 5
                        print(int(row[2]))
                        car.position_y = int(row[2]) + 35
                        start_stop_obstacles.add(Obstacle(row[0], int(row[1]), int(row[2]), int(row[3])))
                    else:
                        obstacles.add(Obstacle(row[0], int(row[1]), int(row[2]), int(row[3])))
        return obstacles, start_stop_obstacles

    def add_ex(self):
        pass

    def edit_ex(self, *objects):
        self.ex_obstacles = pygame.sprite.Group()
        for obj in objects:
            o=Obstacle(obj[0], obj[1], obj[2], obj[3])
            self.ex_obstacles.add(o)

'''    def fileopen(self, **kwargs):
        root = Tk()
        root.withdraw()  # hide the window
        file = askopenfilename(**kwargs)
        root.destroy()
        return file'''