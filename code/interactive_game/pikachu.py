import pygame
import time
import os

#pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.mixer.init()
pygame.init()

#display dimensions
display_width = 800
display_height = 600

#initialising window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Interactive Wall')
clock = pygame.time.Clock()

#colours
white = (0,0,0)

def load_image(name):
    image = pygame.image.load(name)
    return image

class animatedSprite(pygame.sprite.Sprite):
    def __init__(self, posx, posy, dir, sound_name, scale_factor):
        super(animatedSprite, self).__init__()
        self.images = []
        num_frames = len([name for name in os.listdir(dir)])
        for i in range(num_frames):
            self.images.append(load_image('./' + dir + '/' + str(i+1) + '.png'))
            self.images[i] = pygame.transform.scale(self.images[i],(int(self.images[i].get_rect().size[0] * scale_factor), int(self.images[i].get_rect().size[1] * scale_factor)))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        # self.rect.x = 350
        # self.rect.y = 250
        self.rect.center = (posx,posy)
        self.sound = pygame.mixer.Sound(sound_name)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

def load_sprite(sprite):
    gameDisplay.blit(sprite.images[sprite.index],sprite.rect)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if sprite.rect.x + sprite.rect.size[0] > mouse[0] > sprite.rect.x and sprite.rect.y + sprite.rect.size[1] > mouse[1] > sprite.rect.y:
        if(click[0]):
            pygame.mixer.Sound.stop(sprite.sound)
            #pygame.mixer.Sound.play(sprite.sound)
            sprite.sound.play(-1,4000)
            for i in range(50):
                gameDisplay.fill(white)
                sprite.update()
                pygame.sprite.Group(sprite).draw(gameDisplay)
                pygame.time.wait(50)
                pygame.display.update()
            pygame.mixer.Sound.stop(sprite.sound)

def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        #animatedSprite(posx, posy, dir, sound_name, scale_factor)
        pika_sprite = animatedSprite(600,100,'Pika 2','pikaSound.wav', 1)
        snoop_sprite = animatedSprite(200,400,'Snoop','snoop.wav', 0.5)
        iron_sprite = animatedSprite(600,400,'ironman','ironsound.wav',0.5)
        pewds_sprite = animatedSprite(200,100,'Pewds','lasagna.wav',1)

        load_sprite(pika_sprite)
        load_sprite(snoop_sprite)
        load_sprite(iron_sprite)
        load_sprite(pewds_sprite)

        pygame.display.update()
        clock.tick(30)
game_loop()
