import pygame as pg

import os
import sys
import random
import time


class FlappyBird():
    def __init__(self):
        self.pipe_list = []

        self.all_sprites = pg.sprite.Group()
        self.pipes_sp= pg.sprite.Group()
        self.bird_d_sp = pg.sprite.Group()
        self.bird_j_sp = pg.sprite.Group()
        self.bird_sp = pg.sprite.Group()

        self.bg = pg.sprite.Sprite()
        self.bg.image = load_image("background.png")
        self.bg.rect = self.bg.image.get_rect()

        self.bird = pg.sprite.Sprite()
        self.bird.image = load_image("bird.png")
        self.bird.rect = self.bird.image.get_rect()
        self.bird.rect.x = 300
        self.bird.rect.y = 300

        self.bird_jump = pg.sprite.Sprite()
        self.bird_jump.image = load_image("bird_jump.png")
        self.bird_jump.rect = self.bird_jump.image.get_rect()
        self.bird_jump.rect.x = 300
        self.bird_jump.rect.y = 300

        self.pipe_up = pg.sprite.Sprite()
        self.pipe_up.image = load_image("pipe_up.png")
        self.pipe_up.rect = self.pipe_up.image.get_rect()
        self.pipe_up.rect.x = 700
        self.pipe_up.rect.y = 400

        self.pipe_down = pg.sprite.Sprite()
        self.pipe_down.image = load_image("pipe_down.png")
        self.pipe_down.rect = self.pipe_down.image.get_rect()
        self.pipe_down.rect.x = 700
        self.pipe_down.rect.y = 280 - 900

        # Add sprites to group all_sprites
        self.all_sprites.add(self.bg)
        # self.all_sprites.add(self.bird)
        # self.all_sprites.add(self.bird_jump)
        # self.all_sprites.add(self.pipe_up)
        # self.all_sprites.add(self.pipe_down)

        # Add sprites pipe to group pipe
        self.pipes_sp.add(self.pipe_up)
        self.pipes_sp.add(self.pipe_down)

        # Add sprite bird to group bird
        self.bird_d_sp.add(self.bird)

        # Add sprite bird_jump to group bird_j
        self.bird_j_sp.add(self.bird_jump)

        # Add all sprites of bird to group bird_sp
        self.bird_sp.add(self.bird)
        self.bird_sp.add(self.bird_jump)

    def update_pipe(self):
        # # Adding Y coord of pipes to list, max count of pipes = 20
        # if len(self.pipe_list) < 15:
        #     while len(self.pipe_list) < 20:
        #         self.pipe_list.append([random.randint(150, 600)])
        self.pipe_up.rect.x -= 10
        self.pipe_down.rect.x -= 10
        # if self.pipe_up.rect.x <= -10:




def load_image(name, colorkey=None):
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

    FPS = 15
    clock = pg.time.Clock()

    running = True
    while running:
        jump = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            #Do jump
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                jump = True
                fp.bird.rect.y -= 40
                fp.bird_jump.rect.y -= 40

        if not jump:
            fp.bird.rect.y += 5
            fp.bird_jump.rect.y += 5


        fp.update_pipe()

        screen.fill((10, 10, 10))
        fp.all_sprites.draw(screen)
        fp.pipes_sp.draw(screen)
        if jump:
            fp.bird_j_sp.draw(screen)
            jump = False
        else:
            fp.bird_d_sp.draw(screen)
        clock.tick(FPS)
        pg.display.flip()

    pg.quit()

    """
    Add class Pipe what will create all pipes, spawn with pass at random height, pass = 120 and distance = 120 
    and move maybe
    Also add collisions and sprite bird_dead
    Add score with db
    Add money and shop
    """
