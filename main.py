import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow import keras
import pygame as pg
import numpy as np

pg.init()


class Button:
    def __init__(self, surface:pg.Surface, cord:tuple, text:str, size:int, color:tuple, cord_surf:tuple=(0, 0), color_text:tuple=(0, 0, 0)):
        self.font = pg.font.Font(None, size)
        self.text = text
        self.cord_surf = cord_surf
        self.rect = self.font.render(text, True, color_text).get_rect(topleft=cord)
        self.rect.width, self.rect.height = self.rect.width+10*2, self.rect.height+5*2
        self.cord = cord[0]+10, cord[1]+5
        self.surf = surface
        self.color = color
        self.color_text = color_text
    def draw(self):
        text = self.font.render(self.text, True, self.color_text)
        pg.draw.rect(self.surf, self.color, self.rect)
        self.surf.blit(text, self.cord)
    def to_button(self):
        pos = pg.mouse.get_pos()
        pos = pos[0]-self.cord_surf[0], pos[1]-self.cord_surf[1]
        return self.rect.collidepoint(pos)


CELL_LINE = 15

WIDTH_PAINT = 25 * CELL_LINE
HEIGHT_PAINT = 25 * CELL_LINE

WIDTH_BUTTOMS = WIDTH_PAINT
HEIGHT_BUTTOMS = 108

WIDTH_OUTPUTS = 300
HEIGHT_OUTPUTS = HEIGHT_BUTTOMS + HEIGHT_PAINT

WIDTH = WIDTH_PAINT + WIDTH_OUTPUTS
HEIGHT = HEIGHT_OUTPUTS

BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN_LAIM = (191, 255, 0)
FPS = 60
clock = pg.time.Clock()
input = np.zeros((1, 25, 25))
output = np.zeros((1, 10))
cout_output = 0
last_output = None
model = keras.models.load_model('model')
font = pg.font.Font(None, int(HEIGHT_OUTPUTS//21*1.5))
font_naduha = pg.font.Font(None, 72)
text_naduha = font_naduha.render('Да отвали!', True, (WHITE))

screen = pg.display.set_mode((WIDTH,HEIGHT))
paint_surf = pg.Surface((WIDTH_PAINT, HEIGHT_PAINT))
buttoms_surf = pg.Surface((WIDTH_BUTTOMS, HEIGHT_BUTTOMS))
outputs_surf = pg.Surface((WIDTH_OUTPUTS, HEIGHT_OUTPUTS))

buttons = {
    'Результат':Button(buttoms_surf, (WIDTH_BUTTOMS//10*2, HEIGHT_BUTTOMS//5*2),
                          'Результат', 23, GREY,
                          (0, HEIGHT_PAINT), BLACK),
    'Очистить':Button(buttoms_surf, (WIDTH_BUTTOMS//10*6, HEIGHT_BUTTOMS//5*2),
                      'Очистить', 23, GREY,
                      (0, HEIGHT_PAINT), BLACK)
}

pg.display.set_caption('Надюха')
run = True
while run:
    clock.tick(FPS)
    mouse_pressed = pg.mouse.get_pressed()
    pos = pg.mouse.get_pos()

    if paint_surf.get_rect(topleft=(0, 0)).collidepoint(pos):
        if mouse_pressed[0]:
            input[0, pos[1] // CELL_LINE, pos[0] // CELL_LINE] = 1
        if mouse_pressed[2]:
            input[0, pos[1] // CELL_LINE, pos[0] // CELL_LINE] = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONUP:
            if buttons['Результат'].to_button():
                last_output = output
                output = model.predict(input, verbose=False)
                if (output == last_output).all():
                    cout_output += 1
                else:
                    cout_output = 0
            if buttons['Очистить'].to_button():
                cout_output = 2
                input = np.zeros((1, 25, 25))
                output = np.zeros((1, 10))

    if cout_output < 3:
        for i in range(1, 10*2+1, 2):
            text = font.render(f'{i//2}', True, WHITE)
            outputs_surf.blit(text, (WIDTH_OUTPUTS//10, HEIGHT_OUTPUTS//21*i))

            rect_output = pg.Rect(WIDTH_OUTPUTS//10*2, HEIGHT_OUTPUTS//21*i, WIDTH_OUTPUTS//10*7, HEIGHT_OUTPUTS//21)
            pg.draw.rect(outputs_surf, BLACK, rect_output, 5)

            rect_output.move_ip(5, 5)
            rect_output.width = (rect_output.width - 5 * 2) * output[0, i//2]
            rect_output.height = (rect_output.height - 5 * 2)
            pg.draw.rect(outputs_surf, GREEN_LAIM, rect_output)
    else:
        outputs_surf.blit(text_naduha, (20, 217))


    for button in buttons.values():
        if button.to_button():
            button.color_text = BLUE
        else:
            button.color_text = BLACK
        button.draw()

    for i in range(len(input[0])):
        for j in range(len(input[0, i])):
            if input[0, i, j]:
                pg.draw.rect(paint_surf, WHITE, (j * CELL_LINE, i * CELL_LINE, CELL_LINE, CELL_LINE))

    pg.display.update()

    screen.blit(paint_surf, (0, 0))
    paint_surf.fill(BLACK)

    screen.blit(outputs_surf, (WIDTH_PAINT, 0))
    outputs_surf.fill(GREY)

    screen.blit(buttoms_surf, (0, HEIGHT_PAINT))
    buttoms_surf.fill(WHITE)