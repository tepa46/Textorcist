import pygame
import sys
import os

size = [660, 660]


def read_map(level):
    with open(f'levels/{level}/map.txt', 'r', encoding='utf8') as f:
        map_file = f.read().split('\n')
        return [pic.split(' ') for pic in map_file]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', f'{name}.png')
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 60

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, map, koor):
        all_sprites = pygame.sprite.Group()
        for i in range(-5, 6, 1):
            for j in range(-5, 6, 1):
                sprite = pygame.sprite.Sprite(all_sprites)
                sprite.image = pygame.transform.scale(load_image(map[koor[0] + i][koor[1] + j]), (60, 60))
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = (koor[1] + j) * self.cell_size
                sprite.rect.y = (koor[0] + i) * self.cell_size
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color('WHITE'), (
                    j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size),
                                 width=1)

        all_sprites.draw(screen)


class Player(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.player_koor = (5, 5)

    def new_koor(self, command):
        if command == pygame.K_UP:
            self.player_koor[0] -= 1
        elif command == pygame.K_DOWN:
            self.player_koor[0] += 1
        elif command == pygame.K_LEFT:
            self.player_koor[1] -= 1
        elif command == pygame.K_RIGHT:
            self.player_koor[1] += 1


class BoardGame:
    def __init__(self, level):
        self.map = read_map(level)

        pygame.init()
        pygame.display.set_caption('Textorcist')
        self.screen = pygame.display.set_mode(size)
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
        player = Player(11, 11)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.clicks_processing(player)
            self.screen.fill((0, 0, 0))
            player.render(self.screen, self.map, player.player_koor)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = BoardGame('level_1')
