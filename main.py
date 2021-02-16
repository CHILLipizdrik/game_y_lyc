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

    def move(self, bird_up, bird_down):
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

    def die(self, bird_up, bird_down):
        self.bird.rect.y += 2
        self.bird_jump.rect.y += 2
        bird_up.rect.y += 2
        bird_down.rect.y += 2
        if self.bird.rect.y >= 780:
            self.bird_sp.remove(self.bird)
            self.bird_sp.remove(self.bird_jump)
            self.bird_d_sp.remove(self.bird)
            self.bird_j_sp.remove(self.bird_jump)

    def check_collide(self, pipe, bird_up, bird_down):
        for pipes_col in pipe.pipes_list_col:
            pipe_up_col, pipe_down_col = pipes_col
            if (bird_up.rect.colliderect(pipe_up_col) or
                    bird_up.rect.colliderect(pipe_down_col) or
                    bird_down.rect.colliderect(pipe_up_col) or
                    bird_down.rect.colliderect(pipe_down_col)):
                self.dead = True
                time.sleep(1)
            else:
                if not self.dead:
                    self.move(bird_up, bird_down)
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

        pipe_up_col = PipeUp(x, dl_y)
        pipe_down_col = PipeDown(x, dl_y)
        self.pipes_list_col.append([pipe_up_col, pipe_down_col])

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


