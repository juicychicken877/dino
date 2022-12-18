import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Dino')
font = pygame.font.Font('font/font.ttf', 100)
clock = pygame.time.Clock()

score = 0
game_over_score = 0

# intro surfaces
background = pygame.image.load('images/sky.png').convert()
background = pygame.transform.scale(background, (1280, 720))
dino_stand = pygame.image.load('images/1-night.png').convert_alpha()
dino_stand_rectangle = dino_stand.get_rect(center=(640, 350))
game_title = font.render('DINO', False, 'Black')
game_title_rectangle = game_title.get_rect(center=(640, 175))

# surfaces && rectangles
ground_surface = pygame.image.load('images/ground.png').convert()
sky_surface = pygame.image.load('images/sky.png').convert()

# clouds
cloud_surface = pygame.image.load('images/cloud.xcf').convert_alpha()
cloud_rectangle = cloud_surface.get_rect()

obstacle_rect_list = []
cloud_rect_list = []

text_surface = font.render('GAME OVER', False, 'Black').convert()
text_rectangle = text_surface.get_rect(center=(640, 150))
text_outro = font.render('Press SPACE to PLAY', False, 'Black')
text_outro_rectangle = text_outro.get_rect(center=(640, 500))

# dino
dino_run1 = pygame.image.load('images/dino_run1.xcf').convert_alpha()
dino_run2 = pygame.image.load('images/dino_run2.xcf').convert_alpha()
dino_run = [dino_run1, dino_run2]
dino_index = 0
dino_surface = dino_run[dino_index]
dino_rectangle = dino_surface.get_rect(midbottom=(100, 525))
dino_gravity = 0

cactus_surface = pygame.image.load('images/4-green.png').convert_alpha()

game_active = False

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1700)
cloud_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cloud_timer, 1000)


def cloud_generator(cloud_list):
    if cloud_list:
        for cloud_rect in cloud_list:
            cloud_rect.x -= 5

            screen.blit(cloud_surface, cloud_rect)

        obstacle_list = [cloud for cloud in cloud_list if cloud.x > -100]

        return cloud_list

    else:
        return[]


def show_intro():
    screen.blit(background, (0, 0))
    screen.blit(dino_stand, dino_stand_rectangle)
    screen.blit(game_title, game_title_rectangle)


def show_score():
    score_surface = font.render(f'Score:  {score}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(topleft=(10, 10))
    screen.blit(score_surface, score_rectangle)


def obstacle_movement(obstacle_list):
    global score, game_over_score

    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10

            if obstacle_rect.x <= -100:
                score += 1

            # depending on y draw a proper image

            screen.blit(cactus_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list

    else:
        return[]


def isCollision(dino, obstacles):
    global score, game_over_score
    if obstacles:
        for obstacle_rect in obstacles:
            if dino.colliderect(obstacle_rect):
                game_over_score = score
                score = 0
                return False

    return True


def dino_animate():
    global dino_surface, dino_index

    if dino_rectangle.bottom < 525:
        pass

    else:
        dino_index += 0.2
        if dino_index >= len(dino_run):
            dino_index = 0
        dino_surface = dino_run[int(dino_index)]


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            # the player can only jump if he is on the ground
            if event.key == pygame.K_SPACE and dino_rectangle.bottom == 525:
                dino_gravity = -22
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                dino_rectangle.bottom = 525
                dino_gravity = 0
                obstacle_rect_list.clear()

        if event.type == obstacle_timer and game_active:
            obstacle_rect_list.append(cactus_surface.get_rect(bottomright=(randint(1400, 1600), 525)))

        if event.type == cloud_timer:
            cloud_rect_list.append(cloud_surface.get_rect(bottomright=(randint(1400, 1600), randint(75, 125))))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 520))
        screen.blit(dino_surface, dino_rectangle)

        # players' gravity
        dino_rectangle.y += dino_gravity
        dino_gravity += 1
        if dino_rectangle.bottom > 525:
            dino_rectangle.bottom = 525

        dino_animate()

        # cactus / fly movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        cloud_rect_list = cloud_generator(cloud_rect_list)

        # if collision then game_active == false (game stops)
        game_active = isCollision(dino_rectangle, obstacle_rect_list)

        show_score()

    else:
        show_intro()

        cloud_rect_list = cloud_generator(cloud_rect_list)
        game_over_score_surface = font.render(f'Your Score: {game_over_score}', False, 'Black')
        game_over_score_rectangle = game_over_score_surface.get_rect(center=(640, 600))
        screen.blit(game_over_score_surface, game_over_score_rectangle)
        screen.blit(text_outro, text_outro_rectangle)

    pygame.display.update()

    clock.tick(60)

    clock.tick(60)
