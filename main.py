import math
import random
from re import L

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')
background2 = pygame.image.load('background2.jpg')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Coin
coinImg = []
coin_value = 0
num_of_coin = 30
coin_x = []
coin_y = []
coin_x_change = []
coin_y_change = []

# scrolling
bg_y1 = 0
bg_y2 = -screen.get_height()

# clock
clock = pygame.time.Clock()

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

for i in range(num_of_coin):
    coinImg.append(pygame.image.load('dollar.png'))
    coin_x.append(random.randint(0, screen.get_width()))
    coin_y.append(random.randint(-20 * screen.get_height(), 0))

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


coin_value_x = 10
coin_value_y = 50
coin_icon =  pygame.image.load('dollar.png')

def show_coin(x, y):
    coin = font.render("Coin : " + str(coin_value), True, (255, 255, 255))
    screen.blit(coin, (x, y))
    screen.blit(coin_icon, (x+130, y))



def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def coin(x, y, i):
    screen.blit(coinImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False

# Game Loop
running = True
speed = 60
while running:

    # scrolling
    bg_y1 += 1.4  # Move both background images back
    bg_y2 += 1.4

    if bg_y1 > screen.get_height():  # If our bg is at the -width then reset its position
        bg_y1 = -screen.get_height()
    
    if bg_y2 > screen.get_height():
        bg_y2 = -screen.get_height()

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, bg_y1))
    screen.blit(background2, (0, bg_y2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Coin created 

    for i in range(num_of_coin):
        coin_y_change = 6
        coin_y[i] += coin_y_change
        collision = isCollision(coin_x[i], coin_y[i], playerX + 32, playerY + 32)
        if collision:
            coin_sound = mixer.Sound("coin-sound.wav")
            coin_sound.play()
            coin_value += 1
            coin_x[i] = random.randint(-100, 0)
            coin_y[i] = random.randint(screen.get_height(), screen.get_height() + 100)
        coin(coin_x[i], coin_y[i], i)

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    show_coin(coin_value_x, coin_value_y)
    clock.tick(speed)
    pygame.display.update()
