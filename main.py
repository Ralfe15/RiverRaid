import pygame, sys, random

pygame.init()

screen_height = 480
screen_width = 704

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

#background
bg_surface = pygame.image.load('images/bckg-1.jpeg').convert()
bY = 0
bY2 = bg_surface.get_height()

#images of the player
plane = pygame.image.load('images/plane-still.png')
plane_left = pygame.image.load('images/plane-left.png')
plane_right = pygame.image.load('images/plane-right.png')

fuel_bar = pygame.image.load('images/fuel_bar.png')

#images of the enemies
choppa_l1, choppa_l2 = pygame.image.load('images/choppa_l1.png'), pygame.image.load('images/choppa_l2.png')
choppa_r1, choppa_r2 = pygame.image.load('images/choppa_r1.png'), pygame.image.load('images/choppa_r2.png')

choppa_right = [choppa_r1, choppa_r2]
choppa_left = [choppa_l1, choppa_l2]

ship_left = pygame.image.load('images/ship_l.png')
ship_right = pygame.image.load('images/ship_r.png')

jet_left = pygame.image.load('images/jet_l.png')
jet_right = pygame.image.load('images/jet_r.png')

choices_left = ['jet_l.png','ship_l.png']
choices_right = ['jet_r.png','ship_r.png']

start = True

#player atributes
width = plane.get_width()
height = plane.get_height()
vel = 5
left = False
right = False

#plane position in x axis , starting at the middle of screen
plane_x = 350 - (int(width/2))

player_hitbox = pygame.Rect(plane_x, 420, plane.get_width(),plane.get_height())

#camera scrolling
up_pressed = False
down_pressed = False
scroll_speed = 1.5

#enemies
def generate_enemies(number,off,max_x=405,min_x=145):
    #returns a list of lists, each being an enemy with: [0] = list of x,y coords, [1] = direction, [2] = enemy type
    enemies_list = []
    for i in range(number):
        tmp = []
        if not off:
            tmp.append([random.randint(min_x,max_x), random.randint(0,200)])
        elif off:
            tmp.append([random.randint(min_x,max_x), random.randint(-400,0)])
        tmp.append(random.choice([1,0, -1]))
        if tmp[1] == 1 or tmp[1] == 0:
            tmp.append(random.choice(choices_right))
        elif tmp[1] == -1:
            tmp.append(random.choice(choices_left))
        enemies_list.append(tmp)
    print(enemies_list)
    return enemies_list 

def draw_enemies(enemies_list):
    
    for enemy in enemies_list:
        enemy_rect = [enemy[0][0],enemy[0][1],pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height()]
        pygame.draw.rect(screen,(255,0,0),enemy_rect,2)
        if player_hitbox.colliderect(enemy_rect):
            return True
        screen.blit(pygame.image.load('images/'+enemy[2]), enemy[0])




def redrawWindow():
    if start:
        screen.blit(pygame.image.load('images/background.png').convert(), (0,bY))
        screen.blit(bg_surface, (0,bY2))
    else:
        screen.blit(bg_surface, (0,bY))
        screen.blit(bg_surface, (0,bY2))
    if right:
        screen.blit(plane_right,(plane_x, 420))
    elif left:
        screen.blit(plane_left,(plane_x, 420))
    else:
        screen.blit(plane, (plane_x, 420))
    draw_enemies(enemies_start)
    draw_enemies(enemies_start_off)
    move_enemies()
    pygame.draw.line(screen,(255,0,0),(0, bY),(704,bY))
    pygame.draw.line(screen,(255,0,0),(0, bY2),(704,bY2))
    pygame.draw.rect(screen,(255,0,0),player_hitbox,2)
    pygame.display.update()


def move_enemies():
    for i in range(len(enemies_start)):
        enemies_start[i][0][1] += scroll_speed
        enemies_start[i][0][0] += enemies_start[i][1] *0.5
    for i in range(len(enemies_start_off)):
        enemies_start_off[i][0][1] += scroll_speed
        enemies_start_off[i][0][0] += enemies_start_off[i][1] *0.5

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



enemies_start = generate_enemies(3, False)
enemies_start_off = generate_enemies(5, True)


speed = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    redrawWindow()
    checkScroll()

    bY += scroll_speed
    bY2 += scroll_speed
    
    #handle infinite scroll
    if bY > bg_surface.get_height():
        bY = -1*bg_surface.get_height()
        start = False
        enemies_start = generate_enemies(5, True)
        
    if bY2 > bg_surface.get_height():
        bY2 = -1*bg_surface.get_height()
        enemies_start_off = generate_enemies(5, True)

    if draw_enemies(enemies_start) or  draw_enemies(enemies_start_off):
        break


        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        left = False
        right = False
    elif keys[pygame.K_LEFT]: #test value
        plane_x-=vel
        player_hitbox.x -= vel

        left = True    
    elif keys[pygame.K_RIGHT]: #test value
        plane_x+=vel
        player_hitbox.x +=vel

        
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
