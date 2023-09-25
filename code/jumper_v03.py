import pygame
from sys import exit
from settings import *
from level import Level
from game_data import level_0

#to do:
#movement
    ##wenn beide pfeiltasten gleichzeitig gedrückt werden
    #attack jump
    #wenn pfeiltaste nach attack noch gedrückt wird, weiterlaufen?
    #E gedrückt halten und laufen
#animation
    #198 jump animation in klasse ingetriegen
    #death and get hit animation
    #attack animation, wenn spieler nach links guckt (lösung evtl im pdf?)
    #347 zombie verschwindet, wenn spieler sich während spawn animation entfernt
#tile types? brauch ich die?

#obstacle list nur ground, nicht deko

#moving_r, moving_l in character class impl




pygame.init()

# win_width = 800         kommt von settings.py
# win_height = 600
pygame.display.set_caption("JumpeR")
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()


#Game Variables
jump_count = 0
max_jumps = 1
gravity = 0
scroll = 0

moving_l = False            #todo: impl in char class
moving_r = False

#is_attacking = False           == self.attack
attack_count = 0


rows = 16           #aka vertical tile number
cols = 150

scroll_counter = 0

level = Level(level_0, screen)             

TILE_SIZE = win_height // rows
#tile_types = ? 
#store tile in a list
tile_types = [] ############# ??


        
def draw_bg():
    screen.blit(pygame.transform.scale_by(pygame.image.load("jumper/graphics/assets/the dark forest/Background/Night.png"), 3), (0,0))

