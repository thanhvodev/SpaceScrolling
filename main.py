import math
import random
from re import L
import sys
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
num_of_enemies = 5
num_of_enemies_killed = 0

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

# State
state = 'playing'

# Game hardness
hardness = 'easy'
check = pygame.image.load('check-mark.png')


def spawn_enemy(num_of_enemies):
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

def spawn_coin(num_of_coin):
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

def win_text():
    over_text = over_font.render("YOU WIN", True, (255, 255, 255))
    screen.blit(over_text, (230, 250))

def back_text():
    back_text = font.render("Back", True, (255, 255, 255))
    screen.blit(back_text, (10, screen.get_height()-40))

play_again_x = 200
play_again_y = 330
def play_again_text():
    over_text = over_font.render("PLAY AGAIN?", True, (255, 255, 255))
    screen.blit(over_text, (play_again_x, play_again_y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def tick(x, y):
    screen.fill((204, 152, 102, 255))
    screen.blit(check, (x, y))

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

def game_play():
    running = True
    speed = 60
    global bg_y1
    global bg_y2
    global playerX
    global playerY
    global playerX_change
    global state
    global num_of_enemies_killed
    global num_of_enemies
    global num_of_coin
    global bulletX
    global bulletY
    global bulletX_change
    global bulletY_change
    global bullet_state
    global score_value
    global coin_value
    spawn_enemy(num_of_enemies)
    spawn_coin(num_of_coin)
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
        back_text()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if state == 'win' or state == 'lose':
                    if mouse_x > play_again_x and mouse_x < play_again_x + 400:
                        if mouse_y > play_again_y and mouse_y < play_again_y + 50:
                            state = 'playing'
                            num_of_enemies_killed = 0
                            score_value = 0
                            coin_value = 0
                            for i in range(num_of_enemies):
                                enemyX[i] = random.randint(0, 736)
                                enemyY[i] = random.randint(50, 150)
                                enemyY_change[i] = 40
                if 10 < mouse_x < 10+100:
                    if screen.get_height() - 40 < mouse_y < screen.get_height():
                        main_menu()

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
            if state == 'win' or state == 'lose':
                break
            else:
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
            if enemyY[i] > 440:
                state = 'lose'
            if num_of_enemies == num_of_enemies_killed:
                state = 'win'
            # Game Over
            if state == 'lose':
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                play_again_text()
                break
            elif state == 'win':
                win_text()
                play_again_text()
                break
            else:
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
                    enemyY[i] = -440
                    enemyY_change[i] = 0
                    num_of_enemies_killed += 1

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

def about():
    pygame.display.set_caption("About")    
    screen.fill((204, 152, 102, 255))
    while True:
        about_text = over_font.render("This is a scrolling game", True, (255, 255, 255))
        screen.blit(about_text, (0, 170))

        back_text = over_font.render("Back to menu", True, (255, 255, 255))
        screen.blit(back_text, (200, 500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 200 < mouse_x < (200+300):
                    if 500 < mouse_y < 500+50: 
                        main_menu()
        pygame.display.update()

def option():
    global hardness
    global num_of_enemies
    pygame.display.set_caption("Option")  
    screen.fill((204, 152, 102, 255))  
    easy_x = hard_x = back_x = 200
    easy_y = 170
    hard_x = 200
    hard_y = 250
    back_y = 500
    while True:
        if hardness == 'easy':
            tick_y = 160
        else:
            tick_y = 250
        tick(140, tick_y)
        
        easy_text = over_font.render("Easy: 5 enemy", True, (255, 255, 255))
        screen.blit(easy_text, (easy_x, easy_y))

        hard_text = over_font.render("Hard: 10 enemy", True, (255, 255, 255))
        screen.blit(hard_text, (hard_x, hard_y))

        back_text = over_font.render("Back to menu", True, (255, 255, 255))
        screen.blit(back_text, (back_x, back_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if back_x < mouse_x < (back_x+400):
                    if back_y < mouse_y < back_y+50: 
                        main_menu()
                if easy_x < mouse_x < (easy_x+300):
                    if easy_y < mouse_y < easy_y+50: 
                        hardness = 'easy'
                        num_of_enemies = 5
                if hard_x < mouse_x < (hard_x+300):
                    if hard_y < mouse_y < hard_y+50: 
                        hardness = 'hard'   
                        num_of_enemies = 10

        pygame.display.update()    

def main_menu():
    pygame.display.set_caption("Menu")
    play_text_x = 320
    play_text_y = 170

    exit_text_x = 320
    exit_text_y = 380

    option_text_x = 280
    option_text_y = 240

    about_text_x = 290
    about_text_y = 310
    while True:
        screen.fill((204, 152, 102, 255))
        play_text = over_font.render("PLAY", True, (255, 255, 255))
        screen.blit(play_text, (320, 170))

        play_text = over_font.render("OPTION", True, (255, 255, 255))
        screen.blit(play_text, (280, 240))

        play_text = over_font.render("ABOUT", True, (255, 255, 255))
        screen.blit(play_text, (290, 310))

        play_text = over_font.render("EXIT", True, (255, 255, 255))
        screen.blit(play_text, (320, 380))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_text_x < mouse_x < (play_text_x+100):
                    if play_text_y < mouse_y < play_text_y+50:
                        game_play()
                if exit_text_x < mouse_x < (exit_text_x+150):
                    if exit_text_y < mouse_y < exit_text_y+50:
                        pygame.quit()
                        sys.exit()
                if about_text_x < mouse_x < about_text_x + 150:
                    if about_text_y < mouse_y < about_text_y + 50:
                        about()
                if option_text_x < mouse_x < option_text_x + 200:
                    if option_text_y < mouse_y < option_text_y + 50:
                        option()
        pygame.display.update()

main_menu()