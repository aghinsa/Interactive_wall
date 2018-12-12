import pygame
import time
import random

pygame.init()

display_width = 1280
display_height = 720

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)
bright_green = (0,255,0)
bright_red = (255,0,0)

car_width = 227//3
car_height = 500//3

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Demo')
clock = pygame.time.Clock()

carImg = pygame.image.load('car.png')
carImg = pygame.transform.scale(carImg,(227//3,500//3))
carTurnR = pygame.transform.rotate(carImg,-45)
carTurnL = pygame.transform.rotate(carImg,45)

def blocks_dodged(count):
    font = pygame.font.SysFont('ubuntu', 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text,(0,0))

def block(blockx, blocky, blockw, blockh, color):
    pygame.draw.rect(gameDisplay, color, [blockx, blocky, blockw, blockh])

def car(car_img,x,y):
    gameDisplay.blit(car_img,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (display_width/2,display_height/2)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()



def crash():
    message_display('You Crashed')

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        gameDisplay.fill(white)
        message_display("Stupid Car Game")
        if 430 > mouse[0] > 230 and  600 > mouse[1] > 500:
            pygame.draw.rect(gameDisplay,bright_green,(230,500,200,100))
            if click[0] == 1:
                game_loop()
        else:
            pygame.draw.rect(gameDisplay,green,(230,500,200,100))

        if 1070 > mouse[0] > 870 and  600 > mouse[1] > 500:
            pygame.draw.rect(gameDisplay,bright_red,(870,500,200,100))

        else:
            pygame.draw.rect(gameDisplay,red,(870,500,200,100))

        smallText = pygame.font.SysFont('ubuntu', 30)
        textSurf, textRect = text_objects('Go!', smallText)
        textRect.center = (330,550)
        gameDisplay.blit(textSurf,textRect)

        pygame.display.update()
        clock.tick(30)


def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.75)

    x_change = 0
    y_change = 0

    block_width = 100
    block_startx = random.randrange(0, display_width - block_width)
    block_starty = -600
    block_speed = 7
    block_height = 100

    blockCount = 1
    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        x += x_change
        y += y_change
        gameDisplay.fill(white)

        block(block_startx,block_starty,block_width,block_height,red)
        block_starty += block_speed

        if x_change > 0:
            car(carTurnR,x,y)
        elif x_change < 0:
            car(carTurnL,x,y)
        else:
            car(carImg,x,y)

        blocks_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()
        if y > display_height - car_height or y < 0:
            crash()

        if block_starty > display_height:
            block_starty = -block_height
            block_startx = random.randrange(0, display_width - block_width)
            dodged += 1


        if (y > block_starty and y < block_starty + block_height) or (y + block_height > block_starty and y + car_height < block_starty+block_height):
            #print('y crossover')
            if (x > block_startx and x < block_startx + block_width) or (x+car_width > block_startx and x + car_width < block_startx+block_width):
                #print('x crossover')
                crash()


        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
