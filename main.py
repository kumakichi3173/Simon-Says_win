import pygame
import random
import time

# from pygments import highlight

from button import Button # By importing Button we can access methods from the Button class

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

#font = pygame.font.SysFont("Arial", 32)
'''text = font.render("{}:{}:{}".format(hours, mins, secs), True, (255, 255, 255), (0, 0, 0))
textRect = text.get_rect()
textRect.center = 4, 4
'''

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BLUE = (80, 80, 155)
font = pygame.font.SysFont("Arial", 50)
text_render = font.render("Score 0", 1, BLUE)
#SCREEN.blit(text_render, (10, 10))

highScore = 0
gameOver = False
first = True # To see if it's the first round of the game

start_ticks=pygame.time.get_ticks()

# SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GREEN_ON = (0, 255, 0)
GREEN_OFF = (0, 200, 0)
RED_ON = (255, 0, 0)
RED_OFF = (200, 0, 0)
BLUE_ON = (0, 0, 255)
BLUE_OFF = (0, 0, 200)
YELLOW_ON = (255, 255, 0)
YELLOW_OFF = (200, 200, 0)

# Pass in respective sounds for each color
GREEN_SOUND = pygame.mixer.Sound("bell1.wav") # bell1
RED_SOUND = pygame.mixer.Sound("bell2.wav") # bell2
BLUE_SOUND = pygame.mixer.Sound("bell3.wav") # bell3
YELLOW_SOUND = pygame.mixer.Sound("bell4.wav") # bell4

# Button Sprite Objects
green = Button(GREEN_ON, GREEN_OFF, GREEN_SOUND, 10, 110)
red = Button(RED_ON, RED_OFF, RED_SOUND, 260, 110)
blue = Button(BLUE_ON, BLUE_OFF, BLUE_SOUND, 260, 360)
yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 10, 360)

# Variables
colors = ["green", "red", "blue", "yellow"]
cpu_sequence = []
choice = ""

seconds = 3

#resetTimer = False
#playerTurn = False

'''
Draws game board
'''

def stats(score):
    #scoreShow = pygame.Surface((230, 230))
    #scoreShow.fill("White")
    #font = pygame.font.SysFont("Arial", 50)
    text_render = font.render("Score: " + str(score-1), 1, "Black")
    SCREEN.blit(text_render, (10, 10))
    text_render = font.render("Score: " + str(score), 1, BLUE)
    SCREEN.blit(text_render, (10, 10))

    global seconds
    text = font.render("Timer: {}".format(seconds), True, (255, 255, 255), (0, 0, 0))
    SCREEN.blit(text, (230, 10))


def resetButton(screen, position, text):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
    return screen.blit(text_render, (x, y))


def draw_board():
    # Call the draw method on all four button objects
    green.draw(SCREEN)
    red.draw(SCREEN)
    blue.draw(SCREEN)
    yellow.draw(SCREEN)

'''
Chooses a random color and appends to cpu_sequence.
Illuminates randomly chosen color.
'''

def cpu_turn():
    choice = random.choice(colors) # pick random color
    cpu_sequence.append(choice) # update cpu sequence
    if choice == "green":
        green.update(SCREEN)
    # Check other three color options
    if choice == "blue":
        blue.update(SCREEN)
    if choice == "red":
        red.update(SCREEN)
    if choice == "yellow":
        yellow.update(SCREEN)

'''
Plays pattern sequence that is being tracked by cpu_sequence
'''

def repeat_cpu_sequence():
    if(len(cpu_sequence) != 0):
        for color in cpu_sequence:
            if color == "green":
                green.update(SCREEN)
            elif color == "red":
                red.update(SCREEN)
            elif color == "blue":
                blue.update(SCREEN)
            else:
                yellow.update(SCREEN)
            pygame.time.wait(500)

'''
After cpu sequence is repeated the player must attempt to copy the same
pattern sequence.
The player is given 3 seconds to select a color and checks if the selected
color matches the cpu pattern sequence.
If player is unable to select a color within 3 seconds then the game is
over and the pygame window closes.
'''

