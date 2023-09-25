import pygame
import random
from sys import exit

pygame.init()

win_width, win_height = 800, 600        #x, y

pygame.display.set_caption("JumpeR")
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()


#Game Variables
jump_count = 0
max_jumps = 1
gravity = 0
scroll = 0

moving_l = False
moving_r = False


def spawn_enemy(player, enemies):
    # Definiere den Bereich, in dem der Gegner spawnen kann (horizontal)
    spawn_distance = 500

    # Überprüfe, ob der Spieler sich in der Nähe des letzten gespawnten Gegners befindet
    if not enemies or abs(player.rect.x - enemies[-1].rect.x) > spawn_distance:
        # Bestimme die möglichen Spawn-Positionen basierend auf der Spielerposition
        min_x = player.rect.x + spawn_distance
        max_x = player.rect.x + spawn_distance + 100
        spawn_x = random.randint(min_x, max_x)

        # Der Y-Wert des Spawnpunkts ist der Boden der Ebene
        spawn_y = 548

        # Erstelle den neuen Gegner und füge ihn der Liste der Gegner hinzu
        new_enemy = Character(spawn_x, spawn_y, 4)  # Ändere die Parameter für den Gegner nach Bedarf
        enemies.append(new_enemy)

        
def draw_bg():
    screen.blit(pygame.transform.scale_by(pygame.image.load("jumper/graphics/assets/the dark forest/Background/Night.png"), 3), (0,0))

class Character(pygame.sprite.Sprite):                                                                      #Player und NPCs
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.living = True   
        self.speed = speed
        self.direction = 1                                                                                      # -1 = links, 1 = rechts
        self.vel_y = 0
        self.jump = False
        self.flip = False
        self.animation_list = []                                                    #eine liste aus mehreren listen, die die animationen enthalten
        self.frame_index = 0
        self.action = 0                                                                                         #1=idle, 0=run
        self.update_time = pygame.time.get_ticks()

        temp_list = []                                                                                              #animation
        for i in range(4):
            surface = pygame.image.load(f"jumper/graphics/assets/crow animations/walk/crow_walk{i+1}.png")        
            surface = pygame.transform.scale_by(surface, 2)
            temp_list.append(surface)
        self.animation_list.append(temp_list)

        temp_list = []
        for i in range(4):
            surface = pygame.image.load(f"jumper/graphics/assets/crow animations/idle/crow_idle{i+1}.png")      
            surface = pygame.transform.scale_by(surface, 2)
            temp_list.append(surface)
        self.animation_list.append(temp_list)

        self.surf = self.animation_list[self.action][self.frame_index]
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
    
    def move(self, moving_l, moving_r):
        global gravity
        #reset movement variables
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_l:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_r:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # #jumping
        # if self.jump:
        #     gravity += 1

        # #apply gravity
        # self.vel_y += gravity
        # dy += self.vel_y
        
        # #player.rect.y += gravity
        # if self.rect.bottom > 548: 
        #     self.rect.bottom = 548
        #     self.vel_y = 0
        #     self.jump = False

        # #jump
        # if self.jump:
        #     if self.rect.bottom == 548:
        #         self.vel_y = -20
        #         self.jump = False
        #         #jump_count = 0 
        # #dy += self.vel_y 

        #update rect position
        self.rect.x += dx
        self.rect.y += dy 

        # #apply gravity
        # self.vel_y += GRAVITY
        # if self.vel_y > 10:
        #     self.vel_y = 10
        
        # #check collision with floor
        # if self.rect.bottom + dy > 548:
        #     dy = 548 - self.rect.bottom

    def update_animation(self):
        #update animation
        ANIMATION_SPEED = 100
        #update image depending on current frame
        self.surf = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_SPEED:
            self.update_time = pygame.time.get_ticks()                      #reset timer
            self.frame_index += 1
        #if animation has run out, reset to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
        # jump_mitte = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        # if gravity != 0:
            
        #     if gravity in jump_mitte:
        #         self.surf = crow_jump[2]
        #     else:
        #jump animation seperat, weil nicht linear
        if gravity < 0:         
            self.surf = crow_jump[1] 
        if gravity > 0:
            self.surf = crow_jump[3]
                    
            
            

    def update_action(self, new_action):        #walking or idling
        #check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.surf, self.flip, False), self.rect)
        
