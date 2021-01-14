import pygame as pg

import os
import sys
import random
import time


class Bird:
    def __init__(self):
        self.dead = False
        self.jump = 8
        self.fall = 2
        self.bird_d_sp = pg.sprite.Group()
        self.bird_j_sp = pg.sprite.Group()
        self.bird_sp = pg.sprite.Group()

        self.bird = pg.sprite.Sprite()
        self.bird_img = load_image("bird.png")
        self.bird.image = self.bird_img
        self.bird.rect = self.bird.image.get_rect()
        self.bird.rect.x = 300
        self.bird.rect.y = 300

        self.bird_jump = pg.sprite.Sprite()
        self.bird_jump_img = load_image("bird_jump.png")
        self.bird_jump.image = self.bird_jump_img
        self.bird_jump.rect = self.bird_jump.image.get_rect()
        self.bird_jump.rect.x = 300
        self.bird_jump.rect.y = 300

        self.rect = self.bird_img.get_rect()

        # Add sprite bird to group bird
        self.bird_d_sp.add(self.bird)

        # Add sprite bird_jump to group bird_j
        self.bird_j_sp.add(self.bird_jump)

        # Add all sprites of bird to group bird_sp
        self.bird_sp.add(self.bird)
        self.bird_sp.add(self.bird_jump)

    def move(self):
        if jump:
            self.bird.rect.y -= self.jump
            self.bird_jump.rect.y -= self.jump
            bird_up.rect.y -= self.jump
            bird_down.rect.y -= self.jump

        elif not jump:
            self.bird.rect.y += self.fall
            self.bird_jump.rect.y += self.fall
            bird_up.rect.y += self.fall
            bird_down.rect.y += self.fall

    def die(self):
        self.bird.rect.y += 15
        self.bird_jump.rect.y += 15
        bird_up.rect.y += 15
        bird_down.rect.y += 15
        if self.bird.rect.y >= 775:
            quit()

    def check_collide(self):
        global running

        for pipes_col in pipe.pipes_list_col:
            pipe_up_col, pipe_down_col = pipes_col
            if (bird_up.rect.colliderect(pipe_up_col) or
                bird_up.rect.colliderect(pipe_down_col) or
                bird_down.rect.colliderect(pipe_up_col) or
                bird_down.rect.colliderect(pipe_down_col)):
                print(1)
                self.dead = True
            else:
                if not self.dead:
                    self.move()
                    pipe.update_pipe()


class Pipe:

    def __init__(self):
        self.x = 1000
        self.pipes_list_y_cord = []
        self.pipes_list = []
        self.pipes_list_col = []
        self.pipes_sp = pg.sprite.Group()
        self.create_pipes_coords()

    def create_pipes_coords(self):
        # Adding Y coord of pipes to list, max count of pipes = 20

        for _ in range(5):
            self.pipes_list_y_cord.append([self.x, random.randint(300, 600)])
            self.x += 240
        self.create_pipes()

    def create_pipes(self):
        for p in self.pipes_list_y_cord:
            x, y = p
            self.add_pipes(x, y)

    def add_pipes(self, x, dl_y):
        self.pipe_up = pg.sprite.Sprite()
        self.pipe_up_img = load_image("pipe_up.png")
        self.pipe_up.image = self.pipe_up_img
        self.pipe_up.rect = self.pipe_up.image.get_rect()
        self.pipe_up.rect.x = x
        self.pipe_up.rect.y = dl_y

        self.pipe_down = pg.sprite.Sprite()
        self.pipe_down_img = load_image("pipe_down.png")
        self.pipe_down.image = self.pipe_down_img
        self.pipe_down.rect = self.pipe_down.image.get_rect()
        self.pipe_down.rect.x = x
        self.pipe_down.rect.y = dl_y - 200 - 900

        # Add sprites pipe to group pipe
        self.pipes_sp.add(self.pipe_up)
        self.pipes_sp.add(self.pipe_down)
        self.pipes_list.append([self.pipe_up, self.pipe_down])

        self.pipe_up_col = PipeUp(x, dl_y)
        self.pipe_down_col = PipeDown(x, dl_y)
        self.pipes_list_col.append([self.pipe_up_col, self.pipe_down_col])

    def update_pipe(self):
        for pipes in self.pipes_list:
            pipe_up, pipe_down = pipes

            pipe_up.rect.x -= 2
            pipe_down.rect.x -= 2

        for pipes_col in self.pipes_list_col:
            pipe_up_col, pipe_down_col = pipes_col

            pipe_up_col.rect.x -= 2
            pipe_down_col.rect.x -= 2

        # if self.pipe_up.rect.x <= -10:
        #     self.pipes_list_y_cord.remove(self.pipes_list_y_cord[0])
        #     self.pipes_list.remove(self.pipes_list[0])
        #     self.pipes_list_col.remove(self.pipes_list_col[0])


class BirdUp:
    def __init__(self):
        self.image = load_image("bird_jump.png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300


class BirdDown:
    def __init__(self):
        self.image = load_image("bird.png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300


class PipeUp:
    def __init__(self, x, y):
        self.image = load_image("pipe_up.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class PipeDown:
    def __init__(self, x, y):
        self.image = load_image("pipe_down.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 200 - 900


class BackGround:
    def __init__(self):
        self.background = pg.sprite.Group()

        self.bg = pg.sprite.Sprite()
        self.bg.image = load_image("background.png")
        self.bg.rect = self.bg.image.get_rect()

        self.background.add(self.bg)


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


def draw_sprites():
    global jump

    screen.fill((0, 0, 0))
    bg.background.draw(screen)
    pipe.pipes_sp.draw(screen)
    if jump:
        bird.bird_j_sp.draw(screen)
        jump = False
    else:
        bird.bird_d_sp.draw(screen)
    pg.display.flip()


if __name__ == '__main__':
    pg.init()
    size = width, height = 1024, 768
    screen = pg.display.set_mode(size)

    bird = Bird()
    pipe = Pipe()
    bg = BackGround()
    bird_up = BirdUp()
    bird_down = BirdDown()

    FPS = 15
    clock = pg.time.Clock()

    running = True
    while running:
        jump = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # Do jump
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if not bird.dead:
                    jump = True

        bird.check_collide()

        if bird.dead:
            bird.die()

        draw_sprites()
        clock.tick(FPS)

    pg.quit()

    """Add class Pipe what will create all pipes, spawn with pass at random 
    height, pass = 120 and distance = 120 and move maybe 
    Also add collisions and sprite bird_dead Add score with db 
    Add money and shop and skins"""