class Character(pygame.sprite.Sprite):                                                                      #Player und NPCs (vllt trennen?)
    def __init__(self, x, y, speed, can_jump):
        pygame.sprite.Sprite.__init__(self)
        self.living = True       #für später 
        self.can_jump = can_jump
        self.speed = speed
        self.direction = 1                                                                                      # -1 = links, 1 = rechts
        self.vel_y = 0
        self.jump = False
        self.attack = False             #is_attacking für animation?
        #self.is_attacking = False       
        self.attack_frame = 0
        self.flip = False
        self.animation_list = []                                                    #eine liste aus mehreren listen, die die animationen enthalten
        self.frame_index = 0
        self.action = 0                                                                                         #1=idle, 0=run
        self.update_time = pygame.time.get_ticks()
        self.spawned = False                        #zombie spawned
        
        
        
        #animation
        temp_list = []                               #action 0 walk
        for i in range(4):
            surface = pygame.image.load(f"jumper/graphics/assets/crow animations/walk/crow_walk{i+1}.png")        
            surface = pygame.transform.scale_by(surface, 2)
            temp_list.append(surface)
        self.animation_list.append(temp_list)

        temp_list = []                              #action 1 player idle
        for i in range(4):
            surface = pygame.image.load(f"jumper/graphics/assets/crow animations/idle/crow_idle{i+1}.png")      
            surface = pygame.transform.scale_by(surface, 2)
            temp_list.append(surface)
        self.animation_list.append(temp_list)

        temp_list = []                              #action 2 player attack
        for i in range(5):
            surface = pygame.image.load(f"jumper/graphics/assets/crow animations/attack/crow_attack{i+1}.png")      
            surface = pygame.transform.scale_by(surface, 2)
            temp_list.append(surface)
        self.animation_list.append(temp_list)

        temp_list = []                              #action 3 zombie uprise
        for i in range(12):            
            surface = pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Zombie/uprise/zombie_Uprise{i+1}.png")      
            surface = pygame.transform.scale_by(surface, 2)
            temp_list.append(surface)
        self.animation_list.append(temp_list)

        temp_list = []                              #action 4 zombie walk
        for i in range(3):            
            surface = pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Zombie/walk/zombie_walk{i+1}.png")      
            surface = pygame.transform.scale_by(surface, 2)
            temp_list.append(surface)
        self.animation_list.append(temp_list)

        temp_list = []                              #action 5 zombie attack
        for i in range(7):            
            surface = pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Zombie/attack/zombie_attack{i+1}.png")      
            surface = pygame.transform.scale_by(surface, 2)
            temp_list.append(surface)
        self.animation_list.append(temp_list)

        # temp_list = []                              #action 6 larva walk
        # for i in range(4):            
        #     surface = pygame.image.load(f"jumper/graphics/assets/Pale Moon/Creatures/Larva/walk/larva_walk{i+1}.png")      
        #     surface = pygame.transform.scale_by(surface, 2)
        #     temp_list.append(surface)
        # self.animation_list.append(temp_list)

        self.surf = self.animation_list[self.action][self.frame_index]
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
    
    def move(self, moving_l, moving_r):
        global gravity, jump_count
        
        #reset movement variables   #also used for collision detection
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

        #update rect position
        self.rect.x += dx
        self.rect.y += dy 

        #check collision                                ##########################################
        for tile in level.obstacle_list:
            pass
            #check x
        if self.rect.bottom + dy > 352:
            dy = 352 - self.rect.bottom

    
    def attacking(self):                
        
        if self.attack: 
            self.action = 2
            if self.attack_frame > 4:       #len(animation frames)
                self.attack_frame += 1       #Increment attack animation frame
                #print(self.attack_frame)
                self.attack = False
                
            #self.attack_frame += 1

            #print(self.frame_index, len(self.animation_list[self.action]), self.attack)

            # if self.attack_frame >= len(self.animation_list[self.action]) -1:# and self.attack == True:
            #     self.attack = False
            #     self.attack_frame = 0

                
        # if is_attacking:
        #     attack_index += attack_animation_speed
        #     if attack_index >= len(self.animation_list[self.action][self.frame_index]):
        #         attack_index = 0
        #         is_attacking = False


    def update_animation(self):
        #error handling
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = len(self.animation_list[self.action]) - 1

        #validate action 
        if self.action >= len(self.animation_list):
            print("Invalid action")
            

        #validate frame index
        #print(self.frame_index, "///", len(self.animation_list[self.action]), self.can_jump)
        if self.frame_index >= len(self.animation_list[self.action]):
            print("Invalid frame index") 
            
        
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
        
        #jump animation seperat, weil nicht linear
        if self.can_jump:
            if gravity < 0:         
                self.surf = crow_jump[1] 
            if gravity > 0:
                self.surf = crow_jump[3]
                    
        # Handle attack separately
        if self.attack:
            self.attacking()
            
            
                    
    def update_action(self, new_action):        #walking or idling or attacking
        #check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.surf, self.flip, False), self.rect)

    


    def spawn(self):        #zombie
        #print("inside spawn method")
        if not self.spawned:
            #print("inside if not self.spawned")
            self.action = 3     #action 3 = spawn
            self.update_animation()
            #print(self.frame_index, "/", len(self.animation_list[self.action]), "action:", self.action)
            if self.frame_index >= len(self.animation_list[self.action]) -1:
                self.spawned = True 
                print("spawn hat geklappt, action:", self.action)
                self.action = 4     #transistion to walk animation
                self.frame_index = 0
                print("walking, action:", self.action)        

    def scroll_x(self):
        global scroll_counter
          
        if player.rect.x > 550 and moving_r and player.direction == 1:          #maybe make responsive with win_width - (win_width / 4) statt festen wert
            player.speed = 0
            level.world_shift = -4
            scroll_counter += 1
            
        
        elif player.rect.x < 50 and moving_l and player.direction == -1:
            player.speed = 0
            level.world_shift = 4
            scroll_counter -= 1
            
        
        else:
            level.world_shift = 0
            player.speed = 5
            
        
            



#jump animation #todo: in klasse integriegen
crow_jump = []
for i in range(6):
    surface = pygame.image.load(f"jumper/graphics/assets/crow animations/jump/crow_jump{i+1}.png")
    surface = pygame.transform.scale_by(surface, 2)
    crow_jump.append(surface)


player = Character(150, 352, 5, True)
#larva01 = Character(400, 264, 4, False)
zombie01 = Character(600, 264, 4, False)


######################################################################################
    
while True:
    
    clock.tick(60)

    #background
    draw_bg()

    level.run()            
    player.scroll_x()
    

    

    #player Jump
    #if player.jump:
    gravity += 1
    player.rect.y += gravity
    if player.rect.bottom > 352:
        player.rect.bottom = 352
        gravity = 0
        jump_count = 0


    # #    LARVA
    
    # # if abs(larva01.rect.x - player.rect.x) < 100:
    # # print("L:", larva01.rect.x)
    # larva01.action = 6
    # larva01.update_animation()
    # larva01.draw()
    # if player.rect.x <= larva01.rect.x:
    #     larva01.flip = True
    #     larva01.rect.x -= 3
    # elif player.rect.x >= larva01.rect.x:
    #     larva01.flip = False
    #     larva01.rect.x += 3


