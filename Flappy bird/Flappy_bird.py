import pygame
import sys
import random

# функции для труб


def create_pipe():
    random_pipe_pose = random.choice(pipe_height)
    new_pipe = pipe_surface.get_rect(midtop=(350, random_pipe_pose))
    top_pipe = pipe_surface.get_rect(midbottom=(350, random_pipe_pose - 150))
    return new_pipe, top_pipe


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False
    return True


# функции для
# пола


def draw_floor():
    screen.blit(flor_surface, (florX_pose, 450))
    screen.blit(flor_surface, (florX_pose + 288, 450))


# фунуции птицы


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 4, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


# функции очков


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'SCORe : {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(150, 50))
        screen.blit(score_surface, score_rect)

        gameover_surface = game_font2.render('Game over', True, (255, 0, 0))
        gameover_rect = gameover_surface.get_rect(center=(150, 220))
        screen.blit(gameover_surface, gameover_rect)

        tape_surface = game_font3.render('TaPe tO RestaRt', True, (255, 255, 100))
        tape_rect = tape_surface.get_rect(center=(150, 250))
        screen.blit(tape_surface, tape_rect)

        high_score_surface = game_font.render(f'BesT SCORe : {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(120, 425))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()

screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 20)
game_font2 = pygame.font.Font('04B_19.TTF', 30)
game_font3 = pygame.font.Font('04B_19.TTF', 12)

# иконка и название
pygame.display.set_caption("Flappy bird")
icon = pygame.image.load('assets/yellowbird-upflap.png')
pygame.display.set_icon(icon)


# игровые переменные
graviti = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# фоновая поверхность
bg_surface = pygame.image.load('assets//background-day.png').convert()

# переменные земли
flor_surface = pygame.image.load('assets/base.png')
florX_pose = 0

# переменные птицы
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_serface = bird_frames[bird_index]
bird_rect = bird_serface.get_rect(center=(50, 256))


BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# переменные + события труб
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

# игровой цикл
while True:
    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_serface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    # действие игры
    if game_active:
        # птица
        bird_movement += graviti
        rotated_bird = rotate_bird(bird_serface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # движение земли
        florX_pose -= 5

        # препядствия
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # очки
        score += 0.007
        score_display('main_game')
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')

    # зелмя
    draw_floor()
    if florX_pose <= -288:
        florX_pose = 0

    # запуск
    pygame.display.update()
    clock.tick(120)
