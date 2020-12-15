import pygame, sys, random

pygame.init()


screen_height = 576 #480 w/o bar
screen_width = 704

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

#background
bg_surface = pygame.image.load('images/bckg-1.jpeg').convert()
bY = 0
bY2 = bg_surface.get_height()
fuel_bar_bg = pygame.image.load('images/bar test.png')
fuel_bar_indicator = pygame.image.load('images/bar_indicators.png')

#images of the player
plane = pygame.image.load('images/plane-still.png')
plane_left = pygame.image.load('images/plane-left.png')
plane_right = pygame.image.load('images/plane-right.png')


#images of the enemies
choppa_l1, choppa_l2 = pygame.image.load('images/choppa_l1.png'), pygame.image.load('images/choppa_l2.png')
choppa_r1, choppa_r2 = pygame.image.load('images/choppa_r1.png'), pygame.image.load('images/choppa_r2.png')

choppa_right = [choppa_r1, choppa_r2]
choppa_left = [choppa_l1, choppa_l2]

ship_left = pygame.image.load('images/ship_l.png')
ship_right = pygame.image.load('images/ship_r.png')

jet_left = pygame.image.load('images/jet_l.png')
jet_right = pygame.image.load('images/jet_r.png')

choices_left = ['jet_l.png','ship_l.png','choppa_l1.png']
choices_right = ['jet_r.png','ship_r.png','choppa_r1.png']

start = True

#player atributes
width = plane.get_width()
height = plane.get_height()
vel = 5
left = False
right = False

#plane position in x axis , starting at the middle of screen
plane_x = 350 - (int(width/2))
plane_y = 420


player_hitbox = pygame.Rect(plane_x, plane_y, plane.get_width(),plane.get_height())

fuel_pointer = pygame.Rect(437, 505,12,49)


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
    return enemies_list

def draw_enemies(enemies_list):
    for enemy in enemies_list:
        if not enemy[2][:6] == "choppa":
            screen.blit(pygame.image.load('images/'+enemy[2]), enemy[0])
        elif enemy[2] == "choppa_l1.png":
            screen.blit(choppa_left[frame], enemy[0])
        elif enemy[2] == "choppa_r1.png":
            screen.blit(choppa_right[frame], enemy[0])
            
def check_collision(enemies_list):
     for enemy in enemies_list:
        enemy_rect = [enemy[0][0],enemy[0][1]-1,pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height()+1]
        pygame.draw.rect(screen,(0,255,0), enemy_rect,2)
        pygame.display.update()
        if player_hitbox.colliderect(enemy_rect):
            return True

def redrawWindow():
    if start:
        screen.blit(pygame.image.load('images/background.png').convert(), (0,bY))
        screen.blit(bg_surface, (0,bY2))
    else:
        screen.blit(bg_surface, (0,bY))
        screen.blit(bg_surface, (0,bY2))
    if right:
        screen.blit(plane_right,(plane_x, plane_y))
    elif left:
        screen.blit(plane_left,(plane_x, plane_y))
    else:
        screen.blit(plane, (plane_x, plane_y))
    draw_enemies(enemies_start)
    draw_enemies(enemies_start_off)
    move_enemies()
    pygame.draw.line(screen,(255,0,0),(0, bY),(704,bY))
    pygame.draw.line(screen,(255,0,0),(0, bY2),(704,bY2))
    pygame.draw.rect(screen,(255,0,0),player_hitbox,2)
    screen.blit(fuel_bar_bg, (0,480))
    #ponteiro de gasolina
    pygame.draw.rect(screen, (252,252,84),fuel_pointer)
    screen.blit(fuel_bar_indicator, (235,500))
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
    time = pygame.time.get_ticks()
    frame = int((time/speed)%len(choppa_right))

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

    # collision with enemies check
    if check_collision(enemies_start) or  check_collision(enemies_start_off): 
        pygame.quit()
        quit()

    # keys handle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        left = False
        right = False
    elif keys[pygame.K_LEFT]:
        plane_x-=vel
        player_hitbox.x -= vel
        left = True    
    elif keys[pygame.K_RIGHT]:
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
