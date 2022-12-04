import time

import pygame
import math
import random
from pygame import mixer


# --------------INFO--------------
# CTRL+ALT+L - good look code

# --------------------Adrian Lidwin--------------------


# Button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # Draw button on screen
    def draw(self):
        action = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Mouse_position
        pos = pygame.mouse.get_pos()
        # Check mousePosition_&_Click
        (x, y) = pygame.mouse.get_pos()
        # print(x,y)
        if self.rect.collidepoint(pos):
            # 0-left / 1-middle / 2-right
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # if_clicked = 1
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:  # if_not_clicked=0
            self.clicked = False
        return action


# initialize pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.init()
screen = pygame.display.set_mode((1000, 700))  # Tworzenie okna

music = True

# Shop
speed_buy = 2
bullet_buy = 2

# -----------------------------------------MENU

# Button_Images
Logo_font = pygame.font.Font('freesansbold.ttf', 30)
logo_img = pygame.image.load('logo.png')
# Main_Menu

Start = Logo_font.render("Start game", True, (255, 255, 255))  # Start_font
Options = Logo_font.render("Options", True, (255, 255, 255))  # Options_font
Exit = Logo_font.render("Exit", True, (255, 255, 255))  # Exit_font
bos = Logo_font.render("Boss!", True, (255, 0, 0))  # Boss_font
# Options

little_menu = Logo_font.render("Return", True, (255, 255, 255))  # game_menu_font
off_on_music = Logo_font.render("On/Off music", True, (255, 255, 255))  # off/on_music_font
add_speed = Logo_font.render("+ Speed", True, (255, 255, 255))  # Speed_font
add_bullet_speed = Logo_font.render("+ Bullet speed", True, (255, 255, 255))  # Bullet_Speed_font

# Buttons Menu
Button_Start = Button(350, 120, logo_img)
Button_Options = Button(350, 260, logo_img)
Button_Exit = Button(350, 420, logo_img)
Button_BossEvent = Button(720, 10, logo_img)

# Buttons Options
Button_off_on_Music = Button(350, 120, logo_img)
Button_Speed_add = Button(350, 260, logo_img)
Button_Bullet_Speed_add = Button(350, 420, logo_img)
Button_little_menu = Button(700, -20, logo_img)

# -----------------------------------------

# Background
Background_img = pygame.image.load("Stars.jpg")
BackgroundY = 0

# Planets_images
uranus = pygame.image.load("uranus.png")  # 64
sun = pygame.image.load("sun.png")  # 64
venus = pygame.image.load('venus.png')  # 24
jupiter = pygame.image.load('jupiter.png')  # 256
neptune = pygame.image.load('neptune.png')  # 32
world = pygame.image.load('worldwide.png')  # 32
planetsY = 0

# Background sounds
if music == True:
    mixer.music.load('background.wav')
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)

# Title & icon
pygame.display.set_caption("Space Ship")
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)

# Player_Stats
player_img = pygame.image.load("Player_Ship.png")
playerX = 468
playerY = 600
player_Speed = 0.2
playerX_change = 0
playerY_change = 0

# Enemy_Stats
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemy_down_power = 32
enemyY_change = []
numb_of_enemies = 6

# Boss_stats
boss_img = pygame.image.load("Boss.png")
bossX = 0
bossY = 30
right = True
boss_life = 10
boss_Wave = 1
boss_defeated = False

# boss_bullets
boss_bullets_speed = 0.2
boss_bulletsX = []
boss_bulletsY = []
boss_bullets_all = 10
boss_bull_img = []
# boss_bull_img.append(pygame.image.load("enemy.png"))
boss_bullet = pygame.image.load("circle.png")

for i in range(boss_bullets_all):
    boss_bull_img.append(pygame.image.load("circle.png"))
    boss_bulletsX.append(random.randint(2, 998))
    boss_bulletsY.append(0)

for i in range(numb_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 820))
    enemyY.append(random.randint(2, 120))
    enemyX_change.append(0.5)

# Bullet_Stats
bullet_img = pygame.image.load("L_bullet.png")
bulletX = 0
bulletY = 0
bulletX_change = 0  # for late updates
bulletY_Speed = 0.5
bullet_fire = "Ready"  # Ready/Fire

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 20
textY = 20


def CanBuy(x):
    if score_value >= x:
        score_value - x
        return True
    else:
        return False


# Game over txt
def game_over_text():
    game_over_font = pygame.font.Font('freesansbold.ttf', 80)
    game_over = game_over_font.render("Game over!!!", True, (255, 0, 0))
    screen.blit(game_over, (240, 250))
    # mixer.music.stop()



