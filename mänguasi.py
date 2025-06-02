import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Run")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_HEIGHT = HEIGHT - 40

star_width, star_height = 30, 30

dino_width, dino_height = 100, 80
dino_x = 50
dino_y = GROUND_HEIGHT - dino_height + 10
dino_vel_y = 0
gravity = 1
jump_power = -15
on_ground = True

cactus_width, cactus_height = 40, 60
cactus_list = []
cactus_spawn_time = 0
cactus_spawn_delay = 1500

bird_width, bird_height = 30, 20
bird_list = []
bird_spawn_time = 0
bird_spawn_delay = 10000
bird_fly_height = [GROUND_HEIGHT - 100, GROUND_HEIGHT - 150]

star_list = []
star_spawn_time = 0
star_spawn_delay = 7000  

speed = 10
speed_increase_interval = 10000
last_speed_increase = 0

score = 0
stars_collected = 0
game_over = False


invincible = False
invincible_start_time = 0
invincible_duration = 5000


kkk_img = pygame.image.load("kkk.png")
kkk_img = pygame.transform.scale(kkk_img, (dino_width, dino_height))

kk2_img = pygame.image.load("kk2.png")
kk2_img = pygame.transform.scale(kk2_img, (dino_width, dino_height))

cactus_img = pygame.image.load("cactus.png")
cactus_img = pygame.transform.scale(cactus_img, (cactus_width, cactus_height))

zvezda_img = pygame.image.load("svesda.png").convert_alpha()
zvezda_img = pygame.transform.scale(zvezda_img, (star_width, star_height))


fon_img = pygame.image.load("fon.png").convert_alpha()
fon_img = pygame.transform.scale(fon_img, (WIDTH, HEIGHT))


def draw_ground_and_background():
    screen.blit(fon_img, (0, 0)) 


while True:
    if game_over:
        screen.fill(WHITE)
        game_over_text = font.render("Mäng läbi! Vajuta R uuesti alustamiseks", True, BLACK)
        score_text = font.render(f"Skoor: {score}  Tähed: {stars_collected}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                dino_y = GROUND_HEIGHT - dino_height + 10
                dino_vel_y = 0
                on_ground = True
                cactus_list.clear()
                bird_list.clear()
                star_list.clear()
                score = 0
                stars_collected = 0
                cactus_spawn_time = pygame.time.get_ticks()
                bird_spawn_time = pygame.time.get_ticks()
                star_spawn_time = pygame.time.get_ticks()
                speed = 10
                last_speed_increase = pygame.time.get_ticks()
                game_over = False
                invincible = False
                invincible_start_time = 0
        continue

    clock.tick(60)
    draw_ground_and_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        dino_vel_y = jump_power
        on_ground = False

    dino_vel_y += gravity
    dino_y += dino_vel_y

    if dino_y >= GROUND_HEIGHT - dino_height + 10:
        dino_y = GROUND_HEIGHT - dino_height + 10
        dino_vel_y = 0
        on_ground = True

    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)

    now = pygame.time.get_ticks()

    if invincible and now - invincible_start_time > invincible_duration:
        invincible = False

    if now - last_speed_increase > speed_increase_interval:
        speed += 1
        last_speed_increase = now

    if now - cactus_spawn_time > cactus_spawn_delay:
        cactus_x = WIDTH
        cactus_y = GROUND_HEIGHT - cactus_height
        cactus_list.append(pygame.Rect(cactus_x, cactus_y, cactus_width, cactus_height))
        cactus_spawn_time = now
        cactus_spawn_delay = random.randint(1200, 2000)

    if now - bird_spawn_time > bird_spawn_delay:
        bird_x = WIDTH
        bird_y = random.choice(bird_fly_height)
        bird_list.append(pygame.Rect(bird_x, bird_y, bird_width, bird_height))
        bird_spawn_time = now
        bird_spawn_delay = random.randint(7000, 12000)

    if now - star_spawn_time > star_spawn_delay:
        star_x = WIDTH
        star_y = random.randint(GROUND_HEIGHT - 200, GROUND_HEIGHT - 100)
        star_list.append(pygame.Rect(star_x, star_y, star_width, star_height))
        star_spawn_time = now
        star_spawn_delay = random.randint(6000, 9000)

    for cactus in cactus_list[:]:
        cactus.x -= speed
        if cactus.right < 0:
            cactus_list.remove(cactus)
            score += 1
        screen.blit(cactus_img, (cactus.x, cactus.y))
        if dino_rect.colliderect(cactus):
            if not invincible:
                game_over = True

    for bird in bird_list[:]:
        bird.x -= speed + 2
        if bird.right < 0:
            bird_list.remove(bird)
            score += 1
        pygame.draw.rect(screen, (150, 0, 0), bird)
        if dino_rect.colliderect(bird):
            if not invincible:
                game_over = True

    for star in star_list[:]:
        star.x -= speed
        if star.right < 0:
            star_list.remove(star)
        screen.blit(zvezda_img, (star.x, star.y))
        if dino_rect.colliderect(star):
            stars_collected += 1
            star_list.remove(star)
            invincible = True
            invincible_start_time = now


    if invincible:
        screen.blit(kk2_img, (dino_x, dino_y))
    else:
        screen.blit(kkk_img, (dino_x, dino_y))

    score_display = font.render(f"Skoor: {score}  Tähed: {stars_collected}", True, BLACK)
    screen.blit(score_display, (10, 10))

    pygame.display.flip()
