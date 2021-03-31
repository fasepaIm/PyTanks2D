#!/usr/bin/env python
# -*- coding: utf-8 -*-

# импортируем библиотеки
import pygame
import time as tm
from math import sqrt
from pygame import *
from os import path
from itertools import chain
from random import randint, choice
from threading import Timer
# импортируем наcтройки
from settings import *


# функция проверки столкновения объектов с игроком
def collide_with_player(self, xvel, yvel, walls, breakable_walls, breakable_houses, player, all_sprites):
    if sprite.collide_rect(self, player):  # если есть пересечение объекта с игроком
        MuzzleFlash(all_sprites, self.boom_flash, kill_flashes, self.rect.center, True)  # добавляем вспышку
        pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()  # включаем звук взрыва
        pygame.mixer.Sound(path.join(sounds_folder, ENEMY_HIT_SOUND)).play()  # звук урона по игроку
        self.kill()  # удаляем вражеский объект
        player.hit()  # вызываем функцию эффекта урона по игроку
        player.health -= ENEMY_DAMAGE  # уменьшаем здоровье игрока
        if self.xvel > 0:  # если движется вправо
            xvel = ENEMY_KICK
            player.rect.x += xvel
            collide_with_objects(player, xvel, 0, walls)
            collide_with_objects(player, xvel, 0, breakable_walls)
            collide_with_objects(player, xvel, 0, breakable_houses)

        elif self.xvel < 0:  # если движется влево
            xvel = -ENEMY_KICK
            player.rect.x += xvel
            collide_with_objects(player, xvel, 0, walls)  # проверяем на столкновение со стеной
            collide_with_objects(player, xvel, 0, breakable_walls)
            collide_with_objects(player, xvel, 0, breakable_houses)

        elif self.yvel > 0:  # если движется вниз
            yvel = ENEMY_KICK
            player.rect.y += yvel
            collide_with_objects(player, 0, yvel, walls)  # проверяем на столкновение со стеной
            collide_with_objects(player, 0, yvel, breakable_walls)
            collide_with_objects(player, 0, yvel, breakable_houses)

        elif self.yvel < 0:  # если движется вверх
            yvel = -ENEMY_KICK
            player.rect.y += yvel
            collide_with_objects(player, 0, yvel, walls)  # проверяем на столкновение со стеной
            collide_with_objects(player, 0, yvel, breakable_walls)
            collide_with_objects(player, 0, yvel, breakable_houses)


# функция проверки столкновения объектов со стеной
def collide_with_objects(self, xvel, yvel, objects, is_breakable_walls=False, is_bullet=False, is_houses=False):
    for p in objects:
        if sprite.collide_rect(self, p):  # если есть пересечение объекта со стеной
            if self.rect.center != p.rect.center:
                if xvel > 0:                       # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:                       # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:                       # если движется вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз

                if yvel < 0:                       # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
            if is_breakable_walls:
                MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, self.rect.center, True)  # добавляем взрыв
                pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()  # воспроизводим звук взрыва
                p.kill()
                if is_bullet:
                    if CURRENT_BULLET == BULLET_IMAGE:
                        self.kill()
                else:
                    self.kill()
            if is_houses:
                if p.house_life > 0:
                    p.house_life -= 1
                else:
                    MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, self.rect.center, True)  # добавляем взрыв
                    pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()  # воспроизводим звук взрыва
                    p.kill()
                if is_bullet:
                    if CURRENT_BULLET == BULLET_IMAGE:
                        self.kill()
                else:
                    MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, self.rect.center, True)  # добавляем взрыв
                    pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()  # воспроизводим звук взрыва
                    self.kill()


