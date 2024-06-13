import pygame
import random

pygame.init()
#pygame.mixer.init()

pygame.display.set_caption("Snake")

SW, SH = 600, 600

BLOCK_SIZE = 50

FONT = pygame.font.SysFont(name=None, size=BLOCK_SIZE*2)

screen = pygame.display.set_mode((SW, SH))

clock = pygame.time.Clock()

running = True

pause = True

lastKey = pygame.K_d

IMAGE_TAIL = pygame.image.load('tail.png').convert_alpha()

IMAGE_APPLE = pygame.image.load('apple.png').convert_alpha()

IMAGE_HEAD_U = pygame.image.load('head.png').convert_alpha()
IMAGE_HEAD_D = pygame.transform.rotate(IMAGE_HEAD_U, 180)
IMAGE_HEAD_R = pygame.transform.rotate(IMAGE_HEAD_U, 270)
IMAGE_HEAD_L = pygame.transform.rotate(IMAGE_HEAD_U, 90)

colors = [pygame.Color('#569151'), pygame.Color('#4a7c45')]

#pygame.mixer.Channel(0).set_volume(0.2)
#pygame.mixer.Channel(0).play(pygame.mixer.Sound('background.mp3'), loops = -1)
#pygame.mixer.Channel(0).pause()

IMAGE_HEAD = IMAGE_HEAD_R

def drawGrid():
    isColor = 0
    
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

            color = random.randint(0,1)

            if isColor%2 == 0:
                pygame.draw.rect(screen, colors[0], rect)
            else:
                pygame.draw.rect(screen, colors[1], rect)
            isColor += 1
        isColor += 1

class Snake:
    def reset(self):
        global lastKey
        global IMAGE_HEAD
        
        self.x = BLOCK_SIZE
        self.y = BLOCK_SIZE

        self.xdir = 1
        self.ydir = 0

        self.dead = False

        self.head = IMAGE_HEAD.get_rect()
        self.tail = [IMAGE_TAIL.get_rect()]

        lastKey = pygame.K_d

        IMAGE_HEAD = IMAGE_HEAD_R

    def __init__(self):
        self.reset()
    
    def update(self):
        global lastKey
        global pause

        if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
            self.dead = True
        
        for tailPiece in self.tail:
            if self.head.x == tailPiece.x and self.head.y == tailPiece.y and pause == False:
                self.dead = True
        
        if self.dead == True:
            last_score_font = FONT.render(f"Last score: {len(snake.tail) + 1}", True, pygame.Color('#70b76a'))
            last_score_rect = last_score_font.get_rect(center=(SW/2, SH/2))
            
            global apple

            apple = Apple()
            
            self.reset()

            lastKey = pygame.K_d

            pause = True

            #pygame.mixer.Channel(0).stop()
            #pygame.mixer.Channel(0).play(pygame.mixer.Sound('background.mp3'), loops = -1)
            #pygame.mixer.Channel(0).pause()
            
            screen.blit(last_score_font, last_score_rect)
            pygame.display.update()

        self.tail.append(self.head)

        for i in range(len(self.tail)-1):
            self.tail[i].x = self.tail[i+1].x
            self.tail[i].y = self.tail[i+1].y

        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE

        self.tail.remove(self.head)

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE

        self.loc = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        screen.blit(IMAGE_APPLE, self.loc)

snake = Snake()

apple = Apple()

score_font = FONT.render("1", True, "white")
score_rect = score_font.get_rect(center=(SW/2, SH/20 + 20))

pause_font = FONT.render("Press SPACE", True, pygame.Color('#70b76a'))
pause_rect = pause_font.get_rect(center=(SW/2, SH/2))

drawGrid()

pygame.display.update()

while running:
    drawGrid()

    snake.update()

    apple.update()

    screen.blit(IMAGE_HEAD, snake.head)

    for tailPiece in snake.tail:
        screen.blit(IMAGE_TAIL, tailPiece)

    score_font = FONT.render(f"{len(snake.tail) + 1}", True, "white")
    screen.blit(score_font, score_rect)

    screen.blit(pause_font, pause_rect)

    pygame.display.update()
    clock.tick(7)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        #pygame.mixer.Channel(1).play(pygame.mixer.Sound('gnam.mp3'))

        snake.tail.append(pygame.Rect(tailPiece.x, tailPiece.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()


    keyPressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if keyPressed == False:
                keyPressed = True

                if event.key == pygame.K_SPACE:
                    pause = True
                    #pygame.mixer.Channel(0).pause()
                    pause_font = FONT.render("Press SPACE to play", True, pygame.Color('#70b76a'))
                    screen.blit(pause_font, pause_rect)
                    pygame.display.update()

                elif event.key == pygame.K_s:
                    if lastKey != pygame.K_w:
                        IMAGE_HEAD = IMAGE_HEAD_D
                        snake.ydir = 1
                        snake.xdir = 0
                        lastKey = pygame.K_s
                    
                elif event.key == pygame.K_w:
                    if lastKey != pygame.K_s:
                        IMAGE_HEAD = IMAGE_HEAD_U
                        snake.ydir = -1
                        snake.xdir = 0
                        lastKey = pygame.K_w

                elif event.key == pygame.K_d:
                    if lastKey != pygame.K_a:
                        IMAGE_HEAD = IMAGE_HEAD_R
                        snake.ydir = 0
                        snake.xdir = 1
                        lastKey = pygame.K_d

                elif event.key == pygame.K_a:
                    if lastKey != pygame.K_d:
                        IMAGE_HEAD = IMAGE_HEAD_L
                        snake.ydir = 0
                        snake.xdir = -1
                        lastKey = pygame.K_a

    while pause:
        e = pygame.event.get()

        for event in e:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                pause = not pause
                #pygame.mixer.Channel(0).unpause()
                pause_font = FONT.render("", True, pygame.Color('#70b76a'))
                screen.blit(pause_font, pause_rect)
                pygame.display.update()

  
