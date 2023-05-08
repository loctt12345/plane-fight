import pygame
import os
import camera_control
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
HEAL_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
ENERMY_APPEAR_TIME = 100
BULLET_VEL = 7
ENERMY_VEL = 4
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
ENERMY_WIDTH, ENERMY_HEIGHT = 40, 30

YELLOW_HIT = pygame.USEREVENT + 1
ENERMY_HIT = pygame.USEREVENT + 2


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) 

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (ENERMY_WIDTH, ENERMY_HEIGHT)), 270) 


SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_window(yellow, yellow_bullets, yellow_health, point, enermies):
    WIN.blit(SPACE, (0, 0))
    
    yellow_heal_text = HEAL_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    point_text = HEAL_FONT.render("Point: " + str(point), 1, WHITE)

    WIN.blit(yellow_heal_text, (10, 10))
    WIN.blit(point_text, (yellow_heal_text.get_width() + 100, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for enermy in enermies:
        WIN.blit(RED_SPACESHIP, (enermy.x, enermy.y))

    pygame.display.update()

def yellow_handle_movement(yellow):
    pos = camera_control.play()
    if len(pos) > 0:
        (mouseX, mouseY) = pos[0][0], pos[0][1]
        yellow.x = max(0, min(mouseX, WIDTH - yellow.width))
        yellow.y = max(0, min(mouseY, HEIGHT - yellow.height))

def enermy_handle_movement(enermies):
    for enermy in enermies:
        if (enermy.x - ENERMY_VEL < 0):
            enermies.remove(enermy)
        enermy.x -= ENERMY_VEL

def handle_bullets(yellow_bullets, yellow, enermies):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        for enermy in enermies:
            if enermy.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENERMY_HIT))
                yellow_bullets.remove(bullet)
                enermies.remove(enermy)
                break

        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

def handle_enermy_touch(yellow, enermies):
    for enermy in enermies:
        if yellow.colliderect(enermy):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))

def main():
    camera_control.play()
    turn = 0
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    yellow_bullets = []
    enermies = []

    yellow_health = 10
    point = 0
    immortal = False
    time_immortal = 0
    enermy_appear_time = ENERMY_APPEAR_TIME

    clock = pygame.time.Clock()
    run = True
    while (run):
        clock.tick(FPS)
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                immortal = True
            if event.type == ENERMY_HIT:
                point += 5
        
        winner_text = ""

        if yellow_health <= 0:
            winner_text = "You lose!" 

        if winner_text != "":
            draw_winner(winner_text)
            break
        
        turn += 1
        if (turn % 10 == 0):
            bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
            yellow_bullets.append(bullet)

        if (turn % enermy_appear_time == 0):
            enermy = pygame.Rect(800, random.randint(ENERMY_HEIGHT, HEIGHT - ENERMY_HEIGHT), ENERMY_WIDTH, ENERMY_HEIGHT)
            enermies.append(enermy)

        if (turn % 100 == 0):
            enermy_appear_time = max(10, enermy_appear_time - 2)

        if (immortal):
            time_immortal +=1
            if time_immortal == 20:
                immortal = False
                time_immortal = 0

        yellow_handle_movement(yellow)
        enermy_handle_movement(enermies)
        if immortal == False:
            handle_enermy_touch(yellow, enermies)

        handle_bullets(yellow_bullets,yellow, enermies)

        draw_window( yellow, yellow_bullets,  yellow_health, point, enermies)
    pygame.quit()

if __name__ == "__main__":
    main()