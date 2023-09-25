import pygame
from sys import exit

pygame.init()

win_width, win_height = 800, 600 

pygame.display.set_caption("JumpeR")
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

#funktionen

def player_animation():
    global player_surf, player_index, attack_index, is_attack_animating      
    #jump
    if player_rect.bottom < 500:
        player_index += 0.15                                 
        if player_index >= len(player_jump):
            player_index = 0
        player_surf = player_jump[int(player_index)]
        

        if direction == 1:
            player_surf = player_jump[int(player_index)]
        else:
            player_surf = pygame.transform.flip(player_jump[int(player_index)], True, False)
    #walk
    elif is_moving_l or is_moving_r:
        player_index += 0.15                                                                    # 0.1 = langsamere animation
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

    #attack                  ###   #to fix: taste muss gedrückt sein für animation, startet nicht mit 1. frame  ###
    elif is_attacking:  
        if not is_attack_animating:
            attack_index = 0
            is_attack_animating = True

        print(attack_index)
        #attack_index += 0.2                          

        # if attack_index >= len(player_attack):
        #     attack_index = 0
        #     is_attack_animating = False

        
        player_surf = player_attack[int(attack_index)]
            
        
        if direction == 1:
            player_surf = player_attack[int(attack_index)]
        else:
            player_surf = pygame.transform.flip(player_attack[int(attack_index)], True, False)
        
    #idle
    else:
        player_index += 0.15                               
        if player_index >= len(player_idle):
            player_index = 0
        player_surf = player_idle[int(player_index)]

        if direction == 1:
            player_surf = player_idle[int(player_index)]
        else:
            player_surf = pygame.transform.flip(player_idle[int(player_index)], True, False)


def enemy_animation():
    global enemy_zombie_index, enemy_zombie_surf, enemy_larva_index, enemy_larva_surf, enemy_wraith_index, enemy_wraith_surf, enemy_evil_eye_index, enemy_evil_eye_surf
    #walk
    #zombie
    enemy_zombie_index += 0.15                                                                    
    if enemy_zombie_index >= len(enemy_zombie_walk):
        enemy_zombie_index = 0
    enemy_zombie_surf = enemy_zombie_walk[int(enemy_zombie_index)]
    
    #larva
    enemy_larva_index += 0.15
    if enemy_larva_index >= len(enemy_larva_walk):
        enemy_larva_index = 0
    enemy_larva_surf = enemy_larva_walk[int(enemy_larva_index)]
    
    #wraith
    enemy_wraith_index += 0.15
    if enemy_wraith_index >= len(enemy_wraith_walk):
        enemy_wraith_index = 0
    enemy_wraith_surf = enemy_wraith_walk[int(enemy_wraith_index)]
    
    #evil eye
    enemy_evil_eye_index += 0.15
    if enemy_evil_eye_index >= len(enemy_evil_eye_walk):
        enemy_evil_eye_index = 0
    enemy_evil_eye_surf = enemy_evil_eye_walk[int(enemy_evil_eye_index)]

def zombie_spawn(): ##ACHTUNG###BAUSTELLE!!!############ACHTUNG###BAUSTELLE!!!###########!!!ACHTUNG###BAUSTELLE!!!#############ACHTUNG#
    global enemy_zombie_surf, enemy_zombie_index, enemy_zombie_spawning, enemy_zombie_spawn

    # #enemy_zombie_index += 0.5                    #sprite klassen
    # for i in range(len(enemy_zombie_spawn)):
        
    #     enemy_zombie_surf = enemy_zombie_spawn[i]
    #     screen.blit(enemy_zombie_surf, enemy_zombie_rect)
    #     pygame.display.flip()
    #     pygame.time.wait(500)
        
        

    # while enemy_zombie_index < 12:
    #     print(enemy_zombie_index)
    #     enemy_zombie_surf = enemy_zombie_spawn[int(enemy_zombie_index)]
    #     screen.blit(enemy_zombie_surf, enemy_zombie_rect)
    #     if enemy_zombie_index > 11.9:
    #         enemy_zombie_spawning = False
    #         print("breakie")
    #         break
    #     enemy_zombie_index += 0.1
    
    # enemy_zombie_spawning = False


    

def draw_bg():
    for x in range(5):    
        scroll_speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * scroll_speed, 0))
            scroll_speed += 0.2                                             #je weiter vorne das bg_image, desto schneller der scroll_speed



