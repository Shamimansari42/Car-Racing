#importing module
import random
import pygame
import  os

#start game
pygame.init()

#screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# clock
clock = pygame.time.Clock()
fps = 60

#others
bg_scroll = 0
MOVING_ENEMY = 0
fade_counter = 0

#score saving at car_game_score.txt
if os.path.exists('car_game_score.txt'):
    with open('car_game_score.txt', 'r') as file:
        high_score = score = int(file.read())
else:
    high_score = 0

score = 0
game_over = False

#COLOUR
WHITE = (255, 255, 255)
BLACK = (0,0,0)

#font
font_small = pygame.font.SysFont('Calibri',20)
font_big = pygame.font.SysFont('Calibri',25)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Welcome to Shamim Car Race')

#Track image
track_img = pygame.image.load('D:\\Shamim\\Data Science\\python training\\car game\\images\\track.jpg').convert_alpha()
track = pygame.transform.scale(track_img, (SCREEN_WIDTH,SCREEN_HEIGHT))

def draw_text(text, font, text_col, x, y): #function to display letters on screen
    img = font.render(text, font, True, text_col)
    screen.blit(img, (x,y))

def draw_panel():     #function to display panel for score and high score
    pygame.draw.rect(screen,WHITE,(0,0, SCREEN_HEIGHT, 30))
    pygame.draw.line(screen, WHITE, (0,30), (SCREEN_WIDTH, 30))
    if score < high_score:
     draw_text('score:' + str(score), font_small, WHITE, 0,5)
    else:
        draw_text('High Score:' + str(score), font_small, WHITE, 0, 5)


#background motion
def background_move(bg_scroll):
    screen.blit(track, (0,0 + bg_scroll))
    screen.blit(track,(0,-600 + bg_scroll))

# player
class Player():
    def __init__(self, x, y):
        self.image = pygame.image.load('D:\\Shamim\\Data Science\\python training\\car game\\images\\player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self): #Controls
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            dx += 5
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_UP]:
            dy -= 5
        if key[pygame.K_DOWN]:
            dy +=5
        if self.rect.top + dy < 0:
            dy = self.rect.top

        #update screen
        self.rect.x += dx
        self.rect.y += dy

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        screen.blit(self.image, self.rect)

#enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        enemy_1 = pygame.transform.scale(pygame.image.load('D:\\Shamim\\Data Science\\python training\\car game\\images\\enemy3.png'), (120,100))
        enemy_2 = pygame.transform.scale(pygame.image.load('D:\\Shamim\\Data Science\\python training\\car game\\images\\enemy0.png'), (50, 90))
        enemy_3 = pygame.transform.scale(pygame.image.load('D:\\Shamim\\Data Science\\python training\\car game\\images\\enemy9.png'), (80, 90))
        enemy_lib = [enemy_1, enemy_2, enemy_3]
        enemy_choose = random.choice(enemy_lib)
        self.image = enemy_choose
        self.rect = self.image.get_rect()
        self.move = MOVING_ENEMY
        self.rect.x = x
        self.rect.y = y
    def update(self, MOVING_ENEMY): #Enemy movement
        self.rect.y  += MOVING_ENEMY
        if self.rect.top > SCREEN_HEIGHT :
            self.kill()

#calling player and enemy
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT-150)
enemy_group = pygame.sprite.Group()

# LOOP
run = True
while run :
    clock.tick(fps)
    if game_over == False:
        bg_scroll += 5
        print(MOVING_ENEMY)
        MOVING_ENEMY = 1
        background_move(bg_scroll)
        if score < 100:
            MAX_ENEMY = 1
            if len(enemy_group) < MAX_ENEMY:
                p_x = random.randint(0, SCREEN_WIDTH)
                enemy = Enemy(p_x, 0)
                enemy_group.add(enemy)

        elif 300 > score > 100:
            MAX_ENEMY = 2
            if len(enemy_group) < MAX_ENEMY:
                p_x = random.randint(0, SCREEN_WIDTH)
                enemy = Enemy(p_x, 50)
                enemy_group.add(enemy)
                enemy_group.add(enemy)
        else:
            MAX_ENEMY = 3
            if len(enemy_group) < MAX_ENEMY:
                p_x = random.randint(0, SCREEN_WIDTH- 50)
                enemy = Enemy(p_x, 50)
                enemy_group.add(enemy)
                enemy_group.add(enemy)
        enemy_group.update(MOVING_ENEMY)
        enemy_group.draw(screen)

        if bg_scroll == SCREEN_HEIGHT:
            bg_scroll = 0
        if bg_scroll > 0:
            score += 1
            print(score)

        player.draw()
        player.move()
        draw_panel()

    #colision
        if pygame.sprite.spritecollide(player, enemy_group, False):
            if pygame.sprite.spritecollide(player, enemy_group,False, pygame.sprite.collide_mask):
                game_over = True

        if player.rect.top == SCREEN_HEIGHT:
            game_over = True

        if player.rect.left == 0:
            game_over = True

        if player.rect.right == SCREEN_WIDTH:
            game_over = True

    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for  y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK,(0,y * (SCREEN_HEIGHT/6),fade_counter,SCREEN_HEIGHT/6))
                pygame.draw.rect(screen,BLACK,(SCREEN_WIDTH - fade_counter , (y + 1) * (SCREEN_HEIGHT/6), SCREEN_WIDTH, SCREEN_HEIGHT/6))
        draw_text('Welcome to Shamim Car Race', font_big, WHITE, 130, 170)
        draw_text('GAME over', font_big, WHITE, 130,200)
        draw_text(f'Your Score = {score}', font_big, WHITE, 130, 230)
        draw_text(f'High Score = {high_score}', font_big, WHITE, 130, 260)
        draw_text('Press Space to start', font_big, WHITE, 130, 290)

        if score > high_score:
            high_score = score
            with open('car_game_score.txt', 'w') as file:
                file.write(str(high_score))

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            player.rect.x = SCREEN_WIDTH//2
            player.rect.y = SCREEN_HEIGHT-150
            bg_scroll = 0
            score = 0
            enemy_group.empty()
            fade_counter = 0



    for event in pygame.event.get():
        if event.type ==pygame.QUIT :
            run = False

    pygame.display.update()

pygame.quit()
