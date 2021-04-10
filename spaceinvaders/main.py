import pygame
import random
import math
from pygame import mixer

pygame.init()

# schermo
screen = pygame.display.set_mode((800, 600))

# titolo, icona
pygame.display.set_caption("HotDog Invaders")
icon = pygame.image.load("hotdog.png")
pygame.display.set_icon(icon)

# player
player = pygame.image.load("giocatore.png")
playerx = 370
playery = 480
playerx_change = 0
playery_change = 0
rotation = 43
rotation_change = 0

# enemy
enemy = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
NumOfEnemy = 6
for i in range(0, NumOfEnemy):
    enemy.append(pygame.image.load("food.png"))
    enemyx.append(random.randint(65, 736))
    enemyy.append(random.randint(64, 100))
    enemyx_change.append(0.2)
    enemyy_change.append(40)

# fish
fish1 = pygame.image.load("fish.png")
fish = pygame.transform.rotate(fish1, 90)
fishx = playerx
fishy = playery
fishx_change = 0
fishy_change = 0.5
fishstate = "ready"  # ready = you can't see the fish, fire = you can

# backround sound
mixer.music.load("background.wav")
mixer.music.set_volume(0.1)
mixer.music.play(-1)  # you add -1 so it loops during all the time

# score and add text
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)  # name of the font and size
FontX = 10
FontY = 10

# game over
over = pygame.font.Font("freesansbold.ttf", 90)




def Show_Score(x, y):
    score2 = font.render("Score: " + str(score), True, (255, 255, 255))  # before blint you need to render
    # text you want, True, color
    screen.blit(score2, (x, y))


def Giocatore(x, y):
    screen.blit(nuovoplayer, (x, y))


def Nemico(x, y, i):
    screen.blit(enemy[i], (x, y))


def pesce(x, y):
    global fishstate
    fishstate = "fire"
    screen.blit(fish, (x + 30, y - 30))


def IsCollison(EnemyX, EnemyY, FishX, FishY):
    distance = math.sqrt(math.pow(EnemyX - FishX, 2) + math.pow(EnemyY - FishY, 2))  # Distance= sqrt (x-x)2 + (y-y)2
    if distance < 29:
        return True
    else:
        return False


def gameover():
    GameOver = font.render("GAME OVER CAZZO", True, (255, 255, 255))
    screen.blit(GameOver, (250, 250))


running = True
while running:

    # colore sfondo
    screen.fill((100, 0, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # if a key is pressed
            if event.key == pygame.K_a:
                playerx_change = -0.3
            if event.key == pygame.K_d:
                playerx_change = 0.3
            if event.key == pygame.K_w:
                playery_change = -0.3
            if event.key == pygame.K_s:
                playery_change = 0.3
            if event.key == pygame.K_RIGHT:
                rotation_change = -0.3
            if event.key == pygame.K_LEFT:
                rotation_change = 0.3
            if event.key == pygame.K_SPACE:
                if fishstate == "ready":
                    fishsound = mixer.Sound("laser.wav")
                    fishsound.set_volume(0.2)
                    fishsound.play()
                    pesce(playerx, fishy)
                    fishx = playerx

        if event.type == pygame.KEYUP:  # if the keys are not presed anymore
            if event.key == pygame.K_a or event.key == pygame.K_d:  # if the released key is one of these
                playerx_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                playery_change = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                rotation_change = 0

    # adding borders
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:  # keep in mind the size of the icon is 64x64
        playerx = 736
    elif playery <= 0:
        playery = 0
    elif playery >= 536:
        playery = 536

    # player rotation (check also key input)
    rotation += rotation_change
    nuovoplayer = pygame.transform.rotate(player, rotation)

    # enemymovement
    for i in range(0, NumOfEnemy):

        # game over
        if enemyy[i] > 420:
            for j in range(0, NumOfEnemy):
                enemyy[j] = 2000
            gameover()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:  # keep in mind the size of the icon is 64x64
            enemyx_change[i] = -0.2
            enemyy[i] += enemyy_change[i]
        # collision
        if IsCollison(enemyx[i], enemyy[i], fishx, fishy):
            killsound = mixer.Sound("splat.wav")
            killsound.set_volume(0.2)
            killsound.play()
            fishy = 480
            fishstate = "ready"
            score += 1
            enemyx[i] = random.randint(65, 736)
            enemyy[i] = random.randint(64, 100)
        Nemico(enemyx[i], enemyy[i], i)

        # fish movement
    if fishstate == "fire":
        fishy -= fishy_change
        pesce(fishx, fishy)
        fishy -= fishy_change
    if fishy < 0:
        fishy = playery
        fishstate = "ready"

    playerx += playerx_change
    playery += playery_change
    Giocatore(playerx, playery)  # called after the backround color
    Show_Score(FontX, FontY)
    pygame.display.update()