class Character(pygame.sprite.Sprite):          #Player und NPCs
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        surface = pygame.image.load("jumper/graphics/assets/crow animations/walk/crow_walk1.png")
        self.surf = pygame.transform.scale2x(surface)
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)


    def draw(self):
        pass

        
player = Character(50, 500, 2)



# player_surf = player_idle[int(player_index)]     ###########
# player_rect = player_surf.get_rect(midbottom = (player_x, player_y))                                                                 #malt rectangle um das surface





#game variables
player_x, player_y = 50, 500

enemy_x, enemy_y = 750, 500

direction = 1           #  1 = right->, 0 = left<-

scroll = 0

gravity = 0
jump_count = 0
max_jumps = 1       #2 = doublejump

is_attacking = False
is_attack_animating = False

is_moving_r = False  
is_moving_l = False
player_speed = 5  
pif = 0                 #Player Invulnerable Frames     3 = 5, 2=4

player_index = 0
attack_index = 0
enemy_zombie_index = 0
enemy_zombie_spawning = False
enemy_larva_index = 0
enemy_wraith_index = 0
enemy_evil_eye_index = 0


bg_images = []
for i in range(1, 4):           #muss 1, 6 sein
    bg_image = pygame.image.load(f"jumper/graphics/assets/haunted forest parallaxing background/background_{i}.png")
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()
 
#player animation 
player_idle = []            
for i in range(1, 4):
    idle = pygame.transform.scale_by(pygame.image.load(f"jumper/graphics/assets/crow animations/idle/crow_idle{i}.png").convert_alpha(), 2)
    player_idle.append(idle)

player_jump = []            
for i in range(1, 6):
    jump = pygame.transform.scale2x(pygame.image.load(f"jumper/graphics/assets/crow animations/jump/crow_jump{i}.png").convert_alpha())
    player_jump.append(jump)
 
player_walk = []                                                                                                                     #animation = for i in player_walk 
for i in range(1, 4):
    walk = pygame.transform.scale2x(pygame.image.load(f"jumper/graphics/assets/crow animations/walk/crow_walk{i}.png").convert_alpha())
    player_walk.append(walk)

player_attack = []            
for i in range(1, 6):
    attack = pygame.transform.scale_by(pygame.image.load(f"jumper/graphics/assets/crow animations/attack/crow_attack{i}.png").convert_alpha(), 2)
    player_attack.append(attack) 

# #alt
# enemy_surf = pygame.transform.scale2x(pygame.image.load("jumper/graphics/assets/cyborg/cyborg_jump.png").convert_alpha())
# enemy_rect = enemy_surf.get_rect(midbottom = (enemy_x, enemy_y))


