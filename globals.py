import os

# ДИРЕКТОРИИ
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # текущая директория, в которой расположен исполняемый файл

# изображения
IMG_CARS_DIR = f'{CURRENT_DIR}\Images\Cars' # директория, в которой располагаются изображения автомобилей
IMG_OBSTACLES_DIR = f'{CURRENT_DIR}\Images\Obstacles' # директория, в которой располагаются изображения препятствий
# уровни
LEVELS_DIR = f'{CURRENT_DIR}\Levels' # директория, в которой располагаются файлы с уровнями
# базы данных
DATABASES_DIR = f'{CURRENT_DIR}\Databases' # директория, в которой располагаются базы данных
# звуки
SOUNDS_DIR = f'{CURRENT_DIR}\Sounds' # директория, в которой располагаются звуковые файлы


# РАЗМЕРЫ
TRAINING_AREA_W = 1280 # ширина холста
TRAINING_AREA_H = 720 # высота холста
SEGMENT = 50