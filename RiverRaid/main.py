import pygame
pygame.init()

SCREEN_WIDTH = 1065
SCREEN_HEIGHT = 700

colors = {"null": 0x000000, "plane": 0xE8E84A, "background": 0x6E9C42, "water": 0x2D32B8}

win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("River Raid")

bg_surface = pygame.image.load("images/water-bg.jpg").convert()
bg_y_pos = 0

clock = pygame.time.Clock()
#player atributes
x = 50
y = 450
width = 40
height = 60
vel = 5
acel = 0

run = True
while run:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x-=vel
    if keys[pygame.K_RIGHT] and x < SCREEN_WIDTH - width - vel:
        x+=vel
    if keys[pygame.K_UP] and y > vel:
        y-=vel
    if keys[pygame.K_DOWN] and y < SCREEN_HEIGHT - height - vel:
        y+=vel
    pygame.draw.rect(win, (255,0,0), (x,y,width,height))

    clock.tick(60)



pygame.quit()
