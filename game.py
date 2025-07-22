import pygame
import random
import math
from pygame import mixer

# Intitialise pygame module
pygame.init()

# Create screen
screen = pygame.display.set_mode((800,700))

#Backbrground
background = pygame.image.load('Space bg.png')

#background sound
mixer.music.load('backgroundsound.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)


# Game Icon and Title
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('ar.png')
pygame.display.set_icon(icon)

#Player
playerImg=pygame.image.load('spaceship (1).png')
playerImg = pygame.transform.scale(playerImg, (65, 65)) # Adjust the size icon as needed
playerX=300
playerY=570
playerX_change=0

#ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (70, 70)) # Adjust the size icon as needed
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)  #4
    enemyY_change.append(40)   #it will step down the enemey

#BULLET
#ready you can't see the bullet
#fire the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (30, 30)) # Adjust the size icon as needed
bulletX = 0
bulletY = 480
bulletX_change=0
bulletY_change=10   #SPEED of bullet
bullet_state="ready"  

#SCORE~~
score_value = 0 
font = pygame.font.Font('freesansbold.ttf',32)

textX=10
testY=10

#GAME OVER

over_font = pygame.font.Font('freesansbold.ttf',64)

#function
def show_score(x,y):
    score = font.render("SCORE :" + str(score_value),True,(255,255,255))          
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER:",True,(255,255,255))    
    screen.blit(over_text,(150,100))

def player(x,y):
    screen.blit(playerImg,(x,y))#blit-drawing icon img

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))#blit-drawing icon img

def fire_bullet(x,y):# function to fire the bullet 
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+10,y+8))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
    

#playerX+ to move right
#playerX- to move left
#playerY+ to move down
#playerY- to move up
    
# Game Loop
running = True
while running:

    screen.fill((0,0,0))  #RGB
# backgronund img
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #if keystroke is pressed check whether its right or left
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change = -8 #Speed of player
            if event.key==pygame.K_RIGHT:
                playerX_change = 8 
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.mp3")
                    
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(playerX,bulletY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change = 0

    
    #350 = 350 + -0.5 -> 350 = 350 - 0.1
                
    #To check the boundaries

    playerX += playerX_change  

    if playerX<=0:
        playerX=0
    elif playerX>=720:
        playerX=720
    
    #enemy movement  
    for i in range(num_of_enemies):

        #GAME OVER

        # Check if any enemy has reached the bottom of the screen
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break    

        enemyX[i] += enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=2 # 4 #SPEED of enemy
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=750:
            enemyX_change[i]=-2# 4
            enemyY[i]+=enemyY_change[i]

        #collision    
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.mp3")
            explosion_sound.set_volume(0.1)
            explosion_sound.play()
            bulletY = 480
            bullet_state= "ready"  
            score_value += 1
            print(score_value)
            enemyX[i]=random.randint(0,800)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <=0:    
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-= bulletY_change

    player(playerX,playerY)
    show_score(textX,testY)

    pygame.display.update()