#enemy animation
#zombie
enemy_zombie_walk = []            
for i in range(1, 4):
    zombie_walk = pygame.transform.flip(pygame.transform.scale2x(pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Zombie/zombie_walk{i}.png").convert_alpha()), True, False)
    enemy_zombie_walk.append(zombie_walk)

enemy_zombie_surf = enemy_zombie_walk[int(enemy_zombie_index)]
enemy_zombie_rect = enemy_zombie_surf.get_rect(midbottom = (enemy_x, enemy_y))

#zombie spawn
enemy_zombie_spawn = []
for i in range(1, 13):
    zombie_uprise = pygame.transform.flip(pygame.transform.scale2x(pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Zombie/zombie_Uprise{i}.png").convert_alpha()), True, False)
    enemy_zombie_spawn.append(zombie_uprise)

#larva
enemy_larva_walk = []            
for i in range(1, 5):
    larva_walk = pygame.transform.flip(pygame.transform.scale2x(pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Larva/larva_walk{i}.png").convert_alpha()), True, False)
    enemy_larva_walk.append(larva_walk)

enemy_larva_surf = enemy_larva_walk[int(enemy_larva_index)]
enemy_larva_rect = enemy_larva_surf.get_rect(midbottom = (enemy_x, enemy_y))

#wraith
enemy_wraith_walk = []            
for i in range(1, 4):
    wraith_walk = pygame.transform.flip(pygame.transform.scale2x(pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Wraith/wraith_walk{i}.png").convert_alpha()), True, False)
    enemy_wraith_walk.append(wraith_walk)

enemy_wraith_surf = enemy_wraith_walk[int(enemy_wraith_index)]
enemy_wraith_rect = enemy_wraith_surf.get_rect(midbottom = (enemy_x, enemy_y))

#evil eye beast
enemy_evil_eye_walk = []            
for i in range(1, 21):
    evil_eye_walk = pygame.transform.scale2x(pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Evil Eye Beast/Idle/Eye Beast Idle{i}.png").convert_alpha())
    enemy_evil_eye_walk.append(evil_eye_walk)

enemy_evil_eye_surf = enemy_evil_eye_walk[int(enemy_evil_eye_index)]
enemy_evil_eye_rect = enemy_evil_eye_surf.get_rect(midbottom = (enemy_x, enemy_y))


#################################################################################################################################################

while True:
    clock.tick(60)
    
    #background
    draw_bg()


    #Player
    screen.blit(player_surf, player_rect)   
    gravity += 1
    player_rect.y += gravity
    if player_rect.bottom > 500: 
        player_rect.bottom = 500
        gravity = 0
        jump_count = 0 
    

    #bg_scroll      
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    if key[pygame.K_RIGHT]:
        scroll += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Movement                               ##
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jump_count < max_jumps:
                    gravity = -20
                    jump_count += 1

                    
            elif event.key == pygame.K_e:
                is_attacking = True

            elif event.key == pygame.K_RIGHT:           
                is_moving_r = True
                direction = 1
                

            elif event.key == pygame.K_LEFT:            
                is_moving_l = True
                direction = 0

        

        #alte version mit KEYUP statt .get_pressed()
        # elif event.type == pygame.KEYUP:
        #     if event.key == pygame.K_RIGHT:
        #         is_moving_r = False
        #     elif event.key == pygame.K_LEFT:
        #         is_moving_l = False
    


    # if not pygame.key.get_pressed()[pygame.K_e]:
    #     is_attacking = False

    # # Wenn die Angriffsanimation aktiviert ist, erhöhe attack_index, bis sie abgeschlossen ist
    # if is_attack_animating:
    #     attack_index += 0.2

    #     if attack_index >= len(player_attack):
    #         attack_index = 0
    #         is_attack_animating = False


    ###
    if not pygame.key.get_pressed()[pygame.K_e]:
        is_attacking = False

    if is_attack_animating:
        attack_index += 0.2

        if attack_index >= len(player_attack):
            attack_index = 0
            is_attack_animating = False

    
    if not pygame.key.get_pressed()[pygame.K_RIGHT]:
        is_moving_r = False

    if not pygame.key.get_pressed()[pygame.K_LEFT]:
        is_moving_l = False

    if is_moving_r:
        player_rect.x += player_speed

    if is_moving_l:
        player_surf = pygame.transform.flip(player_surf, True, False)                  
        player_rect.x -= player_speed
        if player_rect.bottom < 500:                                                    #bugfix
            player_surf = pygame.transform.flip(player_surf, True, False)                  

    if is_moving_l and is_moving_r:                                                     #wenn beide pfeiltasten gleichzeitig gedrückt werden
        if direction == 0:
            player_surf = player_idle[int(player_index % len(player_idle))]
        else:
            player_surf = player_idle[int(player_index % len(player_idle))]         # % verhindert list index error



    # #collision
    # if player_rect.colliderect(enemy_rect):
    #     if pif == 0:
    #         print("CRASH")
    #         pif = 20
    #     else:
    #         pif -= 1

    #print(player_index)

    #Enemy  
    #Zombie
    if not enemy_zombie_spawning:
        screen.blit(enemy_zombie_surf, enemy_zombie_rect)
        enemy_zombie_rect.x -= 1.1
        if enemy_zombie_rect.x < 0: 
            enemy_zombie_rect.x = 800
    
    #if abs(enemy_zombie_rect.x - player_rect.x) < 250:              #wenn spieler sich dem gegner nähert
        #zombie spawn
     #   enemy_zombie_spawning = True
        #zombie_spawn()
    
    #larva
    screen.blit(enemy_larva_surf, enemy_larva_rect)
    enemy_larva_rect.x -= 2
    if enemy_larva_rect.x < 0: 
        enemy_larva_rect.x = 800
    
    #wraith
    screen.blit(enemy_wraith_surf, enemy_wraith_rect)
    enemy_wraith_rect.x -= 3
    if enemy_wraith_rect.x < 0: 
        enemy_wraith_rect.x = 800
    
    #evil eye               #1. boss?
    screen.blit(enemy_evil_eye_surf, (enemy_wraith_rect.y + 200, 300))
    #enemy_evil_eye_rect.x -= 2
    #if enemy_evil_eye_rect.x < 0: s
    #    enemy_evil_eye_rect.x = 800
    



    player_animation()

    enemy_animation()
    
    pygame.display.update()


    