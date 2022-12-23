import pygame
from sys import exit
from random import randint, choice

score = 0
game_over_score = 0
game_active = False


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        run1 = pygame.image.load('images/dino_run1.xcf').convert_alpha()
        run2 = pygame.image.load('images/dino_run2.xcf').convert_alpha()
        crawl1 = pygame.image.load('images/default/dino_crawl.png').convert_alpha()
        crawl2 = pygame.image.load('images/dino_crawl2.xcf').convert_alpha()
        self.stand = pygame.image.load('images/default/1-night.png').convert_alpha()
        self.frames = [run1, run2]
        self.crawl_frames = [crawl1, crawl2]
        self.frame_index = 0

        self.jump_sound = pygame.mixer.Sound('sounds/jump_mario.wav')
        self.jump_sound.set_volume(0.5)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(200, 525))
        
        self.isCrawling = False

        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom == 525 and not self.isCrawling:
            self.gravity = -22
            self.jump_sound.play()
            self.isCrawling = False
        elif keys[pygame.K_s] and self.rect.bottom == 525:
            self.isCrawling = True
        else:
            self.isCrawling = False

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 525:
            self.rect.bottom = 525

    def animate_run(self):

        if self.rect.bottom < 525:
            self.image = self.stand
        else:
            self.frame_index += 0.2
            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            if self.isCrawling:
                self.image = self.crawl_frames[int(self.frame_index)]
            else:
                self.image = self.frames[int(self.frame_index)]

            self.rect = self.image.get_rect(midbottom=(200, 525))

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate_run()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        # images
        cactus = pygame.image.load('images/default/4-green.png').convert_alpha()
        red_bird = pygame.image.load('images/bird.xcf').convert_alpha()
        purple_bird = pygame.image.load('images/bird_purple.xcf').convert_alpha()
        yellow_bird = pygame.image.load('images/bird_yellow.xcf').convert_alpha()

        if type == 'Cactus':
            self.image = cactus
            y_position = 525
            self.speed = 10
        else:
            if type == 'bird_low':
                y_position = 525
            elif type == 'bird_mid':
                y_position = 425
            elif type == 'bird_high':
                y_position = 350
            else:
                y_position = 300
            self.image = choice([red_bird, purple_bird, yellow_bird])
            self.speed = 10

        self.rect = self.image.get_rect(midbottom=(randint(1400, 1600), y_position))

    def update(self):
        self.destroy()
        self.rect.x -= self.speed

    def destroy(self):
        # variables that I use to show score
        global score, game_over_score

        if self.rect.x <= -100:
            score += 1
            game_over_score += 1
            self.kill()


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Dino')
font = pygame.font.Font('font/font.ttf', 100)
clock = pygame.time.Clock()

# intro surfaces
background = pygame.image.load('images/sky.png').convert()
background = pygame.transform.scale(background, (1280, 720))
dino_stand = pygame.image.load('images/default/1-night.png').convert_alpha()
dino_stand_rectangle = dino_stand.get_rect(center=(640, 350))
game_title = font.render('DINO', False, 'Black')
game_title_rectangle = game_title.get_rect(center=(640, 175))

# background
ground_surface = pygame.image.load('images/ground.png').convert()
sky_surface = pygame.image.load('images/sky.png').convert()

# clouds
cloud_surface = pygame.image.load('images/cloud.xcf').convert_alpha()
cloud_rectangle = cloud_surface.get_rect()
cloud_rect_list = []

text_surface = font.render('GAME OVER', False, 'Black').convert()
text_rectangle = text_surface.get_rect(center=(640, 150))
text_outro = font.render('Press SPACE to PLAY', False, 'Black')
text_outro_rectangle = text_outro.get_rect(center=(640, 500))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1800)
cloud_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cloud_timer, 1000)

# music
background_music = pygame.mixer.Sound('music/background_mario.mp3')
background_music.set_volume(0.25)

# sounds
game_over = pygame.mixer.Sound('sounds/die.wav')

# sprite groups
dino = pygame.sprite.GroupSingle()
dino.add(Dino())
obstacle_group = pygame.sprite.Group()


def cloud_generator(cloud_list):
    if cloud_list:
        for cloud_rect in cloud_list:
            cloud_rect.x -= 1

            screen.blit(cloud_surface, cloud_rect)

        cloud_list = [cloud for cloud in cloud_list if cloud.x > -100]

        return cloud_list

    else:
        return []


def show_intro():
    screen.blit(background, (0, 0))
    screen.blit(dino_stand, dino_stand_rectangle)
    screen.blit(game_title, game_title_rectangle)
    game_over_score_surface = font.render(f'Your Score: {game_over_score}', False, 'Black')
    game_over_score_rectangle = game_over_score_surface.get_rect(center=(640, 600))
    screen.blit(game_over_score_surface, game_over_score_rectangle)
    screen.blit(text_outro, text_outro_rectangle)


def show_score():
    score_surface = font.render(f'Score:  {score}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(topleft=(10, 10))
    screen.blit(score_surface, score_rectangle)


def collision_sprite():
    if not pygame.sprite.spritecollide(dino.sprite, obstacle_group, False):
        return True
    else:
        pygame.mixer.stop()
        game_over.play()
        obstacle_group.empty()
        return False


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                score = 0
                game_over_score = 0
                # stop playing game over sound and play music
                pygame.mixer.stop()
                background_music.play(loops=-1)

        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacles(choice(['Cactus', 'Cactus', 'Cactus', choice(['bird_high', 'bird_low', 'bird_mid'])])))

        if event.type == cloud_timer:
            cloud_rect_list.append(cloud_surface.get_rect(bottomright=(randint(1400, 1600), randint(75, 175))))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 520))

        # draw sprites
        dino.draw(screen)
        dino.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # cloud movement
        cloud_rect_list = cloud_generator(cloud_rect_list)

        # if there is no collision continue
        game_active = collision_sprite()

        show_score()

    else:
        show_intro()

        cloud_rect_list = cloud_generator(cloud_rect_list)

    pygame.display.update()

    clock.tick(60)