# класс игрока
class Player(sprite.Sprite):
    def __init__(self, x, y, boom_flash):
        sprite.Sprite.__init__(self)
        self.image = image.load(PLAYERS_TANK_IMAGE)  # загружаем изображение
        self.last_image_rotation = 0  # последнее значение поворота спрайта
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.pos = (x, y)
        self.health = PLAYER_HEALTH  # здоровье игрока
        self.score = 0  # счёт
        self.special_score = 0
        self.damaged = False
        self.xvel = 0
        self.yvel = 0
        self.ricardo_go = [True, False]
        self.boom_flash = boom_flash
        self.current_fuel = PLAYER_FUEL
        self.baff_works = False
        self.move_speed = MOVE_SPEED

    def update(self, left, right, up, down, all_sprites, enemies, walls, 
               breakable_walls, breakable_houses, repair_kits, speed_up_buffs,
               clear_map_buffs, power_bullet_buffs, fuel_buffs):
        global BULLET_X, BULLET_Y, CURRENT_BULLET, running
        if self.current_fuel <= 0:
            self.move_speed = 0
        self.pos = (self.rect.x, self.rect.y)
        self.image = pygame.transform.rotate(image.load(PLAYERS_TANK_IMAGE),
                                             self.last_image_rotation)  # обновлем изображение игрока
        if self.move_speed > 0:
            if up:  # если движемся вверх
                BULLET_X, BULLET_Y = 0, -1
                self.yvel = -self.move_speed  # меняем значение передвижения по y
                self.image = pygame.transform.rotate(image.load(PLAYERS_TANK_IMAGE), 90)  # поворачиваем спрайт игрока
                self.last_image_rotation = 90

            elif down:  # если движемся вниз
                BULLET_X, BULLET_Y = 0, 1
                self.yvel = self.move_speed  # меняем значение передвижения по y
                self.image = pygame.transform.rotate(image.load(PLAYERS_TANK_IMAGE), 270)  # поворачиваем спрайт игрока
                self.last_image_rotation = 270

            elif left:  # если движемся влево
                BULLET_X, BULLET_Y = -1, 0
                self.xvel = -self.move_speed  # меняем значение передвижения по x
                self.image = pygame.transform.rotate(image.load(PLAYERS_TANK_IMAGE), 180)  # поворачиваем спрайт игрока
                self.last_image_rotation = 180

            elif right:  # если движемся вправо
                BULLET_X, BULLET_Y = 1, 0
                self.xvel = self.move_speed  # меняем значение передвижения по x
                self.image = image.load(PLAYERS_TANK_IMAGE)
                self.last_image_rotation = 0

            if self.damaged:  # если нанесли урон
                try:
                    self.image.fill((255, 0, 0, next(self.damage_alpha)),
                                    special_flags=pygame.BLEND_RGBA_MULT)  # используем маску урона
                except:
                    self.damaged = False

            self.rect.y += self.yvel  # переносим свои положение на yvel
            collide_with_objects(self, 0, self.yvel, walls)  # проверяем на столкновение со стеной
            collide_with_objects(self, 0, self.yvel, breakable_walls)  # проверяем на столкновение с разрушаемой стеной
            collide_with_objects(self, 0, self.yvel, breakable_houses)  # проверяем на столкновение с домами
            self.rect.x += self.xvel  # переносим свои положение на xvel
            collide_with_objects(self, self.xvel, 0, walls)  # проверяем на столкновение со стеной
            collide_with_objects(self, self.xvel, 0, breakable_walls)  # проверяем на столкновение с разрушаемой стеной
            collide_with_objects(self, self.xvel, 0, breakable_houses)  # проверяем на столкновение с домам
            self.xvel = 0
            self.yvel = 0

        for p in repair_kits:
            if sprite.collide_rect(self, p):  # если есть пересечение игрока с ремкомлектом 
                if self.health < 100:  # если здоровье неполное
                    self.health += ENEMY_DAMAGE  # увеличиваем здоровье
                pygame.mixer.Sound(path.join(sounds_folder, BUFFS_SOUND)).play()  # выводим звук подбора баффа
                p.kill()  # уничтожаем ремкомплект

        for p in speed_up_buffs:
            if sprite.collide_rect(self, p):  # если есть пересечение игрока с баффом скорости
                self.baff_time = 10
                t = Timer(self.baff_time, self.speed_up_buff_stop)  # создаём таймер на 10 секунд
                t.start()  # включаем таймер
                self.baff_works = True
                self.baff_start_time = int(tm.time())
                self.move_speed += 2  # увеличиваем скорость
                pygame.mixer.Sound(path.join(sounds_folder, BUFFS_SOUND)).play()  # выводим звук подбора баффа
                p.kill()  # уничтожаем бафф скорости

        for p in power_bullet_buffs:
            if sprite.collide_rect(self, p):  # если есть пересечение игрока с баффом скорости
                self.baff_time = 15
                t = Timer(self.baff_time, self.power_bullet_buff_stop)  # создаём таймер на 10 секунд
                t.start()  # включаем таймер
                self.baff_works = True
                self.baff_start_time = int(tm.time())
                CURRENT_BULLET = POWER_BULLET_IMAGE  # меняем изображение снаяряда
                pygame.mixer.Sound(path.join(sounds_folder, BUFFS_SOUND)).play()  # выводим звук подбора баффа
                p.kill()  # уничтожаем бафф скорости

        for p in clear_map_buffs:
            if sprite.collide_rect(self, p):  # если есть пересечение игрока с баффом скорости
                pygame.mixer.Sound(path.join(sounds_folder, BUFFS_SOUND)).play()  # выводим звук подбора баффа
                for enemy in enemies:
                    self.score += POINT_PRICE
                    MuzzleFlash(all_sprites, self.boom_flash, kill_flashes, enemy.rect.center, True)  # добавляем вспышку
                    pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()  # включаем звук взрыва
                    enemy.kill()
                p.kill()  # уничтожаем бафф зачистки

        for p in fuel_buffs:
            if sprite.collide_rect(self, p):  # если есть пересечение игрока с баффом скорости
                pygame.mixer.Sound(path.join(sounds_folder, BUFFS_SOUND)).play()  # выводим звук подбора баффа
                self.current_fuel = PLAYER_FUEL
                p.kill()  # уничтожаем бафф топлива

        if self.baff_works:
            self.baff_time_left = self.baff_time - (int(tm.time()) - self.baff_start_time)


    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 3)

    # метод возвращающий скорость игрока в нормальное значение
    def speed_up_buff_stop(self):
        self.baff_works = False
        self.move_speed -= 2

    # метод возвращающий снаряд в нормальное состояние
    def power_bullet_buff_stop(self):
        global CURRENT_BULLET
        self.baff_works = False
        CURRENT_BULLET = BULLET_IMAGE


