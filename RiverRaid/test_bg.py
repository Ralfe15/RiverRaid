import pygame, sys, random

pygame.init()

screen_height = 480

screen_width = 704

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

#sprites and background
bg_surface = pygame.image.load('images/background.png').convert()
bY = 0
bY2 = bg_surface.get_height()
plane = pygame.image.load('images/plane-still.png')
bigger_plane = pygame.transform.scale(plane, (int(plane.get_width()*2),int(plane.get_height()*2)))
plane_left = pygame.image.load('images/plane-left.png')
bigger_plane_left = pygame.transform.scale(plane_left, (int(plane_left.get_width()*2),int(plane_left.get_height()*2)))
plane_right = pygame.image.load('images/plane-right.png')
bigger_plane_right = pygame.transform.scale(plane_right, (int(plane_right.get_width()*2),int(plane_right.get_height()*2)))

fuel_bar = pygame.image.load('images/fuel_bar.png')

start = True

#player atributes
width = plane.get_width()
height = plane.get_height()
vel = 5
acel = 0
left = False
right = False

#plane position in x axis , starti\ng at the middle of screen
plane_x = screen_width/2 - width/2

#camera scrolling
up_pressed = False
down_pressed = False
scroll_speed = 1

enemies_img = pygame.image.load('images/choppa.png')
bigger_enemies = pygame.transform.scale(enemies_img, (int(enemies_img.get_width()*2),int(enemies_img.get_height()*2)))

def generate_enemies():
    enemies_x = [random.randint(160,515) for i in range(3)]
    enemies_y = [random.randint(0,300) for i in range(3)]
    enemies_coords = list(zip(enemies_x,enemies_y))
    enemies_direct = [random.choice([1,0, -1]) for i in range(3)]
    return enemies_x, enemies_y, enemies_coords, enemies_direct


def draw_enemies():
    for enemy in enemies_coords:
        screen.blit(bigger_enemies, enemy)

def generate_enemies_off():
    enemies_x_off = [random.randint(160,515) for i in range(3)]
    enemies_y_off = [random.randint(-300,0) for i in range(3)]
    enemies_coords_off = list(zip(enemies_x_off,enemies_y_off))
    enemies_direct_off = [random.choice([1,0, -1]) for i in range(3)]
    return enemies_x_off, enemies_y_off,enemies_coords_off, enemies_direct_off

def draw_enemies_off():
    for enemy in enemies_coords_off:
        screen.blit(bigger_enemies, enemy)

enemies_x, enemies_y, enemies_coords, enemies_direct = generate_enemies()
enemies_x_off, enemies_y_off, enemies_coords_off, enemies_direct_off = generate_enemies_off()

def redrawWindow():
    if start:
        screen.blit(pygame.image.load('images/background.png').convert(), (0,bY))
        screen.blit(pygame.image.load('images/bckg-1.jpeg').convert(), (0,bY2))
        draw_enemies()
        draw_enemies_off()
    else:
        screen.blit(pygame.image.load('images/bckg-1.jpeg').convert(), (0,bY))
        screen.blit(pygame.image.load('images/bckg-1.jpeg').convert(), (0,bY2))
        draw_enemies()
        draw_enemies_off()
    if right:
        screen.blit(bigger_plane_right,(plane_x, 420))
    elif left:
        screen.blit(bigger_plane_left,(plane_x, 420))
    else:
        screen.blit(bigger_plane, (plane_x, 420))

    pygame.display.update()


def checkScroll():
    global scroll_speed
    if up_pressed and scroll_speed < 5.5:
        scroll_speed += 0.5
    elif down_pressed and scroll_speed > 1.0:
        scroll_speed -= 0.5
    else:
        if scroll_speed > 1.5:
            scroll_speed -= 0.08
        elif scroll_speed < 1.5:
            scroll_speed += 0.08       



speed = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    redrawWindow()
    checkScroll()

    bY += scroll_speed #scrolling speed
    bY2 += scroll_speed
    for i in range(len(enemies_y)):
        enemies_y[i] += scroll_speed
        enemies_y_off[i] += scroll_speed
    for i in range(len(enemies_x)):
        enemies_x_off[i] += enemies_direct_off[i]*0.5
        enemies_x[i] += enemies_direct[i] *0.5
        
    enemies_coords = list(zip(enemies_x,enemies_y))
    enemies_coords_off = list(zip(enemies_x_off,enemies_y_off))
        
    if bY > bg_surface.get_height():
        bY = -1*bg_surface.get_height()
        start = False
        print("A")
        
    if bY2 > bg_surface.get_height():
        bY2 = -1*bg_surface.get_height()
        print("B")

        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        left = False
        right = False
    elif keys[pygame.K_LEFT]: #test value
        plane_x-=vel
        left = True    
    elif keys[pygame.K_RIGHT]: #test value
        plane_x+=vel
        right = True
    else:
        left = False
        right = False
    if keys[pygame.K_UP]:
        up_pressed = True
    elif keys[pygame.K_DOWN]:
        down_pressed = True
    else:
        up_pressed = False
        down_pressed = False
    clock.tick(speed)
