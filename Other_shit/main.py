import pygame as pg

if pg.get_sdl_version()[0] < 2:
    raise SystemExit(
        "This example requires pygame 2 and SDL2. _sdl2 is experimental and will change."
    )
from pygame._sdl2 import Window, messagebox




pg.display.init()

import random

answer = messagebox(
    "I will open two windows! Continue?",
    "Hello!",
    info=True,
    buttons=("Yes", "No", "Chance"),
    return_button=0,
    escape_button=1,
)
if answer == 1 or (answer == 2 and random.random() < 0.5):
    import sys

    sys.exit(0)

win = Window("asdf", resizable=True)

running = True


clock = pg.time.Clock()


win2 = Window("2nd window", resizable =True,size=(256, 256))



while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif getattr(event, "window", None) == win2:
            if event.type == pg.WINDOWCLOSE:
                win2.destroy()

    clock.tick(60)

pg.quit()