# класс врагов
class Enemy(sprite.Sprite):
    def __init__(self, all_sprites, player, enemies, coords):
        self.groups = all_sprites, enemies
        sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = image.load(ENEMY_TANK_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.rect.center = coords
        self.lamp = False

    def update(self, ENEMY_SPEED, walls, breakable_walls, breakable_houses, 
               bullets, all_sprites, boom_flash, player, enemies):
        self.all_sprites = all_sprites
        self.boom_flash = boom_flash
        self.xvel = 0
        self.yvel = 0
        distance = int(sqrt((player.rect.x - self.rect.x) ** 2 +
                            (player.rect.y - self.rect.y) ** 2))  # расстояние между врагом и игроком
        if distance < 200:
            self.lamp = True
        else:
            self.lamp = False

        if self.player.pos[0] > self.rect.x:  # если игрок правее чем враг
            self.xvel += ENEMY_SPEED          # то движемся вправо
            self.image = image.load(ENEMY_TANK_IMAGE)

        elif self.player.pos[0] < self.rect.x:  # если игрок левее чем враг
            self.xvel -= ENEMY_SPEED            # то движемся влево
            self.image = pygame.transform.rotate(image.load(ENEMY_TANK_IMAGE), 180)  # поворачиваем спрайт врага

        if self.player.pos[1] > self.rect.y:  # если игрок ниже чем враг
            self.yvel += ENEMY_SPEED          # то движемся вниз
            self.image = pygame.transform.rotate(image.load(ENEMY_TANK_IMAGE), 270)  # поворачиваем спрайт врага

        elif self.player.pos[1] < self.rect.y:  # если игрок выше чем враг
            self.yvel -= ENEMY_SPEED            # то движемся вверх
            self.image = pygame.transform.rotate(image.load(ENEMY_TANK_IMAGE), 90)  # поворачиваем спрайт врага

        self.collide_with_bullets(bullets)
        self.rect.y += self.yvel  # переносим положение врага на по y
        collide_with_player(self, 0, self.yvel, walls, breakable_walls, breakable_houses,
                            player, all_sprites)  # проверяем на столкновение с игроком
        collide_with_objects(self, 0, self.yvel, enemies)  # проверяем на столкновение с другими врагами
        collide_with_objects(self, 0, self.yvel, walls)  # проверяем на столкновение со стенами
        collide_with_objects(self, 0, self.yvel, breakable_walls, True)  # проверяем на столкновение с ломаемыми стенами
        collide_with_objects(self, 0, self.yvel, breakable_houses, False, False, True)  # проверяем на столкновение с домами
        self.rect.x += self.xvel  # переносим положение врага на по x
        collide_with_player(self, 0, self.yvel, walls, breakable_walls, breakable_houses,
                            player, all_sprites)  # проверяем на столкновение с игроком
        collide_with_objects(self, self.xvel, 0, enemies)  # проверяем на столкновение с другими врагами
        collide_with_objects(self, self.xvel, 0, walls)  # проверяем на столкновение со стенами
        collide_with_objects(self, self.xvel, 0, breakable_walls, True)  # проверяем на столкновение с ломаемыми стенами
        collide_with_objects(self, self.xvel, self.yvel, breakable_houses, False, False, True)  # проверяем на столкновение с домами

    # функция проверки столкновения со снарядами
    def collide_with_bullets(self, bullets):
        for p in bullets:
            if sprite.collide_rect(self, p):  # если есть пересечение снаряда с врагом
                MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, p.rect.center, True)  # добавляем взрыв
                self.player.score += POINT_PRICE  # увеличиваем счёт игрока
                if self.player.special_score == 300:
                    self.player.special_score = 0
                    self.player.ricardo_go[0] = True
                self.player.special_score += POINT_PRICE
                pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()  # выводим звук взрыва
                if CURRENT_BULLET == BULLET_IMAGE:
                    p.kill()  # уничтожаем снаряд
                self.kill()  # уничтожаем врага


