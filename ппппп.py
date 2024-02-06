import pygame
from pygame.locals import *

pygame.init()

wid = 600
hei = 600

sc = pygame.display.set_mode((wid, hei))
pygame.display.set_caption("нач")


class Button:
    def __init__(self, x, y, widd, heii, color):
        self.rect = pygame.Rect(x, y, widd, heii)
        self.color = color

    def draw(self):
        pygame.draw.rect(sc, self.color, self.rect)


sp_bt = []
bt_wid = 110
bt_hei = 110
bt1 = 40


x = (wid - bt_wid * 3 - bt1 * 2) / 2
y = (hei - bt_hei * 3 - bt1 * 2) / 2

for i in range(3):
    for j in range(3):
        button = Button(x, y, bt_wid, bt_hei, (0, 128, 128))
        sp_bt.append(button)
        x += bt_wid + bt1
    y += bt_hei + bt1
    x = (wid - bt_wid * 3 - bt1 * 2) / 2

running = True
while running:

    sc.fill((0, 0, 128))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    for button in sp_bt:
        button.draw()

    pygame.display.update()

pygame.quit()