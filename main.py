import pygame as pg

pg.init()

if __name__ == '__main__':
    size = width, height = 1280, 720
    screen = pg.display.set_mode(size)
    screen.fill((10, 10, 10))

    FPS = 60
    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        clock.tick(FPS)
        pg.display.flip()

    pg.quit()
