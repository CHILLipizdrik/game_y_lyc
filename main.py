import pygame as pg

import os
import sys
import random
import time


class Bird:
    def __init__(self):
        self.dead = False
        self.jump = 10
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
                self.dead = True
            else:
                if not self.dead:
                    self.move()
                    pipe.update_pipe()


class Pipe:
    def __init__(self):
        self.x = 1030
        self.pipe_speed = 2
        self.score = 0
        self.pipes_list = []
        self.pipes_list_col = []
        self.pipes_sp = pg.sprite.Group()
        self.create_pipes_coords()

    def create_pipes_coords(self):
        # Adding Y coord of pipes to list, max count of pipes = 20
        x = 544

        for _ in range(5):
            x, y = x, random.randint(300, 600)
            x += 240
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

            pipe_up.rect.x -= self.pipe_speed
            pipe_down.rect.x -= self.pipe_speed

        for pipes_col in self.pipes_list_col:
            pipe_up_col, pipe_down_col = pipes_col

            pipe_up_col.rect.x -= self.pipe_speed
            pipe_down_col.rect.x -= self.pipe_speed


        for pipe in self.pipes_list:
            pipe_up, pipe_down = pipe
            if pipe_up.rect.x <= -176:
                self.pipes_list.pop(0)
                self.pipes_list_col.pop(0)
                self.pipes_sp.remove(pipe_up)
                self.pipes_sp.remove(pipe_down)
                self.add_pipes(self.x, random.randint(300, 600))
            if pipe_up.rect.x == 300:
                self.get_score()

    def get_score(self):
        self.score += 1


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


def print_score(score):
    font = pg.font.Font(None, 86)
    text = font.render(str(score), True, (252, 200, 96))
    screen.blit(text, (512, 78))


def draw_sprites(score):
    global jump

    screen.fill((0, 0, 0))
    bg.background.draw(screen)
    pipe.pipes_sp.draw(screen)
    if jump:
        bird.bird_j_sp.draw(screen)
        jump = False
    else:
        bird.bird_d_sp.draw(screen)
    print_score(score)
    pg.display.flip()


def terminate():
    pg.quit()
    sys.exit()


def main_menu():
    bg = pg.transform.scale(load_image('background.png'), (width, height))
    screen.blit(bg, (0, 0))
    font = pg.font.Font(None, 100)
    section_start_game = "START GAME"
    section_records = "RECORDS"
    section_shop = "SHOP"
    section_exit = "EXIT"
    sections = [section_start_game, section_records, section_shop, section_exit]
    sections_coords = {
        section_start_game: (90, 169, 559, 248),
        section_records: (90, 259, 449, 338),
        section_shop: (90, 349, 310, 428),
        section_exit: (90, 439, 279, 518)
    }

    text_coord = 160
    text_rect_coord = 10
    for section in sections:
        text = font.render(section, True, (252, 200, 96))
        intro_rect = text.get_rect()

        text_coord += 20
        text_rect_coord += 90
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height

        text_x = 90
        text_y = text.get_height() + text_rect_coord
        text_w = text.get_width() + 20
        text_h = text.get_height() + 10


        screen.blit(text, intro_rect)
        pg.draw.rect(screen, (252, 200, 96), (text_x, text_y, text_w, text_h), 3)

    ssg = sections_coords[section_start_game]
    sr = sections_coords[section_records]
    ss = sections_coords[section_shop]
    se = sections_coords[section_exit]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()

            if event.type == pg.MOUSEBUTTONDOWN:
                # section start game
                if (ssg[0] < event.pos[0] < ssg[2]) and (ssg[1] < event.pos[1] < ssg[3]) and event.button == 1:
                    return True

                # section records
                elif (sr[0] < event.pos[0] < sr[2]) and (sr[1] < event.pos[1] < sr[3]) and event.button == 1:
                    pass

                # section shop
                elif (ss[0] < event.pos[0] < ss[2]) and (ss[1] < event.pos[1] < ss[3]) and event.button == 1:
                    pass

                # section exit
                elif (se[0] < event.pos[0] < se[2]) and (se[1] < event.pos[1] < se[3]) and event.button == 1:
                    terminate()

        pg.display.flip()
        clock.tick(FPS)


def game(running):
    global jump

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

        draw_sprites(pipe.score)
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    size = width, height = 1024, 780
    screen = pg.display.set_mode(size)

    FPS = 15
    clock = pg.time.Clock()

    bird = Bird()
    pipe = Pipe()
    bg = BackGround()
    bird_up = BirdUp()
    bird_down = BirdDown()

    jump = False

    game(main_menu())

    pg.quit()
