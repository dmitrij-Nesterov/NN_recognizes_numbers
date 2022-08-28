import pygame as pg
import numpy as np

pg.init()
CELL_LINE = 21
WIDTH = 25 * CELL_LINE
HEIGHT = 25 * CELL_LINE
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
FPS = 60

clock = pg.time.Clock()
traning_input, traning_output = np.load('Traning_inputs.npz').values()
cout = len(traning_input)
traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
cout_input = np.bincount(traning_output.astype('int64'))
font = pg.font.Font(None, 27)
screen = pg.display.set_mode((WIDTH,HEIGHT))
run = True
while run:
    clock.tick(FPS)
    mouse_pressed = pg.mouse.get_pressed()
    pos = pg.mouse.get_pos()

    if mouse_pressed[0]:
        traning_input[cout, pos[1] // CELL_LINE, pos[0] // CELL_LINE] = 1
    if mouse_pressed[2]:
        traning_input[cout, pos[1] // CELL_LINE, pos[0] // CELL_LINE] = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_c:
                traning_input[cout] = np.zeros((25, 25))
            if event.key == pg.K_d and cout > 0:
                cout -= 1
                cout_input[int(traning_output[-1])] -= 1
                traning_input = np.delete(traning_input, -1, axis=0)
                traning_output = np.delete(traning_output, -1)
            if event.key == pg.K_w and traning_output.any():
                np.savez('Traning_inputs', traning_inputs=np.delete(traning_input, -1, axis=0), traning_outputs=traning_output)

            if event.key == pg.K_0:
                cout_input[0] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 0)
            if event.key == pg.K_1:
                cout_input[1] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 1)
            if event.key == pg.K_2:
                cout_input[2] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 2)
            if event.key == pg.K_3:
                cout_input[3] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 3)
            if event.key == pg.K_4:
                cout_input[4] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 4)
            if event.key == pg.K_5:
                cout_input[5] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 5)
            if event.key == pg.K_6:
                cout_input[6] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 6)
            if event.key == pg.K_7:
                cout_input[7] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 7)
            if event.key == pg.K_8:
                cout_input[8] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 8)
            if event.key == pg.K_9:
                cout_input[9] += 1
                cout += 1
                traning_input = np.append(traning_input, np.zeros((1, 25, 25)), axis=0)
                traning_output = np.append(traning_output, 9)

    for i in range(len(traning_input[cout])):
        for j in range(len(traning_input[cout, i])):
            if traning_input[cout, i, j]:
                pg.draw.rect(screen, WHITE, (j * CELL_LINE, i * CELL_LINE, CELL_LINE, CELL_LINE))

    for i in range(1, 10*2+1, 2):
        text = font.render(f'{i//2}:{cout_input[i//2]}', True, GREY)
        screen.blit(text, (i*25, 20))

    pg.display.update()
    screen.fill(BLACK)