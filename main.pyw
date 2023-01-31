import pygame
import random

width,height = 400,600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Flappy Bird")

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(),40)

class Bird():
    def __init__(self):
        self.y = height//2
        self.vel = 0
        self.acc = 0
        self.r = 8

    def draw(self,win):
         
        self.acc += 0.0098
        self.vel += self.acc
        self.y   += self.vel

        if self.y >= height-50-self.r:
            self.y = height-50-self.r
            self.vel  = 0
            self.acc = 0
        elif self.y <= self.r:
            self.y = self.r
            self.vel = 0

        pygame.draw.circle(win,(255,0,0),(50,self.y),self.r)
    
    def jump(self):
        self.acc = 0
        self.vel = -4

class Pipe():
    def __init__(self):
        self.x = width + 20
        self.vel = 2
        self.y = random.randint(100,height-250)

    def update(self):
        self.x -= self.vel

    def draw(self,win):
        pygame.draw.rect(win,(0,150,0),(self.x,0,40,self.y))
        pygame.draw.rect(win,(0,150,0),(self.x,self.y+100,40,height-self.y-100-50))

pipes = []
pipes.append(Pipe())
bird = Bird()
dead = False
run = True
score = 0
clock = pygame.time.Clock()
while run:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dead:
                bird.jump()
            if event.key == pygame.K_RETURN and dead:
                pipes = []
                pipes.append(Pipe())
                bird = Bird()
                score = 0
                dead = False

    win.fill((255,255,255))

    for pipe in pipes:
        if pipe.x < -100:
            pipes.remove(pipe)
        elif pipe.x > width/2 - 1 and pipe.x < width/2 + 1:
            pipes.append(Pipe())

    for pipe in pipes:
        if pipe.x + 40 < 50 - bird.r and pipe.x + 40 > 47 - bird.r and not dead:
            score += 1
        if not dead:
            pipe.update()
        pipe.draw(win)

        if pipe.x < 50 + bird.r and pipe.x + 40 > 50 - bird.r and not dead:
            if bird.y - bird.r < pipe.y or bird.y + bird.r > pipe.y + 100:
                dead = True
                bird.vel = -8
                bird.acc = 0

    pygame.draw.rect(win,(100,100,100),(0,height-50,width,50))

    text = font.render("SCORE : " + str(score),True,(0,0,0))
    win.blit(text,(width/2-text.get_width()/2,height - 45))

    bird.draw(win)

    pygame.display.update()

pygame.quit()
exit()