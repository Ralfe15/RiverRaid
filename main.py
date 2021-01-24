import pygame, sys, random, json
from rectangles import getRects, getBridges


# Screen properties
screen_height = 576
screen_width = 704

### Inits
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

### Loads
# Map collision rects and bridges
rects = getRects()
bridges = getBridges()

# Sound effects
pygame.mixer.pre_init(44100, -16, 1, 256)
fly_normal = pygame.mixer.music.load("sounds/player_flying_normal.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
player_shoot = pygame.mixer.Sound("sounds/player_shooting.wav")
pygame.mixer.Sound.set_volume(player_shoot, 2)
enemy_explosion = pygame.mixer.Sound("sounds/enemy_destroyed.wav")
pygame.mixer.Sound.set_volume(enemy_explosion, 2)
refuel = pygame.mixer.Sound("sounds/player_refueling.wav")
pygame.mixer.Sound.set_volume(refuel, 2)
refuel_full = pygame.mixer.Sound("sounds/player_refueling_full.wav")
pygame.mixer.Sound.set_volume(refuel_full, 2)

# Score/lives display
score = 0
myfont = pygame.font.Font("fonts/AtariSmall.ttf", 32)
text_image = myfont.render("Score: {}".format(score), True, (252,252,84))
lives = 3
lives_text_image = myfont.render("Lives: {}".format(lives), True, (252,252,84))

# Intro text
myfont_intro = pygame.font.Font("fonts/AtariSmall.ttf", 64)
text_image_intro = myfont_intro.render("River Raid", True, (252,252,84))
myfont_intro_sub = pygame.font.Font("fonts/AtariSmall.ttf", 32)
text_image_intro_sub = myfont_intro_sub.render("Press spacebar to start", True, (252,252,84))


# Background
on_screen = pygame.image.load('map/map1/1.png').convert()
off_screen = pygame.image.load('map/map1/2.png').convert()
bY = 0
bY2 = off_screen.get_height()
fuel_bar_bg = pygame.image.load('images/bar test.png')
fuel_bar_indicator = pygame.image.load('images/bar_indicators.png')

intro_background = pygame.image.load('map/intro/intro.png')
introY = -380
intro_background2 = pygame.image.load('map/intro/intro_2.png')

# Player images
plane = pygame.image.load('images/plane-still.png')
plane_left = pygame.image.load('images/plane-left.png')
plane_right = pygame.image.load('images/plane-right.png')

# Enemies images
choppa_l1, choppa_l2 = pygame.image.load('images/choppa_l1.png'), pygame.image.load('images/choppa_l2.png')
choppa_r1, choppa_r2 = pygame.image.load('images/choppa_r1.png'), pygame.image.load('images/choppa_r2.png')
choppa_right = [choppa_r1, choppa_r2]
choppa_left = [choppa_l1, choppa_l2]
choices_left = ['jet_l.png','ship_l.png','choppa_l1.png']
choices_right = ['jet_r.png','ship_r.png','choppa_r1.png']

# Fuel image
fuel = pygame.image.load("images/fuel.png")

# Bullets image
bullet = pygame.image.load("images/bullet.png")

# Bridge image
bridge_image = pygame.image.load("images/bridge.png")

### Variables
# Scroll speed maximum and minimum speeds
MAX_SPEED = 5
MIN_SPEED = 2

# Bullets initializer
bullets = []

# Main loop controller
start = True

# Intro controller
intro = True

# Plane atributes
width = plane.get_width()
height = plane.get_height()
vel = 4
left = False
right = False
lost_life = False

# Plane position in x axis , starting at the middle of screen
plane_x = 350 - (int(width/2))
plane_y = 420

# Fuel indicator position in x axis
fuel_x = 437

# Player hitbox
player_hitbox = pygame.Rect(plane_x, plane_y, plane.get_width()-2,plane.get_height())

### Camera scrolling
up_pressed= False
down_pressed = False
scroll_speed = 1

### Functions
## ======================================================= Enemy functions =======================================================

def generate_enemies(number,off,max_x=405,min_x=145):
    #Returns a list of lists, each being an enemy with: [0] = list of x,y coords, [1] = direction, [2] = enemy type
    enemies_list = []
    for i in range(number):
        tmp = []
        if not off:
            gen_y = random.randint(0,200)
            gen_x = random.randint(min_x,max_x)
            aux = (gen_x,gen_y)
            for enemy in enemies_list:
                while gen_y in range(enemy[0][1]-30, enemy[0][1]+40):
                    gen_y = random.randint(0,200)
            while pygame.Rect(gen_x,gen_y, 64,32).collidelist(curr_rects) != -1 or pygame.Rect(gen_x,gen_y, 64,32).collidelist(curr_rects_off) != -1:
                gen_x = random.randint(0,704)
            aux = (gen_x,gen_y)
            tmp.append(list(aux))   
        elif off:
            gen_y = random.randint(-400,0)
            gen_x = random.randint(min_x,max_x)
            aux = (gen_x,gen_y)
            for enemy in enemies_list:
                while gen_y in range(enemy[0][1]-30,enemy[0][1]+40):
                    gen_y = random.randint(-400,0)
            while pygame.Rect(gen_x,gen_y, 64,32).collidelist(curr_rects) != -1 or pygame.Rect(gen_x,gen_y, 64,32).collidelist(curr_rects_off) != -1:
                gen_x = random.randint(0,704)
            aux = (gen_x,gen_y)
            tmp.append(list(aux))
        tmp.append(random.choice([1,0, -1]))
        if tmp[1] == 1 or tmp[1] == 0:
            #load sprite acording to direction
            tmp.append(random.choice(choices_right))
        elif tmp[1] == -1:
            #load sprite acording to direction
            tmp.append(random.choice(choices_left))
        enemies_list.append(tmp)
    return enemies_list

def draw_enemies(enemies_list):
    #Blits the enemies on screen
    for enemy in enemies_list:
        if not enemy[2][:6] == "choppa":
            screen.blit(pygame.image.load('images/'+enemy[2]), enemy[0])
        #handles the heli animation
        elif enemy[2] == "choppa_l1.png":
            screen.blit(choppa_left[frame], enemy[0])
        elif enemy[2] == "choppa_r1.png":
            screen.blit(choppa_right[frame], enemy[0])

def check_collision(enemies_list):
    #Checks if player hitbox collides with bridges/enemies
     for enemy in enemies_list:
        enemy_rect = [enemy[0][0],enemy[0][1]-1,pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height()+1]
        pygame.display.update()
        if player_hitbox.colliderect(enemy_rect):
            enemy_explosion.play()
            return True
     if len(bridge) != 0:
        for i in bridge:
            if player_hitbox.colliderect(i):
                enemy_explosion.play()
                return True

def move_enemies():
    #Moves enemies acording to random direction generated and handles wall collision
    for enemy in enemies_start:
        enemy_rect = pygame.Rect(enemy[0][0],enemy[0][1],pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height())
        for rect in curr_rects:
            if enemy_rect.colliderect(rect):
                enemy[1]*=-1
                if "r" in enemy[2]:
                    enemy[2] = enemy[2].replace("r","l")
                elif "l" in enemy[2]:
                    enemy[2] = enemy[2].replace("l","r")
        for rect in curr_rects_off:
            if enemy_rect.colliderect(rect):
                enemy[1]*=-1
                if "r" in enemy[2]:
                    enemy[2] = enemy[2].replace("r","l")
                elif "l" in enemy[2]:
                    enemy[2] = enemy[2].replace("l","r")
        enemy[0][1] += scroll_speed
        enemy[0][0] += enemy[1]*1
    for enemy in enemies_start_off:
        enemy_rect = pygame.Rect(enemy[0][0],enemy[0][1],pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height())
        for rect in curr_rects:
            if enemy_rect.colliderect(rect):
                enemy[1]*=-1
                if "r" in enemy[2]:
                    enemy[2] = enemy[2].replace("r","l")
                elif "l" in enemy[2]:
                    enemy[2] = enemy[2].replace("l","r")
        for rect in curr_rects_off:
            if enemy_rect.colliderect(rect):
                enemy[1]*=-1
                if "r" in enemy[2]:
                    enemy[2] = enemy[2].replace("r","l")
                elif "l" in enemy[2]:
                    enemy[2] = enemy[2].replace("l","r")
        enemy[0][1] += scroll_speed
        enemy[0][0] += enemy[1]*1

##======================================================= Fuel functions =======================================================
        
def generate_fuel(number,off,max_x=704,min_x=0):
    # Returns a list of lists, each being a [x,y] list of fuel coordinates, randomly generated
    fuel_list = []
    for i in range(number):
        tmp = []
        if not off:
            aux = [random.randint(min_x,max_x), random.randint(0,200)]

            while pygame.Rect(aux[0],aux[1],pygame.image.load("images/fuel.png").get_width(), pygame.image.load("images/fuel.png").get_height()).collidelist(curr_rects) != -1 or pygame.Rect(aux[0],aux[1],pygame.image.load("images/fuel.png").get_width(), pygame.image.load("images/fuel.png").get_height()).collidelist(curr_rects_off) != -1:
                aux[0] = random.randint(min_x,max_x)
            tmp.append(aux)
        elif off:
            aux = [random.randint(min_x,max_x), random.randint(-400,0)]
            while pygame.Rect(aux[0],aux[1],pygame.image.load("images/fuel.png").get_width(), pygame.image.load("images/fuel.png").get_height()).collidelist(curr_rects) != -1 or pygame.Rect(aux[0],aux[1],pygame.image.load("images/fuel.png").get_width(), pygame.image.load("images/fuel.png").get_height()).collidelist(curr_rects_off) != -1:
                aux[0] = random.randint(min_x,max_x)
            tmp.append(aux)
        fuel_list.append(tmp)
    return fuel_list

def draw_move_fuel(fuel_list):
    # Moves fuel vertically
    for galoon in fuel_list:
        screen.blit(pygame.image.load("images/fuel.png"), (galoon[0][0],galoon[0][1]))
        galoon[0][1] += scroll_speed

def check_fuel():
    # Checks if fuel tank is empty
    global fuel_x
    return fuel_x < 254


                
def collision_with_fuel(fuel_list):
    global fuel_x
    i = 0
    for galoon in fuel_list:
            galoon_rect = [galoon[0][0],galoon[0][1]-1,pygame.image.load("images/fuel.png").get_width(),pygame.image.load("images/fuel.png").get_height()+1]
            if player_hitbox.colliderect(galoon_rect) and fuel_x < 437:
                fuel_x += 0.9
                refuel.play()
            elif player_hitbox.colliderect(galoon_rect) and fuel_x >= 437:
                refuel_full.play()

            

# ================================================ Bullets functions =================================       

def bullet_isonscreen(curr):
    # Checks if bullets coords are on screen
    return curr[1] <= screen_height and curr[1] >= 0

def shoot():
    # Shoot bullet
    global space_pressed
    bullets.append([plane_x+(width/2)-3, 420])

def move_draw_bullets():
    # Move bullets vertically
    for i in bullets:
        screen.blit(pygame.image.load("images/bullet.png"), (i[0], i[1]))
        if not up_pressed:
            i[1] -= 15
        else:
            i[1] -= 20-scroll_speed
        if not bullet_isonscreen(i):
            bullets.pop(bullets.index(i))

def bullet_collision():
    # Checks collision with fuel, walls and enemies
    global score
    global first_bridge
    removed = False
    for bullet in bullets:
        for enemy in enemies_start:
            enemy_rect = [enemy[0][0],enemy[0][1]-1,pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height()+1]
            bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
            if bullet_rect.colliderect(enemy_rect):
                score += 30
                bullets.remove(bullet)
                enemy_explosion.play()
                removed = True
                enemies_start.remove(enemy)
        for enemy in enemies_start_off:
            enemy_rect = [enemy[0][0],enemy[0][1]-1,pygame.image.load('images/'+enemy[2]).get_width(),pygame.image.load('images/'+enemy[2]).get_height()+1]
            bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
            if bullet_rect.colliderect(enemy_rect) and not removed:
                score +=30
                bullets.remove(bullet)
                enemy_explosion.play()
                removed = True
                enemies_start_off.remove(enemy)
        for galoon in fuel_start:
            galoon_rect = [galoon[0][0],galoon[0][1]-1,pygame.image.load("images/fuel.png").get_width(),pygame.image.load("images/fuel.png").get_height()+1]
            bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
            if bullet_rect.colliderect(galoon_rect)and not removed:
                score += 80
                bullets.remove(bullet)
                enemy_explosion.play()
                removed = True
                fuel_start.remove(galoon)
        for galoon in fuel_start_off:
            galoon_rect = [galoon[0][0],galoon[0][1]-1,pygame.image.load("images/fuel.png").get_width(),pygame.image.load("images/fuel.png").get_height()+1]
            bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
            if bullet_rect.colliderect(galoon_rect) and not removed:
                score += 80
                bullets.remove(bullet)
                enemy_explosion.play()
                removed = True
                fuel_start_off.remove(galoon)
        for rect in curr_rects:
            bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
            if bullet_rect.colliderect(rect) and not removed:
                bullets.remove(bullet)
                removed = True
        for rect in curr_rects_off:
            bullet_rect = pygame.Rect(bullet[0],bullet[1], pygame.image.load("images/bullet.png").get_width(), pygame.image.load("images/bullet.png").get_height())
            if bullet_rect.colliderect(rect) and not removed:
                bullets.remove(bullet)
                removed = True
        for br in bridge:
            if bullet_rect.colliderect(br) and not removed:
                score += 500
                bullets.remove(bullet)
                bridge.remove(br)
                first_bridge = False
                enemy_explosion.play()
                removed = True
                
# ============================================= Scroll ===============================================

def checkScroll():
    global scroll_speed
    if up_pressed and scroll_speed < MAX_SPEED:
        scroll_speed += 1
    elif down_pressed and scroll_speed > 1:
        scroll_speed -= 1
    else:
        if scroll_speed > MIN_SPEED:
            scroll_speed -= 1
        elif scroll_speed < MIN_SPEED:
            scroll_speed += 1

# ============================================= Map generator ===============================================
            
def generate_map(start=False):
    if start:
        return iter(['map/map1/1.png','map/map1/2.png','map/map1/2.png','map/map1/2.png','map/map1/3.png'])
    else:
        choice = random.choice([2,2]) #add more maps dirs later
        return iter(['map/map{}/1.png'.format(choice),'map/map{}/2.png'.format(choice),'map/map{}/2.png'.format(choice),'map/map{}/2.png'.format(choice),'map/map{}/3.png'.format(choice)])
    

def reset(start = False):
    global fuel_x
    global first_bridge
    global intro
    global introY
    global plane_x
    global curr_map
    global curr_rects
    global curr_rects_off
    global aux
    global aux2
    global on_screen
    global off_screen
    global bY
    global bY2
    global enemies_start
    global enemies_start_off
    global player_hitbox
    global bridge
    global scroll_speed
    global MAX_SPEED
    global MIN_SPEED

    
    intro = True
    introY = -380
    plane_x = 350 - (int(width/2))
    if first_bridge:
        curr_map = generate_map(True)
        aux = next(curr_map)
        curr_rects = [pygame.Rect(i) for i in rects[aux[7:10]]]
        on_screen = pygame.image.load(aux).convert()
        aux2 = next(curr_map)
        curr_rects_off = [pygame.Rect(i) for i in rects[aux2[7:10]]]
        for rect in curr_rects_off:
            rect.y -= 480
        off_screen = pygame.image.load(aux2).convert()
        enemies_start = generate_enemies(3, False) 
        enemies_start_off = generate_enemies(4, True)
        bY = 0
        bY2 = off_screen.get_height()
    else:
        curr_map = generate_map(False)
        aux = next(curr_map)
        curr_rects = [pygame.Rect(i) for i in rects[aux[7:10]]]
        on_screen = pygame.image.load(aux).convert()
        aux2 = next(curr_map)
        curr_rects_off = [pygame.Rect(i) for i in rects[aux2[7:10]]]
        for rect in curr_rects_off:
            rect.y -= 480
        off_screen = pygame.image.load(aux2).convert()
        enemies_start = generate_enemies(3, False) 
        enemies_start_off = generate_enemies(4, True)
        bY = 0
        bY2 = off_screen.get_height()
    MAX_SPEED = 5
    MIN_SPEED = 2
    scroll_speed = 1
    bridge = []
    redrawWindow()
    fuel_x = 437
    enemies_start = generate_enemies(3, False) 
    enemies_start_off = generate_enemies(4, True)
    fuel_start = generate_fuel(1,False)
    fuel_start_off = generate_fuel(2, True)
    player_hitbox = pygame.Rect(plane_x, plane_y, plane.get_width()-2,plane.get_height())
    

# ============================================= Blitting ===============================================

def redrawWindow():
    # Main blitting function
    global fuel_x
    global text_image
    global lives_text_image
    screen.blit(on_screen, (0,bY))
    screen.blit(off_screen, (0,bY2))
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
    #gray bar
    screen.blit(fuel_bar_bg, (0,480))
    #fuel pointer
    pygame.draw.rect(screen, (252,252,84),pygame.Rect(fuel_x,504,12,49))
    #fuel ammount indicators
    screen.blit(fuel_bar_indicator, (235,500))
    move_draw_bullets()
    bullet_collision()
    if len(bridge) > 0:
        for i in bridge:
            screen.blit(bridge_image, i)
    screen.blit(text_image, (20,515))
    screen.blit(lives_text_image,(560,515))
    text_image = myfont.render("Score: {}".format(score), True, (252,252,84))
    lives_text_image = myfont.render("Lives: {}".format(lives), True, (252,252,84))
    pygame.display.update()

def introduction(start = False):
    global introY
    global text_image
    global lives_text_image
    if start:
        screen.blit(intro_background, (0,introY))
        if introY < 0:
            introY += 2
        else:
            screen.blit(text_image_intro, (190,140))
            screen.blit(text_image_intro_sub, (170,220))
    else:
        screen.blit(intro_background2, (0,introY))    
        if introY < 0:
            introY += 2
        else:
            screen.blit(text_image_intro_sub, (170,220))
    #gray bar
    screen.blit(fuel_bar_bg, (0,480))
    #fuel pointer
    pygame.draw.rect(screen, (252,252,84),pygame.Rect(fuel_x,504,12,49))
    #fuel ammount indicators
    screen.blit(fuel_bar_indicator, (235,500))
    screen.blit(text_image, (20,515))
    screen.blit(lives_text_image,(560,515))
    text_image = myfont.render("Score: {}".format(score), True, (252,252,84))
    lives_text_image = myfont.render("Lives: {}".format(lives), True, (252,252,84))
    pygame.display.update()
    

### Map properties

curr_map = generate_map(True)
aux = next(curr_map)
curr_rects = [pygame.Rect(i) for i in rects[aux[7:10]]]
on_screen = pygame.image.load(aux).convert()
aux2 = next(curr_map)
curr_rects_off = [pygame.Rect(i) for i in rects[aux2[7:10]]]
for rect in curr_rects_off:
    rect.y -= 480
off_screen = pygame.image.load(aux2).convert()
first_bridge = True


### Init bridges list
bridge = []

#generate enemies at start
enemies_start = generate_enemies(3, False) 
enemies_start_off = generate_enemies(4, True)
fuel_start = generate_fuel(1,False)
fuel_start_off = generate_fuel(2, True)

count_end_game = 0

speed = 35

while True:
    if lives <= 0:
        pygame.quit()
        quit()

    time = pygame.time.get_ticks()
    frame = int((time/speed)%len(choppa_right))
    while intro:
        introduction(first_bridge)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and introY == 0:
            print(plane_x)
            intro = False
            redrawWindow()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    time = pygame.time.get_ticks()
    frame = int((time/speed)%len(choppa_right))

    
    redrawWindow()
    checkScroll()

            

    # ======================================== Collisions ==========================================
    if check_collision(enemies_start) or check_collision(enemies_start_off):
        lives-=1
        reset()
        continue
    for rect in curr_rects:
        rect.move_ip(0,scroll_speed)
        if player_hitbox.colliderect(rect):
            lives-=1
            reset()
            continue
    for rect in curr_rects_off:
        rect.move_ip(0,scroll_speed)
        if player_hitbox.colliderect(rect):
            lives-=1
            reset()
            continue
    #no fuel check
    if check_fuel():
        lives-=1
        reset()
        continue
    # =================================== End of collisions ====================================
   

    #move background
    bY += scroll_speed
    bY2 += scroll_speed
    
    if len(bridge) > 0:
        for i in bridge:
            i.move_ip(0,scroll_speed)

    #move fuel pointer
    fuel_x -= 0.125
    
    #handle infinite scroll
    if bY > off_screen.get_height():
        bY = -1*off_screen.get_height()
        start = False
        MIN_SPEED+=1
        MAX_SPEED+=1
        try:
            aux = next(curr_map)
            curr_rects = [pygame.Rect(i) for i in rects[aux[7:10]]]
            for rect in curr_rects:
                rect.y-=480
            on_screen = pygame.image.load(aux).convert()
        except StopIteration:
            del curr_map
            curr_map = generate_map(False)
            aux = next(curr_map)
            curr_rects = [pygame.Rect(i) for i in rects[aux[7:10]]]
            for rect in curr_rects:
                rect.y-=480
            on_screen = pygame.image.load(aux).convert()
        if aux[9] == "3":
            tmp = pygame.Rect(bridges[aux[7:10]])
            tmp.y -= 480
            bridge.append(tmp)
        enemies_start = generate_enemies(4, True)
        fuel_start = generate_fuel(2,True)
        
    if bY2 > off_screen.get_height():
        bY2 = -1*off_screen.get_height()
        try:
            aux2 = next(curr_map)
            curr_rects_off = [pygame.Rect(i) for i in rects[aux2[7:10]]]
            for rect in curr_rects_off:
                rect.y-=480
            off_screen=pygame.image.load(aux2).convert()
        except StopIteration:
            del curr_map
            curr_map = generate_map(False)
            aux2 = next(curr_map)
            curr_rects_off = [pygame.Rect(i) for i in rects[aux2[7:10]]]
            for rect in curr_rects_off:
                rect.y-=480
            off_screen = pygame.image.load(aux2).convert()
        if aux2[9] == "3":
            tmp = pygame.Rect(bridges[aux2[7:10]])
            tmp.y -= 480
            bridge.append(tmp)
        enemies_start_off = generate_enemies(4, True)
        fuel_start_off = generate_fuel(2, True)
 
    #refuel
    collision_with_fuel(fuel_start)
    collision_with_fuel(fuel_start_off)
    
    
    
    # keys handle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if len(bullets) == 0:
            shoot()
            player_shoot.play()
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        left = False
        right = False
    elif keys[pygame.K_LEFT]:
        plane_x -= vel
        player_hitbox.x -= vel
        left = True    
    elif keys[pygame.K_RIGHT]:
        plane_x += vel
        player_hitbox.x += vel 
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
