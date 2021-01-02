import pygame
import sys
import os

SIZE = (300, 300)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Arrow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('Герой двигается')
        self.koor = [0, 0]

        self.run()

    def run(self):
        running = True
        pygame.mouse.set_visible(False)
        all_sprites = pygame.sprite.Group()

        arrow = pygame.sprite.Sprite(all_sprites)
        arrow.image = load_image("creature.png")
        arrow.rect = arrow.image.get_rect()
        self.screen.fill((255, 255, 255))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                keys_event = pygame.key.get_pressed()
                self.screen.fill((255, 255, 255))
                if keys_event[pygame.K_UP]:
                    self.koor[1] -= 10
                if keys_event[pygame.K_DOWN]:
                    self.koor[1] += 10
                if keys_event[pygame.K_LEFT]:
                    self.koor[0] -= 10
                if keys_event[pygame.K_RIGHT]:
                    self.koor[0] += 10
                all_sprites.draw(self.screen)
                arrow.rect = self.koor
            pygame.display.flip()


if __name__ == '__main__':
    game = Arrow()
