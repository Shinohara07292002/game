import pygame
import random
import itertools
import sys


pygame.init()

# Dimensions of the screen
WIDTH, HEIGHT = 600, 500

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font('freesansbold.ttf', 15)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し")

# to control the frame rate
clock = pygame.time.Clock()
FPS = 30



# Ball Class
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = 1

        self.ball = pygame.draw.circle(
            screen,
            self.color,
            (self.posx, self.posy),
            self.radius
            )
        
        # Used to display the object on the screen
    def display(self):
        self.ball = pygame.draw.circle(
            screen,
            self.color,
            (self.posx,self.posy),
            self.radius
            )
        
        # Used to update the state of the object
    def update(self):
        self.posx += self.xFac*self.speed
        self.posy += self.yFac*self.speed

        # Reflecting the ball if it touches
        # either of the vertical edges
        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1

        # Reflection from the top most edge of the screen
        if self.posy <= 0:
            self.yFac *= -1

        # If the ball touches the bottom most edge of
        # the screen, True value is returned
        if self.posy >= HEIGHT:
            return True

        return False
    
    # Resets the position of the ball
    def reset(self):
        self.posx = 0
        self.posy = HEIGHT
        self.xFac, self.yFac = 1, -1
    
    def hit(self):
        self.yFac *= -1
    
    def getRect(self):
        return self.ball        

class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.color = color
        self.damage = 100
        if color == WHITE:
            self.health=200
        elif color == RED:
            self.health=300
        else:
            self.health=100    
            
        # self.health = 200 if color == WHITE  else 300 if color == RED else 100
        self.blockRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.block = pygame.draw.rect(screen, self.color, self.blockRect)        
    def display(self):
        if self.health > 0:
            self.brick = pygame.draw.rect(screen, self.color, self.blockRect)
    def getRect(self):
        return self.blockRect
    def getHealth(self):
        return self.health
    def hit(self):
        self.health -= self.damage

# Striker class
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        # The rect variable is used to handle the placement
        # and the collisions of the object
        self.strikerRect = pygame.Rect(
            self.posx,
            self.posy,
            self.width,
            self.height
            )
        self.striker = pygame.draw.rect(
            screen,
            self.color,
            self.strikerRect
            )
    # Used to render the object on the screen
    def display(self):
        self.striker = pygame.draw.rect(
            screen,
            self.color,
            self.strikerRect
            )
        

    # Used to update the state of the object
    def update(self, xFac):
        self.posx += self.speed*xFac

        # Restricting the striker to be in between the 
        # left and right edges of the screen
        if self.posx <= 0:
            self.posx = 0
        elif self.posx+self.width >= WIDTH:
            self.posx = WIDTH-self.width

        self.strikerRect = pygame.Rect(
            self.posx,
            self.posy,
            self.width,
            self.height
            )

    # Returns the rect of the object
    def getRect(self):
        return self.strikerRect

def populateBlocks(block_w, block_h, h_Gap, v_Gap, ratio=(0.5, 0.3, 0.2)):
    listOfBlocks = []
    ws = range(0, WIDTH, block_w+h_Gap)
    hs = range(0, HEIGHT//2, block_h+v_Gap)
    blocktotal = len(ws) * len(hs)
    red_total = int(blocktotal*ratio[2])
    white_total = int(blocktotal*ratio[1])
    green_total = blocktotal - (red_total + white_total)
    red_add = 0
    white_add = 0
    green_add = 0
    block_pos = [[i, j] for i, j in itertools.product(ws, hs)]
    
    while red_add <= red_total and white_add <= white_total and green_add <= green_total:
        color = random.choice([WHITE, GREEN, RED])
        span = len(block_pos)-1
        if color == RED:
            if red_add == red_total:
                continue
            else:
                red_add += 1
        elif color == WHITE:
            if white_add == white_total:
                continue
            else:
                white_add += 1
        elif color == GREEN:
            if green_add == green_total:
                continue
            else:
                green_add += 1
        n = random.randint(0, span)
        i, j = block_pos[n]
        listOfBlocks.append(Block(i, j, block_w, block_h, color))
        del block_pos[n]
        if len(block_pos) == 0: break
    return listOfBlocks    

def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True
    return False

def gameOver():
    gameOver = True
    while gameOver:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

def main():
    running = True
    striker = Striker(0, HEIGHT-50, 100, 20, 10, WHITE)
    strikerXFac = 0
    ball = Ball(0, HEIGHT-150, 7, 5, WHITE)
    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20
    listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)
    lives = 3
    score = 0
    livesText = font.render("Lives", True, WHITE)
    livesTextRect = livesText.get_rect()
    livesTextRect.center = (120, HEIGHT-10)
    
    scoreText = font.render("score", True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (20, HEIGHT-10)

    while running:
        screen.fill(BLACK)
        screen.blit(livesText, livesTextRect)
        screen.blit(scoreText, scoreTextRect)
        livesText = font.render("Lives : " + str(lives), True, WHITE)
        scoreText = font.render("Score : " + str(score), True, WHITE)
        if not listOfBlocks:
            listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)
        if lives <= 0:
            running = gameOver()
            while listOfBlocks:
                listOfBlocks.pop(0)
                lives = 3
                listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    strikerXFac = -1
                elif event.key == pygame.K_RIGHT:
                    strikerXFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0
                    
        if (collisionChecker(striker.getRect(),ball.getRect())):
            ball.hit()
        
        for block in listOfBlocks:
            if (collisionChecker(block.getRect(), ball.getRect())):
                ball.hit()
                block.hit()
                
                if block.getHealth() <= 0:
                    listOfBlocks.pop(listOfBlocks.index(block))
            
        # Update
        striker.update(strikerXFac)
        lifeLost = ball.update()
        if lifeLost:
            lives -= 1
            ball.reset()
        # Display
        striker.display()
        ball.display()
        for block in listOfBlocks:
            block.display()
        
        pygame.display.update()
        
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()