# класс снарядов
class Bullet(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, walls, breakable_walls, breakable_houses, pos, player, boom_flash):
        global kill_flashes
        self.boom_flash = boom_flash
        self.all_sprites = all_sprites
        self.player = player
        self.groups = all_sprites, bullets
        self.walls = walls
        self.breakable_walls = breakable_walls
        self.breakable_houses = breakable_houses
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.bul_x = BULLET_X
        self.bul_y = BULLET_Y
        self.check_image()  # проверяем куда летит, дабы повернуть спрайт
        self.rect.center = pos
        self.pos = list(pos)
        self.vel = BULLET_SPEED

        xvel = -(KICKBACK * self.bul_x)  # значение отдачи по x
        player.rect.x += xvel  # переносим игрока по x
        collide_with_objects(player, xvel, 0, walls)  # проверям столкновение со стеной
        collide_with_objects(player, xvel, 0, breakable_walls)  # проверяем столкновение с ломаемой стеной
        collide_with_objects(player, xvel, 0, breakable_houses)  # проверяем на столкновение с домами
        yvel = -(KICKBACK * self.bul_y)  # значение отдачи по y
        player.rect.y += yvel  # переносим игрока по y
        collide_with_objects(player, 0, yvel, walls)  # проверям столкновение со стеной
        collide_with_objects(player, 0, yvel, breakable_walls)  # проверяем столкновение с ломаемой стеной
        collide_with_objects(player, 0, yvel, breakable_houses)  # проверяем на столкновение с домами
        self.spawn_time = pygame.time.get_ticks()  # время создания снаряда

    def check_image(self):
        if self.bul_x > 0:  # если летит вправо
            self.image = image.load(CURRENT_BULLET)
        elif self.bul_x < 0:  # если летит влево
            self.image = pygame.transform.rotate(image.load(CURRENT_BULLET), 180)  # поворачиваем спрайт снаряда
        elif self.bul_y < 0:  # если летит вверх
            self.image = pygame.transform.rotate(image.load(CURRENT_BULLET), 90)  # поворачиваем спрайт снаряда
        elif self.bul_y > 0:  # если летит вниз
            self.image = pygame.transform.rotate(image.load(CURRENT_BULLET), 270)  # поворачиваем спрайт снаряда
        self.rect = self.image.get_rect()

    def update(self):
        self.check_image()  # проверяем куда летит, дабы повернуть спрайт
        self.pos[0] += self.vel * self.bul_x  # значение сдвига по x
        self.pos[1] += self.vel * self.bul_y  # значение сдвига по y
        self.rect.center = self.pos  # перемещаем снаряд
        if sprite.spritecollideany(self, self.walls):  # если снаряд столкнулся со стеной
            MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, self.rect.center)  # добавляем взрыв
            pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()  # воспроизводим звук взрыва
            self.kill()                                                           # уничтожаем снаряд

        if sprite.spritecollideany(self, self.breakable_walls):  # если снаряд столкнулся со стеной
            MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, self.rect.center)  # добавляем взрыв
            pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()
        collide_with_objects(self, 0, 0, self.breakable_walls, True, True)  # проверяем столкновение с разрушаемой стеной

        if sprite.spritecollideany(self, self.breakable_houses):  # если снаряд столкнулся со стеной
            MuzzleFlash(self.all_sprites, self.boom_flash, kill_flashes, self.rect.center)  # добавляем взрыв
            pygame.mixer.Sound(path.join(sounds_folder, EXPLOSION_SOUND)).play()
        collide_with_objects(self, 0, 0, self.breakable_houses, False, True, True)  # проверяем столкновение с домами

        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:  # если время полёта снаряда превысило время жизни
            self.kill()                                                  # уничтожаем снаряд


