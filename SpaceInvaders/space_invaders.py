import pygame
import random
import math
from pygame import mixer

# initialize the Pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))  # DON'T FORGET SECOND SET OF BRACKETS

# add space background (add after screen.fill)
background = pygame.image.load('C:\\Python\\PyGame_projects\\SpaceInvaders\\space.png')

# music
# mixer.music.load('<file>')
# mixer.music.play(-1)  # -1 tp play on loop

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('C:\\Python\\PyGame_projects\\SpaceInvaders\\home.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('C:\\Python\\PyGame_projects\\SpaceInvaders\\spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('C:\\Python\\PyGame_projects\\SpaceInvaders\\space-invaders.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(10)
    enemyY_change.append(40)

# bullet
# ready - can't see the bullet on the screen
# fire - bullet is currently moving
bulletImg = pygame.image.load('C:\\Python\\PyGame_projects\\SpaceInvaders\\bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 25
bullet_state = "ready"

# score
score_value = 0
textX = 10
textY = 10
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 50)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # draw image of player on screen
    screen.blit(playerImg, (x, y))  # parameters: image, coordinates


def enemy(x, y, i):
    # draw image of enemy on screen
    screen.blit(enemyImg[i], (x, y))  # parameters: image, coordinates


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # add space between bullet and character


def is_collision(enemyX, enemyY, item2X, item2Y):
    distance = math.sqrt(math.pow(enemyX - item2X, 2) + math.pow(enemyY - item2Y, 2))

    if distance < 27:
        return True
    else:
        return False


def game_over_text():
    go = font2.render("GAME OVER", True, (255, 255, 255))
    screen.blit(go, (225, 250))


running = True

# Game loop
while running:
    # change background of window, RGB
    screen.fill((0, 0, 0))

    # make background persist
    screen.blit(background, (0, 0))  # img variable and img coordinates

    for event in pygame.event.get():  # loop through all pygame events
        # quit event
        if event.type == pygame.QUIT:
            running = False

        # keystroke event
        if event.type == pygame.KEYDOWN:  # KEYDOWN - pressing down on key
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # bullet_sound = mixer.Sound('<file>')
                    # bullet_sound.play()
                    # get and store the current x-coord of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            # if direction key is released, character stops changing
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Player movement
    playerX += playerX_change

    # Player bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # have to account for size of character
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        # Enemy movement
        enemyX[i] += enemyX_change[i]

        # Player bounds
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # have to account for size of character
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision
        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # enemy function
        enemy(enemyX[i], enemyY[i], i)

    # call player function - make sure it is called after the fill method
    player(playerX, playerY)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)

    # update view
    pygame.display.update()

pygame.quit()