#jump animation 
crow_jump = []
for i in range(6):
    surface = pygame.image.load(f"jumper/graphics/assets/crow animations/jump/crow_jump{i+1}.png")
    surface = pygame.transform.scale_by(surface, 2)
    crow_jump.append(surface)




enemies = []

player = Character(150, 548, 5)
#enemy = Character(500, 350, 4)

# player_walk = []                                                                                                                     
# for i in range(1, 4):
#     walk = pygame.transform.scale2x(pygame.image.load(f"jumper/graphics/assets/crow animations/walk/crow_walk{i}.png").convert_alpha())
#     player_walk.append(walk)


# bg_images = []
# for i in range(1, 4):           #muss 1, 6 sein
#     bg_image = pygame.image.load(f"jumper/graphics/assets/haunted forest parallaxing background/background_{i}.png")
#     bg_images.append(bg_image)

# bg_width = bg_images[0].get_width()


while True:
    
    clock.tick(60)

    #background
    draw_bg()

    #player Jump
    #if player.jump:
    gravity += 1
    player.rect.y += gravity
    if player.rect.bottom > 548:
        player.rect.bottom = 548
        gravity = 0
        jump_count = 0



   



    #player
    player.update_animation()
    player.draw()


    #enemy
    # Rufe die Funktion zum Spawne des Gegners auf
    spawn_enemy(player, enemies)

    for enemy in enemies:
        #enemy.move(False, True)  # Hier kannst du festlegen, in welche Richtung die Gegner gehen sollen
        enemy.update_animation()
        enemy.draw()

    #update player actions
    if player.living:
        if moving_l or moving_r:
            player.update_action(0)     #0 = run
        else:
            player.update_action(1)     #1 = idle

    player.move(moving_l, moving_r)


    #Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Movement                               ##
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_SPACE:
            #     if jump_count < max_jumps:
            #         gravity = -20
            #         jump_count += 1
            # elif event.key == pygame.K_e:
            #     is_attacking = True

            if event.key == pygame.K_ESCAPE:           
                pygame.quit()
                exit()

            if event.key == pygame.K_RIGHT:           
                moving_r = True
                player.direction = 1
                
            if event.key == pygame.K_LEFT:            
                moving_l = True
                player.direction = -1

            if event.key == pygame.K_SPACE and player.living:
                if jump_count < max_jumps:
                    gravity = -20
                    jump_count += 1
                
                # gravity += 1 
                # player.rect.y += gravity
                # if player.rect.bottom > 548:
                #     player.rect.bottom = 548
                #     gravity = 0

                    

    print(gravity)
    if gravity > 0:
        print("DOWN")

            # if event.key == pygame.K_LEFT and pygame.K_RIGHT:


    # if pygame.key.get_pressed()[pygame.K_RIGHT] and pygame.key.get_pressed()[pygame.K_LEFT]:
    #     moving_l = False
    #     moving_r = False
    #     if not pygame.key.get_pressed()[pygame.K_RIGHT]:
    #         moving_l = True
    #     if not pygame.key.get_pressed()[pygame.K_LEFT]:
    #         moving_r = True

    
    if not pygame.key.get_pressed()[pygame.K_RIGHT]:
        moving_r = False

    if not pygame.key.get_pressed()[pygame.K_LEFT]:
        moving_l = False
                

    # if is_moving_l and is_moving_r:                                                     #wenn beide pfeiltasten gleichzeitig gedrückt werden
    #     if direction == 0:
    #         player_surf = player_idle[int(player_index % len(player_idle))]
    #     else:
    #         player_surf = player_idle[int(player_index % len(player_idle))]         # % verhindert list index error

    ### Attack
    #if not pygame.key.get_pressed()[pygame.K_e]:
    #     is_attacking = False

    # if is_attack_animating:
    #     attack_index += 0.2

    #     if attack_index >= len(player_attack):
    #         attack_index = 0
    #         is_attack_animating = False




    
    
    
    
    pygame.display.update()

pygame.quit()