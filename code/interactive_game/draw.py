import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Drawing')

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)

gameDisplay.fill(black)

pixAr = pygame.PixelArray(gameDisplay)
pixAr[1][0:20] = green
pygame.draw.line(gameDisplay,blue,(100,200),(300,450),10)
pygame.draw.rect(gameDisplay,red,(350,250,100,100))
pygame.draw.circle(gameDisplay,white,(150,150),75,1)
pygame.draw.polygon(gameDisplay,green,((0,0),(750,200),(50,50),(150,20)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