###############################################################################################


    #ZOMBIE
    #zombie spawn
    #if abs(zombie01.rect.x - player.rect.x) < 20 and not zombie01.spawned:
    #    print("zombie spawn")
        #if not zombie01.spawned:
    
    #print(zombie01.spawned)
    #zombie01.spawn()                    ################
    #zombie walk
    # collide = pygame.Rect.colliderect(player.rect, zombie01.rect)       #sprite group für collision?
    # if collide:
    #     print(collide, "COLLIDE")

    


    #zombie01.flip = True
    #if not zombie01.spawned:

    #print(abs(zombie01.rect.x - player.rect.x))

    
    if scroll_counter > 100:
        #print("scroooooooool")


        if abs(zombie01.rect.x - player.rect.x) < 100 and not zombie01.spawned:             #todo: wenn player sich während spawn animation entfernt
            zombie01.spawn()
            zombie01.draw()

        elif not zombie01.spawned:
            print("zombie spawn srenrjjjenruneurneur")
            zombie01.spawned = True


        elif abs(zombie01.rect.x - player.rect.x) < 30:
            zombie01.action = 5         #attack
            zombie01.update_animation()
            zombie01.draw()
        
        elif abs(zombie01.rect.x - player.rect.x) > 30 and zombie01.spawned:           
            zombie01.action = 4            #walk
            zombie01.update_animation()
            zombie01.draw()

        #print(zombie01.frame_index, "/", len(zombie01.animation_list[zombie01.action]), "action:", zombie01.action) 

        if zombie01.spawned and zombie01.action != 5:
            zombie01.action = 4       #walk
            zombie01.update_animation()
            zombie01.draw()
            zombie01.rect.x -= 1

        if zombie01.rect.x > player.rect.x:     #follow the player
            zombie01.flip = True
            if zombie01.spawned:
                zombie01.rect.x -= 1    

        if zombie01.rect.x < player.rect.x:     
            zombie01.flip = False
            if zombie01.spawned:
                zombie01.rect.x += 3    

    # elif zombie01.rect.x < player.rect.x:
    #     print("FLIP")
    #     zombie01.flip = False
    #     zombie01.rect.x += 3


    # if zombie01.living and not zombie01.spawned:
    #     zombie01.update_action(3)           #3 = uprise
    #     zombie01.spawn()

    # elif zombie01.living and zombie01.spawned and zombie01.attack:
    #     zombie01.update_action(5)          #5 = attack  
    #                                         
    # else:
    #     zombie01.update_action(4)           #4 = walk


###############################################################################################

    
    print("P:", player.rect.x, "Z:", zombie01.rect.x, "diff:", abs(zombie01.rect.x - player.rect.x), "scroll:", scroll_counter)


    
    
    #PLAYER
	# Player related functions
    if player.attack == True:
        player.attacking() 
    player.update_animation()
    player.draw()


    #update player actions  
    if player.living:
        if moving_l or moving_r:
            player.update_action(0)     #0 = run
        elif player.attack:
            player.update_action(2)     #2 = attack
        else:
            player.update_action(1)     #1 = idle   #todo: 


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

            if event.key == pygame.K_e:
                if player.attack == False:
                    #if attack_count < 1:
                    moving_l = False
                    moving_r = False
                    player.attack = True
                    # Reset attack animation            ######BAUSTELLE#####
                    player.frame_index = 0
                    player.attacking()
                    player.attack = True
                
        

            if event.key == pygame.K_SPACE and player.living:
                if jump_count < max_jumps:
                    gravity = -20
                    jump_count += 1


            # if event.key == pygame.K_LEFT and pygame.K_RIGHT:
    
    if not pygame.key.get_pressed()[pygame.K_RIGHT]:
        moving_r = False

    if not pygame.key.get_pressed()[pygame.K_LEFT]:
        moving_l = False
                
    if not pygame.key.get_pressed()[pygame.K_e]:
        player.attack = False





    # if pygame.key.get_pressed()[pygame.K_RIGHT] and pygame.key.get_pressed()[pygame.K_LEFT]:
    #     moving_l = False
    #     moving_r = False
    #     if not pygame.key.get_pressed()[pygame.K_RIGHT]:
    #         moving_l = True
    #     if not pygame.key.get_pressed()[pygame.K_LEFT]:
    #         moving_r = True


    # if is_moving_l and is_moving_r:                                                     #wenn beide pfeiltasten gleichzeitig gedrückt werden
    #     if direction == 0:
    #         player_surf = player_idle[int(player_index % len(player_idle))]
    #     else:
    #         player_surf = player_idle[int(player_index % len(player_idle))]         # % verhindert list index error

    
    pygame.display.update()

pygame.quit()