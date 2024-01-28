import sys

import pygame
import random
import math
from button import Button

from pygame import mixer

# Initializing pygame:
pygame.init()

# Creating the screen and setting its size
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('assets/background.jpg')

# Background Sound
playMusic = True
if playMusic:
    mixer.music.load('assets/background.wav')
    mixer.music.play(-1)
else:
    mixer.music.stop()

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# Bullet loaded in via image
bulletImg = pygame.image.load('assets/bullet.png')


def readHighScore():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


high_score = readHighScore()


def getFont(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def play():
    # Player loaded in via image
    playerImg = pygame.image.load('assets/ship.png')
    global bulletState
    global high_score

    # Enemy loaded in via image
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyXChange = []
    enemyYChange = []
    numEnemies = 6

    for i in range(numEnemies):
        enemyImg.append(pygame.image.load('assets/enemy.png'))
        enemyX.append(random.randint(40, 735))
        enemyY.append(random.randint(20, 150))
        enemyXChange.append(0.1)
        enemyYChange.append(random.randint(25, 95))

    bulletX = 0
    bulletY = 480
    bulletXChange = 0
    bulletYChange = 0.5
    # Ready = cant see bullet on screen
    # Fire = The bullet is currently moving
    bulletState = "ready"

    # Score
    scoreValue = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    textX = 10
    textY = 10

    # Game over text
    gameOverFont = pygame.font.Font('freesansbold.ttf', 64)

    # Play again text
    gameOverFont = pygame.font.Font('freesansbold.ttf', 64)

    # Setting Player Coordinates on screen
    playerX = 370
    playerY = 480

    # Variable for changing player location
    playerXChange = 0
    playerXChangeNegative = 0

    def showScore(x, y):
        score = font.render("Score: " + str(scoreValue), True, (0, 128, 128))
        high_score_text = font.render("High Score: " + str(high_score), True, (0, 128, 128))
        screen.blit(score, (x, y))
        screen.blit(high_score_text, (x, y + 30))

    def gameOverText():
        overText = gameOverFont.render("GAME OVER", True, (255, 255, 255))
        screen.blit(overText, (200, 250))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    scoreValue = 0

    running = True
    # Game Loop
    while running:
        # Set background color in RGB
        screen.fill((0, 128, 128))

        # Background Image
        screen.blit(background, (0, 0))

        # Allowing exit button to work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save high score when exiting the game loop
                with open('highscore.txt', 'w') as file:
                    file.write(str(high_score))
                running = False
            # Checking keystroke for movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    playerXChangeNegative = -0.3
                if event.key == pygame.K_d:
                    playerXChange = 0.3
                if event.key == pygame.K_SPACE and bulletState is "ready":
                    bulletSound = mixer.Sound('assets/laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
            # If the key is unpressed, turn off movement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    playerXChange = 0
                if event.key == pygame.K_a:
                    playerXChangeNegative = 0

        # Adding the movements value to the players position to move the player
        playerX += playerXChange or playerXChangeNegative

        if playerX <= 0:
            playerX = 0
        elif playerX >= 735:
            playerX = 735

        for i in range(numEnemies):
            enemyX[i] += enemyXChange[i]
            if enemyX[i] <= 0:
                enemyXChange[i] = 0.1
                enemyY[i] += enemyYChange[i]
            elif enemyX[i] >= 735:
                enemyXChange[i] -= 0.1
                enemyY[i] += enemyYChange[i]

            # Game Over
            if enemyY[i] > 440:
                for j in range(numEnemies):
                    enemyY[j] = 2000
                gameOverText()
                with open('highscore.txt', 'w') as file:
                    file.write(str(high_score))
                pygame.display.update()
                gameOverTime = 3000  # time in milliseconds (e.g., 3000ms = 3 seconds)
                startTime = pygame.time.get_ticks()
                while pygame.time.get_ticks() - startTime < gameOverTime:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                running = False  # Set running false to exit the game loop
                break

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound('assets/explosion.wav')
                explosionSound.play()
                bulletY = 480
                bulletState = "ready"
                scoreValue += 1
                enemyX[i] = random.randint(40, 735)
                enemyY[i] = random.randint(20, 150)
                enemyXChange[i] = 0.1

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletState is "fire":
            fireBullet(bulletX, bulletY)
            bulletY -= bulletYChange
        if bulletY <= 0:
            bulletY = 480
            bulletState = "ready"

        # Update high score
        if scoreValue > high_score:
            high_score = scoreValue

        # Calling the player
        player(playerX, playerY)

        # Calling score
        showScore(textX, textY)

        # Need to update screen ALWAYS
        pygame.display.update()


def options():
    optionsScreen = True
    global playMusic
    while optionsScreen:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))

        optionsText = getFont(45).render("OPTIONS", True, "Black")
        optionsRect = optionsText.get_rect(center=(400, 100))
        screen.blit(optionsText, optionsRect)

        optionsBack = Button(image=pygame.image.load("assets/Back col_Button.png"), pos=(400, 500),
                             text_input="", font=getFont(20), base_color="Black", hovering_color="Green")

        musicToggle = Button(image=pygame.image.load("assets/Audio col_Square Button.png"), pos=(400, 250),
                             text_input="", font=getFont(20), base_color="Black", hovering_color="Green")

        optionsBack.changeColor(OPTIONS_MOUSE_POS)
        optionsBack.update(screen)

        musicToggle.changeColor(OPTIONS_MOUSE_POS)
        musicToggle.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save high score when exiting the game loop
                with open('highscore.txt', 'w') as file:
                    file.write(str(high_score))
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if optionsBack.checkForInput(OPTIONS_MOUSE_POS):
                    optionsScreen = False
                if musicToggle.checkForInput(OPTIONS_MOUSE_POS):
                    playMusic = not playMusic  # Toggle the music state
                    if playMusic:
                        mixer.music.play(-1)  # Play music
                    else:
                        mixer.music.stop()

        pygame.display.update()


running = 2
while running == 2:
    screen.blit(background, (0, 0))

    menuMousePOS = pygame.mouse.get_pos()

    menuText = getFont(50).render("MAIN MENU", True, "#b68f40")
    menuRect = menuText.get_rect(center=(400, 100))

    playButton = Button(image=pygame.image.load("assets/Play col_Button.png"), pos=(400, 250),
                        text_input="", font=getFont(20), base_color="#d7fcd4", hovering_color="White")
    optionsButton = Button(image=pygame.image.load("assets/Options col_Button.png"), pos=(400, 350),
                           text_input="", font=getFont(20), base_color="#d7fcd4", hovering_color="White")
    quitButton = Button(image=pygame.image.load("assets/Quit col_Button.png"), pos=(400, 450),
                        text_input="", font=getFont(20), base_color="#d7fcd4", hovering_color="White")

    screen.blit(menuText, menuRect)

    for button in [playButton, optionsButton, quitButton]:
        button.changeColor(menuMousePOS)
        button.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButton.checkForInput(menuMousePOS):
                play()
            if optionsButton.checkForInput(menuMousePOS):
                options()
            if quitButton.checkForInput(menuMousePOS):
                pygame.quit()
                sys.exit()

    pygame.display.update()
