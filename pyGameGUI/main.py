from module import TextBox,Window,Label
import pygame
import sys

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tbox = TextBox(20,20,w=400,h=75)
tbox.focus()

rtWind = Window()
rtWind.add_component(TextBox(30,100),"field1")

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))
            try:
                rtWind.recv_key(event.key)
            except:
                continue
        elif event.type == pygame.QUIT:
            sys.exit(-1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tx, ty = pygame.mouse.get_pos()
            rtWind.recv_mouse(tx,ty)
    rtWind.tick()
    screen.fill((0, 0, 240))
    rtWind.draw(screen)
    pygame.display.update()