class MainMenu:
    def __init__(self):
        self.bg_main = pg.transform.scale(load_image('background.png'), (width, height))
        self.font_normal = pg.font.Font(None, 100)
        self.font_chosen = pg.font.Font(None, 120)
        self.color_normal = (250, 200, 100)
        self.color_chosen = (255, 144, 0)
        self.section_start_game = "START GAME"
        self.section_records = "RECORDS"
        self.section_stats = "STATS"
        self.section_info = "INFO"
        self.section_exit = "EXIT"
        self.sections = [[self.section_start_game, False], [self.section_records, False], [self.section_stats, False],
                         [self.section_info, False], [self.section_exit, False]]
        self.sections_coords = {
            self.section_start_game: (80, 119, 549, 198),
            self.section_records: (80, 219, 439, 298),
            self.section_stats: (80, 319, 311, 398),
            self.section_info: (80, 419, 263, 498),
            self.section_exit: (80, 519, 269, 598)}

        self.text_coord = [
            [90, 129, 449, 69],
            [90, 229, 339, 69],
            [90, 329, 211, 69],
            [90, 429, 196, 69],
            [90, 529, 169, 69]]

        self.rect_coord = [
            [80, 119, 469, 79],
            [80, 219, 359, 79],
            [80, 319, 231, 79],
            [80, 419, 183, 79],
            [80, 519, 189, 79]]

        self.rect_coord_chosen = [
            [80, 119, 561, 93],
            [80, 219, 430, 93],
            [80, 319, 276, 93],
            [80, 419, 216, 93],
            [80, 519, 224, 93]]

        self.ssg = self.sections_coords[self.section_start_game]
        self.sr = self.sections_coords[self.section_records]
        self.sst = self.sections_coords[self.section_stats]
        self.si = self.sections_coords[self.section_info]
        self.se = self.sections_coords[self.section_exit]

    def main_menu(self):
        screen.blit(self.bg_main, (0, 0))
        for i in range(5):
            section = self.sections[i]
            if section[1]:
                color = self.color_chosen
                font = self.font_chosen
                text = font.render(section[0], True, color)
                rect_coord = self.rect_coord_chosen[i]
            else:
                color = self.color_normal
                font = self.font_normal
                text = font.render(section[0], True, color)
                rect_coord = self.rect_coord[i]

            screen.blit(text, self.text_coord[i])
            pg.draw.rect(screen, color, rect_coord, 3)

    def choose_section(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                if event.type == pg.MOUSEMOTION:
                    # section start game
                    if (self.ssg[0] < event.pos[0] < self.ssg[2]) and (self.ssg[1] < event.pos[1] < self.ssg[3]):
                        self.clear_selection()
                        self.sections[0][1] = True
                        self.main_menu()

                    # section records
                    elif (self.sr[0] < event.pos[0] < self.sr[2]) and (self.sr[1] < event.pos[1] < self.sr[3]):
                        self.clear_selection()
                        self.sections[1][1] = True
                        self.main_menu()

                    # section stats
                    elif (self.sst[0] < event.pos[0] < self.sst[2]) and (self.sst[1] < event.pos[1] < self.sst[3]):
                        self.clear_selection()
                        self.sections[2][1] = True
                        self.main_menu()

                    # section shop
                    elif (self.si[0] < event.pos[0] < self.si[2]) and (self.si[1] < event.pos[1] < self.si[3]):
                        self.clear_selection()
                        self.sections[3][1] = True
                        self.main_menu()

                    # section exit
                    elif (self.se[0] < event.pos[0] < self.se[2]) and (self.se[1] < event.pos[1] < self.se[3]):
                        self.clear_selection()
                        self.sections[4][1] = True
                        self.main_menu()
                    else:
                        self.clear_selection()
                        self.main_menu()

                if event.type == pg.MOUSEBUTTONDOWN:

                    # section start game
                    if (self.ssg[0] < event.pos[0] < self.ssg[2]) and (self.ssg[1] < event.pos[1] < self.ssg[3]) \
                            and event.button == 1:
                        return 1

                    # section records
                    elif (self.sr[0] < event.pos[0] < self.sr[2]) and (self.sr[1] < event.pos[1] < self.sr[3]) \
                            and event.button == 1:
                        return 2

                    # section stats
                    elif (self.sst[0] < event.pos[0] < self.sst[2]) and (self.sst[1] < event.pos[1] < self.sst[3]) \
                            and event.button == 1:
                        return 3

                    # section shop
                    elif (self.si[0] < event.pos[0] < self.si[2]) and (self.si[1] < event.pos[1] < self.si[3]) \
                            and event.button == 1:
                        return 4

                    # section exit
                    elif (self.se[0] < event.pos[0] < self.se[2]) and (self.se[1] < event.pos[1] < self.se[3]) \
                            and event.button == 1:
                        return 5

            pg.display.flip()
            clock.tick(FPS)

    def clear_selection(self):
        for i in range(5):
            self.sections[i][1] = False


class EndScreen:
    def __init__(self):
        self.font = pg.font.Font(None, 80)
        self.color_normal = (250, 200, 100)
        self.color_chosen = (255, 144, 0)
        self.section_play_again = "PLAY AGAIN"
        self.section_main_menu = "EXIT TO MENU"
        self.section_exit = "EXIT TO DESKTOP"
        self.sections = [[self.section_play_again, False], [self.section_main_menu, False], [self.section_exit, False]]
        self.sections_coords = {
            self.section_play_again: (335, 240, 695, 310),
            self.section_main_menu: (302, 326, 730, 396),
            self.section_exit: (253, 412, 776, 482)}

        self.text_coord = [
            [345, 250, 340, 56],
            [312, 336, 408, 56],
            [263, 422, 513, 56]]

        self.rect_coord = [
            [335, 240, 360, 70],
            [302, 326, 428, 70],
            [253, 412, 523, 70]]

        self.spa = self.sections_coords[self.section_play_again]
        self.smm = self.sections_coords[self.section_main_menu]
        self.se = self.sections_coords[self.section_exit]

    def end_screen(self):
        pg.draw.rect(screen, self.color_chosen, (240, 180, 550, 390), 5)
        for i in range(3):
            section = self.sections[i]
            if section[1]:
                color = self.color_chosen
            else:
                color = self.color_normal
            text = self.font.render(section[0], True, color)

            screen.blit(text, self.text_coord[i])
            pg.draw.rect(screen, color, self.rect_coord[i], 3)

    def choose_section(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                if event.type == pg.MOUSEMOTION:
                    # section play again
                    if (self.spa[0] < event.pos[0] < self.spa[2]) and (self.spa[1] < event.pos[1] < self.spa[3]):
                        self.clear_selection()
                        self.sections[0][1] = True
                        self.end_screen()

                    # section main menu
                    elif (self.smm[0] < event.pos[0] < self.smm[2]) and (self.smm[1] < event.pos[1] < self.smm[3]):
                        self.clear_selection()
                        self.sections[1][1] = True
                        self.end_screen()

                    # section exit
                    elif (self.se[0] < event.pos[0] < self.se[2]) and (self.se[1] < event.pos[1] < self.se[3]):
                        self.clear_selection()
                        self.sections[2][1] = True
                        self.end_screen()

                    else:
                        self.clear_selection()
                        self.end_screen()

                if event.type == pg.MOUSEBUTTONDOWN:
                    # section play again
                    if (self.spa[0] < event.pos[0] < self.spa[2]) and (self.spa[1] < event.pos[1] < self.spa[3]):
                        return 1

                    # section main menu
                    elif (self.smm[0] < event.pos[0] < self.smm[2]) and (self.smm[1] < event.pos[1] < self.smm[3]):
                        return 2

                    # section exit
                    elif (self.se[0] < event.pos[0] < self.se[2]) and (self.se[1] < event.pos[1] < self.se[3]):
                        return 3

            pg.display.flip()
            clock.tick(FPS)

    def clear_selection(self):
        for i in range(3):
            self.sections[i][1] = False


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


def draw_sprites(score, pipe, bird):
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


def game():
    global jump, running
    bird = Bird()
    pipe = Pipe()
    bird_up = BirdUp()
    bird_down = BirdDown()
    draw_sprites(pipe.score, pipe, bird)

    # Start game, waiting player
    start = False
    while not start:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                start = True

    while running:
        jump = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if not bird.dead:
                    jump = True

        bird.check_collide(pipe, bird_up, bird_down)

        if bird.dead:
            while bird.bird.rect.y <= 780:
                bird.die(bird_up, bird_down)
                draw_sprites(pipe.score, pipe, bird)

            running = False
            section = end_screen.choose_section()
            if section == 1:
                running = True
                break
            elif section == 2:
                running = False
                break

            elif section == 3:
                running = False
                terminate()

        draw_sprites(pipe.score, pipe, bird)
        clock.tick(FPS)

    del bird, pipe, bird_down, bird_up


if __name__ == '__main__':
    pg.init()
    size = width, height = 1024, 780
    screen = pg.display.set_mode(size)

    FPS = 15
    clock = pg.time.Clock()
    jump = False

    bg = BackGround()
    main_menu = MainMenu()
    end_screen = EndScreen()

    while True:
        section = main_menu.choose_section()
        if section == 1:
            running = True
            while running:
                game()

        elif section == 2:
            pass

        elif section == 3:
            pass

        elif section == 4:
            pass

        elif section == 5:
            terminate()

    pg.quit()
