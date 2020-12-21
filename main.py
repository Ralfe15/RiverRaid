import pygame, sys, random

pygame.init()


screen_height = 576 #480 w/o bar
screen_width = 704

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

score = 0

myfont = pygame.font.Font("fonts/AtariSmall.ttf", 32)
text_image = myfont.render("Score: {}".format(score), True, (252,252,84))

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

choices_left = ['jet_l.png','ship_l.png','choppa_l1.png']
choices_right = ['jet_r.png','ship_r.png','choppa_r1.png']

fuel = pygame.image.load("images/fuel.png")

bullet = pygame.image.load("images/bullet.png")
bullets = []
cooldown = 20
cooldown_counter = 0

start = True

#player atributes
width = plane.get_width()
height = plane.get_height()
vel = 4
left = False
right = False

#plane position in x axis , starting at the middle of screen
plane_x = 350 - (int(width/2))
plane_y = 420

#fuel position in x axis
fuel_x = 437

player_hitbox = pygame.Rect(plane_x, plane_y, plane.get_width(),plane.get_height())

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
            #generate enememies on main scene, with max height of 200 and minimum/maximum x specified on function call
            gen_y = random.randint(0,200)
            #check if an enemy has the
            for j in enemies_list:
                while gen_y in range(j[0][1]-25, j[0][1]+25):
                    gen_y = random.randint(0,200)
            tmp.append([random.randint(min_x,max_x), gen_y])   
        elif off:
            #generate enememies on main scene, with max height of -400/minumum of 0 and minimum/maximum x specified on function call
            gen_y = random.randint(-400,0)
            for j in enemies_list:
                while gen_y in range(j[0][1]-25, j[0][1]+25):
                    gen_y = random.randint(-400,0)
            tmp.append([random.randint(min_x,max_x), gen_y])
        tmp.append(random.choice([1,0, -1]))
        if tmp[1] == 1 or tmp[1] == 0:
            #load sprite acording to direction
            tmp.append(random.choice(choices_right))
        elif tmp[1] == -1:
            #load sprite acording to direction
            tmp.append(random.choice(choices_left))
        enemies_list.append(tmp)
    return enemies_list

def generate_fuel(number,off,max_x=405,min_x=145):
    #returns a list of lists, each being a [x,y] list of fuel coordinates, randomly generated
    fuel_list = []
    for i in range(number):
        tmp = []
        if not off:
            tmp.append([random.randint(min_x,max_x), random.randint(0,200)])
        elif off:
            tmp.append([random.randint(min_x,max_x), random.randint(-400,0)])
        fuel_list.append(tmp)
    return fuel_list

def draw_move_fuel(fuel_list):
    for galoon in fuel_list:
        screen.blit(pygame.image.load("images/fuel.png"), (galoon[0][0],galoon[0][1]))
        galoon[0][1] += scroll_speed

def draw_enemies(enemies_list):
    for enemy in enemies_list:
        if not enemy[2][:6] == "choppa":
            screen.blit(pygame.image.load('images/'+enemy[2]), enemy[0])
        #handles the heli animation
        elif enemy[2] == "choppa_l1.png":
            screen.blit(choppa_left[frame], enemy[0])
        elif enemy[2] == "choppa_r1.png":
            screen.blit(choppa_right[frame], enemy[0])
            
def check_collision(enemies_list):
     for enemy in enemies_list:
        enemy_rect = [enemy[0][0],enemy[0][1]-1,pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height()+1]
        pygame.display.update()
        if player_hitbox.colliderect(enemy_rect):
            return True

def check_fuel():
    global fuel_x
    return fuel_x < 254

def redrawWindow():
    global fuel_x
    global text_image
    if start:
        screen.blit(pygame.image.load('images/background.png').convert(), (0,bY))
        screen.blit(bg_surface, (0,bY2))
    else:
        screen.blit(bg_surface, (0,bY))
        screen.blit(bg_surface, (0,bY2))
    if right:
        draw_move_fuel(fuel_start)
        draw_move_fuel(fuel_start_off)
        screen.blit(plane_right,(plane_x, plane_y))
    elif left:
        draw_move_fuel(fuel_start)
        draw_move_fuel(fuel_start_off)
        screen.blit(plane_left,(plane_x, plane_y))
    else:
        draw_move_fuel(fuel_start)
        draw_move_fuel(fuel_start_off)
        screen.blit(plane, (plane_x, plane_y))
    draw_enemies(enemies_start)
    draw_enemies(enemies_start_off)
    move_enemies()
    pygame.draw.rect(screen,(255,0,0),player_hitbox,2)
    #barra cinza
    screen.blit(fuel_bar_bg, (0,480))
    #ponteiro de gasolina
    pygame.draw.rect(screen, (252,252,84),pygame.Rect(fuel_x,504,12,49))
    #indicador de quantidade de gasolina
    screen.blit(fuel_bar_indicator, (235,500))
    move_draw_bullets()
    bullet_collision()
    screen.blit(text_image, (20,515))
    text_image = myfont.render("Score: {}".format(score), True, (252,252,84))
    pygame.display.update()