def showScore(x, y):
    score = font.render("Score " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def showHp(x, y):
    global boss_life
    hp = font.render("HP - " + str(boss_life), True, (255, 22, 22))
    screen.blit(hp, (x, y))


def showBossDefeat(x, y):
    global boss_Wave
    global boss_defeated
    if boss_defeated:
        deff = font.render("BOSS DEFEATED! LVL: " + str(boss_Wave), True, (255, 22, 22))
        screen.blit(deff, (x, y))
    else:
        return


def enemy_move(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def player_move(x, y):
    screen.blit(player_img, (x, y))  # blit = draw


def Bullet(x, y):
    global bullet_fire
    bullet_fire = "Fire"
    screen.blit(bullet_img, (x + 25, y - 24))


def backGround_move(Bc):
    screen.blit(Background_img, (0, Bc))


def planets_move(y):
    screen.blit(jupiter, (0, y))  # Xd


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX - enemyX - 8, 2) + math.pow(bulletY - enemyY - 16, 2))
    if distance < 36:
        return True
    else:
        return False


def bossCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX - enemyX - 8, 2) + math.pow(bulletY - enemyY - 16, 2))
    if distance < 80:
        return True
    else:
        return False


def bossEvent():
    global bossX
    global right
    global boss_life
    global boss_defeated
    global boss_Wave
    global bossY
    global score_value

    global boss_bulletsX
    global boss_bullets_all
    global only_one

    if boss_life == 0 and boss_defeated == False:
        bossY = 1200
        score_value += 2 * boss_Wave
        boss_Wave += 1
        boss_defeated = True

    if boss_defeated == False:
        bossY = 30

    if bossX < 0:
        right = True
    if bossX > 746:
        right = False

    if right:
        bossX += 0.1
    else:
        bossX -= 0.1

    screen.blit(boss_img, (bossX, bossY))

    # Boss_shot
    screen.blit(boss_bullet, (bossX, bossY + 100))
    for i in range(boss_bullets_all):
        screen.blit(boss_bull_img[i], (boss_bulletsX[i], boss_bulletsY[i]))
        boss_bulletsY[i] += (boss_bullets_speed * boss_Wave) + 0.1
        if boss_bulletsY[i]>700:
            boss_bulletsY[i] = 0
            boss_bulletsX[i] = random.randint(2,988)
        if isCollision(boss_bulletsX[i],boss_bulletsY[i],playerX,playerY):
            game_over_text()
            for j in range(boss_bullets_all):
                screen.blit(boss_bull_img[i], (boss_bulletsX[i], 2000))


# Game loop
running = False  # Gra
Game = True  # Aplikacja
Menu = True  # menu
Boss_event = False
Options_menu = False  # Opcje


def options():
    global speed_buy
    global bullet_buy
    global score_value
    if Button_off_on_Music.draw() == True:
        print("music off/on")
        global music
        if music == True:
            music = False
            mixer.music.set_volume(0)
        else:
            music = True
            mixer.music.set_volume(0.1)
    if Button_Speed_add.draw() == True:
        if CanBuy(speed_buy):

            global player_Speed
            player_Speed += 0.3
            score_value -= speed_buy
            speed_buy += 2

            if player_Speed > 4.5:
                player_Speed = 4.5

            print("+ Speed add " + player_Speed.__str__())
        else:
            return

    if Button_Bullet_Speed_add.draw() == True:
        if (CanBuy(bullet_buy)):
            global bulletY_Speed
            bulletY_Speed += 0.5
            score_value -= bullet_buy
            bullet_buy += 2

            print("+ Bullet speed add + " + bulletY_Speed.__str__())
        else:
            return

    if Button_little_menu.draw() == True:
        print("little menu - back")
        global Options_menu
        global running
        global Menu
        time.sleep(0.1)
        Options_menu = False
        if running == True:
            running = False
        Menu = True

    screen.blit(off_on_music, (410, 206))  # Start_txt
    screen.blit(add_speed, (430, 346))  # Options_txt
    screen.blit(add_bullet_speed, (396, 506))  # Exit_txt
    screen.blit(little_menu, (800, 66))


def menu():
    if Button_Start.draw() == True:  # Start_img
        print("Start")
        time.sleep(0.1)
        global running
        running = True
        global Menu
        Menu = False
    if Button_Options.draw() == True:  # Options_img
        print("Options")
        time.sleep(0.1)
        global Options_menu
        Options_menu = True
        Menu = False
    if Button_Exit.draw() == True:  # Exit_img
        print("Exit")
        global Game
        Game = False

    if Button_BossEvent.draw() == True:
        global Boss_event
        Boss_event = True
        Menu = False

    screen.blit(Start, (410, 206))  # Start_txt
    screen.blit(Options, (430, 346))  # Options_txt
    screen.blit(Exit, (465, 506))  # Exit_txt
    screen.blit(bos, (820, 96))


