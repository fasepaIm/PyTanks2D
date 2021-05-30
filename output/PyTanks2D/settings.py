# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеки
from os import path

# Объявляем переменные цветов
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (20, 20, 20)

# пути к папкам игры
game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')
music_folder = path.join(game_folder, 'assets/music')
sounds_folder = path.join(game_folder, 'assets/sounds')
images_folder = path.join(game_folder, 'assets/images')
videos_folder = path.join(game_folder, 'assets/videos')
fonts_folder = path.join(game_folder, 'assets/fonts')
database_folder = path.join(game_folder, 'assets/records_db')

# основные параметры игры
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
ICON = 'icon.ico'  # изображение иконки игры
TOTAL_LEVEL_WIDTH = 0  # полная ширина уровня
TOTAL_LEVEL_HEIGHT = 0  # полная высота уровня
FPS = 60  # количество кадров в секунду
NAME = 'Player'  # имя игрока по умолчанию
ENEMIES_SPAWN_COORDINATES = []  # координаты возрождения врагов
BUFF_SPAWN_COORDINATES = []  # координаты спавна баффов
FUEL_SPAWN_COORDINATES = []  # координаты спавна топлива
NIGHT = False  # ночь
SELECTED_MODE = 'mode: NORMAL'  # выбранный режим игры
BACKGROUND_MUSIC = 'third.ogg'  # фоновая музыка
MUSIC_VOLUME = 0.05  # громкось музыки

# параметры ночного режима
NIGHT_COLOR = (0, 0, 0)  # ночная заливка
LIGHT_RADIUS = (500, 500)  # радиус света
LIGHT_MASK = "light_350_med.png"  # маска света
LAMP_IMAGE = path.join(images_folder, 'lamp.png')  # лампа индикации врагов
FUEL_LAMP_IMAGE = path.join(images_folder, 'fuel_lamp.png')  # лампа индикации уровня топлива

# дополнительно
WALL_IMAGE = path.join(images_folder, 'wall.png')  # изображение стены
# изображения домов
HOUSE_1_1_IMAGE = path.join(images_folder, 'house_1_1.png')
HOUSE_2_1_IMAGE = path.join(images_folder, 'house_2_1.png')
HOUSE_2_2_IMAGE = path.join(images_folder, 'house_2_2.png')
HOUSE_3_1_IMAGE = path.join(images_folder, 'house_3_1.png')
HOUSE_3_2_IMAGE = path.join(images_folder, 'house_3_2.png')
HOUSE_3_3_IMAGE = path.join(images_folder, 'house_3_3.png')
HOUSE_4_1_IMAGE = path.join(images_folder, 'house_4_1.png')
HOUSE_4_2_IMAGE = path.join(images_folder, 'house_4_2.png')
HOUSE_5_1_IMAGE = path.join(images_folder, 'house_5_1.png')
HOUSE_5_2_IMAGE = path.join(images_folder, 'house_5_2.png')
HOUSE_5_3_IMAGE = path.join(images_folder, 'house_5_3.png')
HOUSE_5_4_IMAGE = path.join(images_folder, 'house_5_4.png')
# Свойства домов
HOUSE_LIFE = 3

# баффы
REPAIR_KIT_IMAGE = path.join(images_folder, 'repair_kit.png')  # изображение ремкомплекта
SPEED_UP_BUFF_IMAGE = path.join(images_folder, 'speed_up.png')  # изображение баффа скорости
CLEAR_MAP_BUFF_IMAGE = path.join(images_folder, 'clear_map.png')  # изображение баффа зачистки карты
POWER_BULLET_BUFF_IMAGE = path.join(images_folder, 'power_bullet.png')  # изображение баффа пробивающего снаряда
FUEL_BUFF_IMAGE = path.join(images_folder, 'fuel.png')  # изображение баффа пробивающего снаряда
BUFFS_SOUND = 'buff.wav'

# параметры игрока
MOVE_SPEED = 1  # скорость игрока
PLAYER_HEALTH = 100  # здоровье игрока
ENEMIES_KILLED = 0  # убито врагов
POINT_PRICE = 10  # цена очка
AMMUNITION = 5  # боезапас
PLAYER_FUEL = 100  # запас топлива
FUEL_CONSUMPTION = 2  # расход топлива
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]  # эффект урона
PLAYERS_TANK_IMAGE = path.join(images_folder, 'players_tank.png')  # изобрадение игрока
PLAYER_SHOT_SOUND = 'player_shot.wav'  # звук выстрела
PLAYER_RIDE_SOUND = 'player_ride.wav'  # звук передвижения
LEVEL_START_SOUND = 'level_start.wav'  # звук начала уровня

# параметры врагов
ENEMY_SPEED = 2  # скорость врагов
ENEMY_KICK = 15  # отдача врагов
ENEMY_DAMAGE = 20  # урон врагов
ENEMY_TANK_IMAGE = path.join(images_folder, 'enemies_tank.png')  # изображение врагов
ENEMY_HIT_SOUND = 'enemy_hit.wav'  # звук ударв врагов

# параметры снарядов
BULLET_SPEED = 6  # скорость снаряда
BULLET_LIFETIME = 1000  # время жизни снаряда
BULLET_X, BULLET_Y = 1, 0  # направление полёта
KICKBACK = 3  # отдача от выстрела
BULLET_IMAGE = path.join(images_folder, 'bullet.png')  # изображение снаряда
POWER_BULLET_IMAGE = path.join(images_folder, 'bullet_x.png')  # изображение бронебойного снаряда
CURRENT_BULLET = BULLET_IMAGE  # текущий снаряд

# эффекты
# изображения облаков стрельбы
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png',
                  'whitePuff17.png', 'whitePuff18.png']

# изображения взрывов
BOOM_FLASHES = ['boom_flashes_1.png', 'boom_flashes_2.png',
                'boom_flashes_3.png', 'boom_flashes_4.png']
EXPLOSION_SOUND = 'explosion.wav'  # звук взрыва
FLASH_DURATION = 40  # длительность облака выстрела
KILL_FLASH_DURATION = 150  # длительность взрыва
EFFECTS_LAYER = 4
kill_flashes = []

# изображения для обучения
TUTORIAL_IMAGES = ['tutorial_1.jpg', 'tutorial_2.jpg', 'tutorial_3.jpg',
                   'tutorial_4.jpg', 'tutorial_5.jpg']

# просто Рикардо
RICARDO_IMAGE = path.join(images_folder, 'ricardo.png')
RICARDO_SOUND = 'ricardo.wav'