def player_turn():
    global seconds
    pygame.event.clear()

    turn_time = time.time()
    players_sequence = []

    while time.time() <= turn_time + 3 and len(players_sequence) < len(cpu_sequence):
        text = font.render("Timer: {}".format(seconds), True, (0, 0, 0), (0, 0, 0))
        SCREEN.blit(text, (230, 10))

        seconds = int(turn_time + 3 - time.time()) + 1
        text = font.render("Timer: {}".format(seconds), True, (255, 255, 255), (0, 0, 0))
        SCREEN.blit(text, (230, 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # button click occured
                # Grab the current position of mouse here
                pos = pygame.mouse.get_pos()
                if green.selected(pos): # green button was selected
                    green.update(SCREEN) # illuminate button
                    players_sequence.append("green") # add to player sequence
                    check_sequence(players_sequence) # check if player choice was correct
                    turn_time = time.time() # reset timer


                # Check other three options

                if red.selected(pos): # green button was selected
                    red.update(SCREEN) # illuminate button
                    players_sequence.append("red") # add to player sequence
                    check_sequence(players_sequence) # check if player choice was correct
                    turn_time = time.time() # reset timer

                if blue.selected(pos): # green button was selected
                    blue.update(SCREEN) # illuminate button
                    players_sequence.append("blue") # add to player sequence
                    check_sequence(players_sequence) # check if player choice was correct
                    turn_time = time.time() # reset timer
                
                if yellow.selected(pos): # green button was selected
                    yellow.update(SCREEN) # illuminate button
                    players_sequence.append("yellow") # add to player sequence
                    check_sequence(players_sequence) # check if player choice was correct
                    turn_time = time.time() # reset timer

    # If player does not select a button within 3 seconds then the game closes
    if not time.time() <= turn_time + 3:
        game_over()

'''
Checks if player's move matches the cpu pattern sequence
'''

def check_sequence(players_sequence):
    if players_sequence != cpu_sequence[:len(players_sequence)]:
        game_over()

'''
Quits game and closes pygame window
'''


def game_over():
    pygame.event.clear()

    global cpu_sequence
    global highScore
    image = pygame.Surface((500, 600))
    image.fill("Black")
    SCREEN.blit(image, (0, 0))

    if highScore < len(cpu_sequence):
        highScore = len(cpu_sequence)
        font = pygame.font.SysFont("Arial", 25)
        text_render = font.render("New High Score! " + str(highScore), 1, "Gold")
        SCREEN.blit(text_render, (150, 150))
    else:
        font = pygame.font.SysFont("Arial", 25)
        text_render = font.render("Score:  " + str(len(cpu_sequence)), 1, "Gold")
        SCREEN.blit(text_render, (150, 150))
        text_render = font.render("High Score:  " + str(highScore), 1, "Gold")
        SCREEN.blit(text_render, (150, 200))
    font = pygame.font.SysFont("Arial", 25)
    text_render = font.render("If you want to restart, ", 1, "White")
    SCREEN.blit(text_render, (150, 300))
    text_render = font.render("click on the reset button!", 1, "White")
    SCREEN.blit(text_render, (150, 325))

    reset = resetButton(SCREEN, (150, 400), "RESET")
    global gameOver
    gameOver = True

    global score
    score = 0
    cpu_sequence = []
    global first
    first = True


# Game Loop
def gameStart():
    global gameOver
    while gameOver == False:
        pygame.event.clear()
        global first
        global score
        global cpu_sequence
        
        score = len(cpu_sequence)

        if first == True:
            #pygame.display.update()
            draw_board() # draws buttons onto pygame screen
            stats(score) # Timer and score
            first = False

        #pygame.display.update()

        pygame.time.wait(1000) # waits one second before repeating cpu sequence
        draw_board() # draws buttons onto pygame screen

        stats(score) # Timer and score

        repeat_cpu_sequence() # repeats cpu sequence if it's not empty

        cpu_turn() # cpu randomly chooses a new color

        player_turn() # player tries to recreate cpu sequence
        clock.tick(60)
        if gameOver == True:
            break


#This was for the timer of how long the whole game lasts

#t1 = Thread(target = gameStart)
#t2 = Thread(target = timerShow)#, daemon=True)#, args=(start_ticks,), daemon=True)
#t1.start()
#t2.start()

while True:
    pygame.display.update()
    if gameOver == False:
        gameStart()
    else:
        reset = resetButton(SCREEN, (150, 400), "RESET")
        pygame.event.clear()
        #event = pygame.event.wait()  
        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset.collidepoint(pygame.mouse.get_pos()):
                        gameOver = False
                        pygame.event.clear()
                        image = pygame.Surface((500, 600))
                        image.fill("Black")
                        SCREEN.blit(image, (0, 0))
    pygame.display.update()