# класс взрыва
class MuzzleFlash(pygame.sprite.Sprite):
    def __init__(self, all_sprites, muzzle_flash, gun_flashes, pos, kill=False):
        for img in BOOM_FLASHES:
            kill_flashes.append(pygame.image.load(path.join(images_folder, img)).convert_alpha())
        self._layer = EFFECTS_LAYER
        self.groups = all_sprites, muzzle_flash
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.killed = kill
        # размеры взрыва в зависимости от типа
        if kill:
            size = randint(60, 90)
        else:
            size = randint(20, 50)
        self.image = pygame.transform.scale(choice(gun_flashes), (size, size))  # изменяем размеры изображения облака
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.rect.x += 15 * BULLET_X  # косметический сдвиг спрайта
        self.rect.y += 15 * BULLET_Y  # косметический сдвиг спрайта
        self.spawn_time = pygame.time.get_ticks()  # время создания облака

    def update(self):
        if self.killed:  # если облако от убийства
            if pygame.time.get_ticks() - self.spawn_time > KILL_FLASH_DURATION:  # если превысило время жизни
                self.kill()  # уничтожаем облако
        else:
            if pygame.time.get_ticks() - self.spawn_time > FLASH_DURATION:  # если превысило время жизни
                self.kill()  # уничтожаем облако

class BreakableWall(sprite.Sprite):
    def __init__(self, all_sprites, breakable_wall, coords):
        self.groups = all_sprites, breakable_wall
        sprite.Sprite.__init__(self, self.groups)
        self.image = image.load(WALL_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords


class BreakableHouse(sprite.Sprite):
    def __init__(self, all_sprites, breakable_house, coords, name):
        self.groups = all_sprites, breakable_house
        sprite.Sprite.__init__(self, self.groups)
        self.image = image.load(eval(f'HOUSE_{name[-3:]}_IMAGE'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.house_life = HOUSE_LIFE


class RepairKit(sprite.Sprite):
    def __init__(self, all_sprites, repair_kits, coords):
        self.groups = all_sprites, repair_kits
        sprite.Sprite.__init__(self, self.groups)
        self.image = image.load(REPAIR_KIT_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = coords


class SpeedUpBuff(sprite.Sprite):
    def __init__(self, all_sprites, speed_up_buffs, coords):
        self.groups = all_sprites, speed_up_buffs
        sprite.Sprite.__init__(self, self.groups)
        self.image = image.load(SPEED_UP_BUFF_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = coords


class ClearMapBuff(sprite.Sprite):
    def __init__(self, all_sprites, speed_up_buffs, coords):
        self.groups = all_sprites, speed_up_buffs
        sprite.Sprite.__init__(self, self.groups)
        self.image = image.load(CLEAR_MAP_BUFF_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = coords


class PowerBulletBuff(sprite.Sprite):
    def __init__(self, all_sprites, power_bullet_buffs, coords):
        self.groups = all_sprites, power_bullet_buffs
        sprite.Sprite.__init__(self, self.groups)
        self.image = image.load(POWER_BULLET_BUFF_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = coords


class FuelBuff(sprite.Sprite):
    def __init__(self, all_sprites, fuel_buffs, coords):
        self.groups = all_sprites, fuel_buffs
        sprite.Sprite.__init__(self, self.groups)
        self.image = image.load(FUEL_BUFF_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = coords
