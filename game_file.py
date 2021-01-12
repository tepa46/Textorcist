import pygame
import sys
import os
import time

import game_fight
import challenge_window

SIZE = [660, 660]
MAP_SIZE = [11, 11]


def read_map(level, view):
    with open(f'data/levels/{level}/maps/{view}_map.txt', 'r', encoding='utf8') as f:
        map_file = f.read().split('\n')
        for i in range(len(map_file)):
            while len(map_file[i].replace('  ', ' ')) != len(map_file[i]):
                map_file[i] = map_file[i].replace('  ', ' ')
        return [mini_pic for mini_pic in [pic.split(' ') for pic in map_file]]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', f'{name}.png')
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_sprites(group, map, koor, dir, cell_size, colorkey=None):
    for i in range(-5, 6, 1):
        for j in range(-5, 6, 1):
            sprite = pygame.sprite.Sprite(group)
            sprite.image = pygame.transform.scale(
                load_image(f'{dir}/{map[koor[0] + i][koor[1] + j]}', colorkey), (60, 60))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = (j + 5) * cell_size
            sprite.rect.y = (i + 5) * cell_size


def get_player_koor(level):
    with open(f'data/levels/{level}/player_koor.txt', 'r', encoding='utf8') as f:
        koor_file = f.read().split(' ')
        return [int(pic) for pic in koor_file]


def get_chest_num(level, chest_num):
    with open(f'data/levels/{level}/chest_number.txt', 'r', encoding='utf8') as input_file:
        numbers = input_file.read().split('\n')
    return numbers[int(chest_num)]


def is_possible_to_move(material):
    if material != 'empty' and material[:4] != 'wall':
        return True
    return False


class Board:
    def __init__(self, width, height, level, materials_map, heroes_map, chest_map):
        self.width = width
        self.height = height
        self.cell_size = 60
        self.materials_map = materials_map
        self.heroes_map = heroes_map
        self.chest_map = chest_map
        self.level = level

    def render(self, screen, koor):
        all_sprites = pygame.sprite.Group()
        load_sprites(all_sprites, self.materials_map, koor, 'materials', self.cell_size)
        load_sprites(all_sprites, self.heroes_map, koor, 'heroes', self.cell_size, -1)

        sprite = pygame.sprite.Sprite(all_sprites)
        sprite.image = pygame.transform.scale(load_image('heroes/hero'), (60, 60))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 5 * self.cell_size
        sprite.rect.y = 5 * self.cell_size
        all_sprites.draw(screen)


class Player(Board):
    def __init__(self, screen, width, height, level, materials_map, heroes_map, chest_map, player_koor):
        super().__init__(width, height, level, materials_map, heroes_map, chest_map)
        self.screen = screen
        self.player_koor = player_koor
        self.past_player_koor = player_koor

    def new_koor(self, command):
        if command == pygame.K_UP:
            if is_possible_to_move(self.materials_map[self.player_koor[0] - 1][self.player_koor[1]]):
                self.past_player_koor = self.player_koor.copy()
                self.player_koor[0] -= 1
        elif command == pygame.K_DOWN:
            if is_possible_to_move(self.materials_map[self.player_koor[0] + 1][self.player_koor[1]]):
                self.past_player_koor = self.player_koor.copy()
                self.player_koor[0] += 1
        elif command == pygame.K_LEFT:
            if is_possible_to_move(self.materials_map[self.player_koor[0]][self.player_koor[1] - 1]):
                self.past_player_koor = self.player_koor.copy()
                self.player_koor[1] -= 1
        elif command == pygame.K_RIGHT:
            if is_possible_to_move(self.materials_map[self.player_koor[0]][self.player_koor[1] + 1]):
                self.past_player_koor = self.player_koor.copy()
                self.player_koor[1] += 1

    def heroes_processing(self):
        if self.heroes_map[self.player_koor[0]][self.player_koor[1]].split('_')[0] == 'bad':
            fight = game_fight.Fight(self.screen, 'hero', self.heroes_map[self.player_koor[0]][self.player_koor[1]])
            result = fight.run()
            if result == 'hero':
                self.heroes_map[self.player_koor[0]][self.player_koor[1]] = 'empty'
            else:
                self.player_koor = self.past_player_koor
        elif self.heroes_map[self.player_koor[0]][self.player_koor[1]] == 'chest':
            if self.chest_map[self.player_koor[0]][self.player_koor[1]] != 'empty':
                text = get_chest_num(self.level, self.chest_map[self.player_koor[0]][self.player_koor[1]])
                self.chest_map[self.player_koor[0]][self.player_koor[1]] = 'empty'
                self.ex = challenge_window.ChallengeWindow(text)
                self.ex.show()


class Textorcist:
    def __init__(self, level):
        self.level = level
        self.materials_map = read_map(level, 'materials')
        self.heroes_map = read_map(level, 'heroes')
        self.chest_map = read_map(level, 'chest')

        pygame.init()
        pygame.display.set_caption('Textorcist')
        self.screen = pygame.display.set_mode(SIZE)
        self.run()

    def clicks_processing(self, player):
        keys_event = pygame.key.get_pressed()
        if keys_event[pygame.K_UP]:
            player.new_koor(pygame.K_UP)
        if keys_event[pygame.K_DOWN]:
            player.new_koor(pygame.K_DOWN)
        if keys_event[pygame.K_LEFT]:
            player.new_koor(pygame.K_LEFT)
        if keys_event[pygame.K_RIGHT]:
            player.new_koor(pygame.K_RIGHT)

    def run(self):
        player = Player(self.screen, *MAP_SIZE, self.level, self.materials_map, self.heroes_map, self.chest_map,
                        get_player_koor(self.level))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.clicks_processing(player)
                player.heroes_processing()
            self.screen.fill((0, 0, 0))
            player.render(self.screen, player.player_koor)
            pygame.display.flip()
        pygame.quit()


def main(level):
    game = Textorcist(level)


if __name__ == '__main__':
    main('level_1')