def move_enemies():
    for i in range(len(enemies_start)):
        enemies_start[i][0][1] += scroll_speed
        if enemies_start[i][0][0] > 145 and enemies_start[i][0][0] < 500:
            enemies_start[i][0][0] += enemies_start[i][1] * 0.5
    for i in range(len(enemies_start_off)):
        enemies_start_off[i][0][1] += scroll_speed
        enemies_start_off[i][0][0] += enemies_start_off[i][1] * 0.5

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

def cooldown_handler():
    global cooldown_counter
    global cooldown
    if cooldown_counter >= cooldown:
        cooldown_counter = 0
    else:
        cooldown_counter += 1
        
def bullet_isoffscreen(curr):
    return curr[1] <= screen_height and curr[1] >= 0

def shoot():
    global cooldown_counter
    if cooldown_counter == 0:
        bullets.append([plane_x+(width/2)-3, 420])
        cooldown_counter = 1

def move_draw_bullets():
    cooldown_handler()
    for i in bullets:
        screen.blit(pygame.image.load("images/bullet.png"), (i[0], i[1]))
        i[1] -= 15
        if not bullet_isoffscreen(i):
            bullets.remove(i)

def bullet_collision():
    global score
    for bullet in bullets:
     for enemy in enemies_start:
         enemy_rect = [enemy[0][0],enemy[0][1]-1,pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height()+1]
         bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
         if bullet_rect.colliderect(enemy_rect):
            score += 30
            bullets.remove(bullet)
            enemies_start.remove(enemy)
     for enemy in enemies_start_off:
         enemy_rect = [enemy[0][0],enemy[0][1]-1,pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height()+1]
         bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
         if bullet_rect.colliderect(enemy_rect):
            score +=30
            bullets.remove(bullet)
            enemies_start_off.remove(enemy)
     for galoon in fuel_start:
        galoon_rect = [galoon[0][0],galoon[0][1]-1,pygame.image.load("images/fuel.png").get_width(),pygame.image.load("images/fuel.png").get_height()+1]
        bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
        if bullet_rect.colliderect(galoon_rect):
            score += 80
            bullets.remove(bullet)
            fuel_start.remove(galoon)
     for galoon in fuel_start_off:
        galoon_rect = [galoon[0][0],galoon[0][1]-1,pygame.image.load("images/fuel.png").get_width(),pygame.image.load("images/fuel.png").get_height()+1]
        bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
        if bullet_rect.colliderect(galoon_rect):
            score += 80
            bullets.remove(bullet)
            fuel_start_off.remove(galoon)
                
def collision_with_fuel(fuel_list):
    global fuel_x
    for galoon in fuel_list:
            galoon_rect = [galoon[0][0],galoon[0][1]-1,pygame.image.load("images/fuel.png").get_width(),pygame.image.load("images/fuel.png").get_height()+1]
            if player_hitbox.colliderect(galoon_rect) and fuel_x < 437:
                fuel_x += 0.6




enemies_start = generate_enemies(3, False)
enemies_start_off = generate_enemies(5, True)
fuel_start = generate_fuel(1,False)
fuel_start_off = generate_fuel(3, True)


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

    #move background
    bY += scroll_speed
    bY2 += scroll_speed

    #move fuel pointer
    fuel_x -= 0.125
    
    #handle infinite scroll

    if bY > bg_surface.get_height():
        bY = -1*bg_surface.get_height()
        start = False
        enemies_start = generate_enemies(5, True)
        fuel_start = generate_fuel(3,True)
    if bY2 > bg_surface.get_height():
        bY2 = -1*bg_surface.get_height()
        enemies_start_off = generate_enemies(5, True)
        fuel_start_off = generate_fuel(3, True)

    # collision with enemies check
    if check_collision(enemies_start) or  check_collision(enemies_start_off): 
        pygame.quit()
        quit()
    #no fuel check
    if check_fuel():
        pygame.quit()
        quit()
    collision_with_fuel(fuel_start)
    collision_with_fuel(fuel_start_off)
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
    if keys[pygame.K_SPACE]:
        shoot()


    clock.tick(speed)
