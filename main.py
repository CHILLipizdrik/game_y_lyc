import pygame as pg

import os
import sys


class FlappyBird():
    def __init__(self):
        self.all_sprites = pg.sprite.Group()

        self.bg = pg.sprite.Sprite()
        self.bg.image = self.load_image("background.png")
        self.bg.rect = self.bg.image.get_rect()

        self.bird = pg.sprite.Sprite()
        self.bird.image = self.load_image("bird.png")
        self.bird.rect = self.bird.image.get_rect()
        self.bird.rect.x = 300
        self.bird.rect.y = 300

        self.bird_jump = pg.sprite.Sprite()
        self.bird_jump.image = self.load_image("bird_jump.png")
        self.bird_jump.rect = self.bird_jump.image.get_rect()

        self.pipe_up = pg.sprite.Sprite()
        self.pipe_up.image = self.load_image("pipe_up.png")
        self.pipe_up.rect = self.pipe_up.image.get_rect()
        self.pipe_up.rect.x = 700
        self.pipe_up.rect.y = 370

        self.pipe_down = pg.sprite.Sprite()
        self.pipe_down.image = self.load_image("pipe_down.png")
        self.pipe_down.rect = self.pipe_down.image.get_rect()
        self.pipe_down.rect.x = 700
        self.pipe_down.rect.y = 280 - 900

        self.all_sprites.add(self.bg)
        self.all_sprites.add(self.bird)
        self.all_sprites.add(self.bird_jump)
        self.all_sprites.add(self.pipe_up)
        self.all_sprites.add(self.pipe_down)


    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pg.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

if __name__ == '__main__':
    pg.init()
    size = width, height = 1024, 768
    screen = pg.display.set_mode(size)
    fp = FlappyBird()

    FPS = 60
    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


        screen.fill((10, 10, 10))
        fp.all_sprites.draw(screen)
        clock.tick(FPS)
        pg.display.flip()

    pg.quit()
