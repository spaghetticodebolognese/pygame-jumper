import pygame
from pygame.locals import *

#### scheißcode von chatgpt

# Initialisierung von Pygame
pygame.init()

# Definiere die Fenstergröße
window_width = 800
window_height = 600

# Erstelle das Fenster
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('JumpeR')        # da seh ich ein LogO ;)

background = pygame.image.load("jumper/bg.png")
standing_surface = pygame.transform.scale(pygame.image.load("jumper/cyborg_run1.png"), (0, 0))
jumping_surface = pygame.transform.scale(pygame.image.load("jumper/cyborg_jump.png"), (0, 0))

moving = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = running(counter, moving)           #pygame.image.load("jumper/cyborg_run1.png")
        #self.image.fill(RED)  # Rotes Rechteck für die Spielfigur
        self.rect = self.image.get_rect()
        self.rect.center = (window_width // 2, window_height // 2)
        self.speed_x = 0
        self.speed_y = 0
        self.y_velocity = jump_height       ###
        self.jump_count = 0                 ###
        self.jump_height = jump_height      ###

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.speed_x = -5
        if keys[K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        self.speed_y += 0.5  # Beschleunigung für den Sprung
        self.rect.y += self.speed_y

        if self.rect.y >= window_height - self.rect.height:
            self.rect.y = window_height - self.rect.height
            self.speed_y = 0
        #print(self.rect.y)
        #if self.rect.y == 550:
         #   self.jump_count = 0
           
        

    def jump(self): 
        #global jump_count
       
        self.speed_y = -13  # Geschwindigkeit für den Sprung
        y_velocity = self.y_velocity  #Y wird bestimmt
        y_velocity -= gravity       #velo wird um gravity(1) verringert
        
        self.rect.y -= y_velocity   #

        jump_height = self.jump_height  #10
        y_velocity = jump_height
        if y_velocity < -jump_height:
            y_velocity = jump_height


def running(c, moving):
    print("Walking funk")
    if moving:
        if c == 0:          #if walking True
            print("walking funk c0")
            return pygame.image.load("jumper/cyborg_run1.png")
        elif c == 1:
            print("walking funk c1")
            return pygame.image.load("jumper/cyborg_run2.png")
        elif c == 2:
            print("walking funk c2")
            return pygame.image.load("jumper/cyborg_run3.png")
        elif c == 3:
            print("walking funk c3")
            return pygame.image.load("jumper/cyborg_run4.png")
        elif c == 4:
            print("walking funk c4")
            return pygame.image.load("jumper/cyborg_run5.png")
    else:
        return pygame.image.load("jumper/cyborg_run5.png")
            

            
# Definiere die Farben
#BLACK = (0, 0, 0)
#RED = (255, 0, 0)

# Spielfigur                #get rect!
player_width = 50
player_height = 50
player_x = window_width // 2 - player_width // 2
player_y = window_height - player_height

# Spielvariablen
player_speed = 5        #?
     
gravity = 1
max_jumps = 2
jump_count = 0
jump_height = 10
y_velocity = jump_height

counter = 0



player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

moving = False

gameon = True
clock = pygame.time.Clock()

while gameon:
    clock.tick(60)  # Begrenze die Framerate auf 60 FPS

    if player.rect.y >= window_height - player.rect.height:
        jump_count = 0

    


    for event in pygame.event.get():

        if event.type == QUIT:
            gameon = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if jump_count < max_jumps:
                    player.jump()  
                    jump_count += 1
            elif event.key == K_RIGHT:
                moving = True

                #if counter > 5:
                 #   counter = 0
                #else:
                  #  counter += 1
            elif event.key == K_LEFT:
                moving = True
                #if counter > 5:
                 #   counter = 0
                #else:
                  #  counter += 1
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                moving = False
            if event.key == K_LEFT:
                moving = False
            
                

    if moving:
        if counter > 5:
            counter = 0
        else:
            counter += 1

    window.blit(background, (0, 0))
    player.image


    print(counter)

    all_sprites.update()
 
    #window.fill(BLACK)  # Hintergrundfarbe des Fensters

    all_sprites.draw(window)

    pygame.display.flip()

pygame.quit()