while Game:
    # Menu
    if Menu:
        BackgroundY += 0.1
        backGround_move(BackgroundY)
        backGround_move(BackgroundY - 700)
        if BackgroundY > 700:
            BackgroundY = 0
        menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Game = False
        showScore(20, 30)
        pygame.display.update()

    if Options_menu:
        BackgroundY += 0.1
        backGround_move(BackgroundY)
        backGround_move(BackgroundY - 700)
        showScore(20, 30)
        options()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Game = False

        speed_cost = Logo_font.render("Cost: " + speed_buy.__str__(), True, (255, 255, 255))
        bullet_cost = Logo_font.render("Cost: " + bullet_buy.__str__(), True, (255, 255, 255))
        screen.blit(bullet_cost, (700, 500))
        screen.blit(speed_cost, (700, 350))
        screen.blit(boss_img, (100, 200))
        pygame.display.update()

    if Boss_event:

        BackgroundY += 0.1
        backGround_move(BackgroundY)
        backGround_move(BackgroundY - 700)
        if BackgroundY > 700:
            BackgroundY = 0
        showScore(20, 30)

        showHp(200, 20)
        showBossDefeat(280, 250)
        bossEvent()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Game = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change -= player_Speed

                if event.key == pygame.K_RIGHT:
                    playerX_change += player_Speed

                if event.key == pygame.K_UP:
                    playerY_change -= player_Speed

                if event.key == pygame.K_DOWN:
                    playerY_change += player_Speed

                if event.key == pygame.K_SPACE and bullet_fire == "Ready":
                    bulletY = playerY
                    bulletX = playerX
                    Bullet(playerX, bulletY)

                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_sound.set_volume(0.1)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        if Button_little_menu.draw() == True:
            print("little menu - back")
            time.sleep(0.2)
            screen.blit(little_menu, (800, 66))
            Menu = True
            Boss_event = False
            boss_defeated = False
            boss_life = 10 * boss_Wave
            only_one = True

            for k in range(boss_bullets_all):
                boss_bulletsY[k]=0
                screen.blit(boss_bull_img[k], (boss_bulletsX[k], boss_bulletsY[k]))

        playerX += playerX_change
        playerY += playerY_change

        # player_block
        if playerX >= 936:
            playerX = 936
        if playerX <= 0:
            playerX = 0
        if playerY <= 450:
            playerY = 450
        if playerY >= 638:
            playerY = 638
        player_move(playerX, playerY)

        if bulletY <= 0:
            bulletY = playerY
            bullet_fire = "Ready"

        if bullet_fire == "Fire":
            Bullet(bulletX, bulletY)
            bulletY -= bulletY_Speed
        collision = bossCollision(bossX + 100, bossY + 74, bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_fire = "Ready"
            boss_life -= 1
            enemySound = mixer.Sound('explosion.wav')
            enemySound.play()
            enemySound.set_volume(0.1)

        pygame.display.update()

    if running:
        planetsY += 0.1

        # RGB
        # screen.fill((10, 0, 20))
        # Background_animation
        BackgroundY += 0.1
        backGround_move(BackgroundY)
        backGround_move(BackgroundY - 700)

        # print(BackgroundY)
        if BackgroundY >= 700:
            BackgroundY = 0

        # planets_move(planetsY)
        showScore(textX, textY)

        if Button_little_menu.draw() == True:
            print("little menu - back")
            time.sleep(0.1)
            screen.blit(little_menu, (800, 66))
            Menu = True
            running = False
        # QUIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Game = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change -= player_Speed

                if event.key == pygame.K_RIGHT:
                    playerX_change += player_Speed

                if event.key == pygame.K_UP:
                    playerY_change -= player_Speed

                if event.key == pygame.K_DOWN:
                    playerY_change += player_Speed

                if event.key == pygame.K_SPACE and bullet_fire == "Ready":
                    bulletY = playerY
                    bulletX = playerX
                    Bullet(playerX, bulletY)

                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_sound.set_volume(0.1)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        playerX += playerX_change
        playerY += playerY_change

        # player_block
        if playerX >= 936:
            playerX = 936
        if playerX <= 0:
            playerX = 0
        if playerY <= 450:
            playerY = 450
        if playerY >= 638:
            playerY = 638

        # Enemy_movement
        for i in range(numb_of_enemies):

            # Game_Over
            if enemyY[i] > 360:
                for j in range(numb_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] >= 936:
                enemyX_change[i] = -0.6
                enemyY[i] += enemy_down_power
            elif enemyX[i] <= 0:
                enemyX_change[i] = 0.6
                enemyY[i] += enemy_down_power
            # Collisions
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = playerY
                bullet_fire = "Ready"
                score_value += 1
                enemyX[i] = random.randint(0, 820)
                enemyY[i] = random.randint(2, 120)
                enemySound = mixer.Sound('explosion.wav')
                enemySound.play()
                enemySound.set_volume(0.1)
            enemy_move(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bulletY <= 0:
            bulletY = playerY
            bullet_fire = "Ready"

        if bullet_fire == "Fire":
            Bullet(bulletX, bulletY)
            bulletY -= bulletY_Speed

        player_move(playerX, playerY)

        pygame.display.update()
