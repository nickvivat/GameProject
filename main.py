import random
import sys
import time
import pygame
from button import Button

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

GRID_BLOCK = 20
SCORE = 0

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

icon = pygame.image.load("Pictures/Snake-3.png")
pygame.display.set_icon(icon)

big_fruit = pygame.image.load("Pictures/Fruit.png")
fruit = pygame.transform.scale(big_fruit, (GRID_BLOCK, GRID_BLOCK))

big_heart = pygame.image.load("Pictures/One_heart.png")
heart = pygame.transform.scale(big_heart, (GRID_BLOCK, GRID_BLOCK))

big_star = pygame.image.load("Pictures/star.png")
star = pygame.transform.scale(big_star, (GRID_BLOCK, GRID_BLOCK))

BLACK = (25, 25, 25)
WHITE = (220, 220, 220)
YELLOW = (227, 207, 87)
RED = (205, 51, 51)
VIOLET = (143, 0, 255)
BLUE = (93, 173, 226)

font_name = '8-BIT WONDER.TTF'
score_font_name = 'font.TTF'
score_font_style = pygame.font.Font(score_font_name, 40)

Menu_bg = pygame.image.load("Pictures/Menu-Background.jpg")
BG = pygame.transform.scale(Menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


def get_font(size):
    return pygame.font.Font(font_name, size)


def update_snake(snake_block, snake_list, head_color, body_color):
    for x in snake_list:
        if x == snake_list[len(snake_list) - 1]:
            pygame.draw.rect(SCREEN, head_color, [x[0], x[1], snake_block, snake_block])
        else:
            pygame.draw.rect(SCREEN, body_color, [x[0], x[1], snake_block, snake_block])


def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_BLOCK):
        for y in range(0, SCREEN_HEIGHT, GRID_BLOCK):
            rect = pygame.Rect(x, y, GRID_BLOCK, GRID_BLOCK)
            pygame.draw.rect(SCREEN, VIOLET, rect, 1)


def playing():
    pygame.display.set_caption("Snake Game 2.0")

    game_over = False

    SCREEN.fill(BLACK)
    draw_grid()

    score = 0
    life = 3

    start_life = pygame.image.load("Pictures/Three_heart.png")
    two_heart = pygame.image.load("Pictures/Two_heart.png")
    one_heart = pygame.image.load("Pictures/One_heart.png")

    display_life = pygame.transform.scale(start_life, (60, 20))

    x = SCREEN_HEIGHT / 2
    y = SCREEN_WIDTH / 2

    delta_x = 0
    delta_y = 0

    snake_body = []
    length_of_snake = 1

    fruit_x = round(random.randrange(20, SCREEN_WIDTH - 20) / GRID_BLOCK) * GRID_BLOCK
    fruit_y = round(random.randrange(20, SCREEN_HEIGHT - 20) / GRID_BLOCK) * GRID_BLOCK

    heart_x = round(random.randrange(20, SCREEN_WIDTH - 20) / GRID_BLOCK) * GRID_BLOCK
    heart_y = round(random.randrange(20, SCREEN_WIDTH - 20) / GRID_BLOCK) * GRID_BLOCK

    star_x = round(random.randrange(20, SCREEN_WIDTH - 20) / GRID_BLOCK) * GRID_BLOCK
    star_y = round(random.randrange(20, SCREEN_WIDTH - 20) / GRID_BLOCK) * GRID_BLOCK

    clock = pygame.time.Clock()

    while not game_over:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT and delta_x != GRID_BLOCK) or (event.key == pygame.K_a and delta_x != GRID_BLOCK):
                    delta_x = -GRID_BLOCK
                    delta_y = 0
                elif (event.key == pygame.K_RIGHT and delta_x != -GRID_BLOCK) or (event.key == pygame.K_d and delta_x != -GRID_BLOCK):
                    delta_x = GRID_BLOCK
                    delta_y = 0
                elif (event.key == pygame.K_UP and delta_y != GRID_BLOCK) or (event.key == pygame.K_w and delta_y != GRID_BLOCK):
                    delta_x = 0
                    delta_y = -GRID_BLOCK
                elif (event.key == pygame.K_DOWN and delta_y != -GRID_BLOCK) or (event.key == pygame.K_s and delta_y != -GRID_BLOCK):
                    delta_x = 0
                    delta_y = GRID_BLOCK
                elif event.key == pygame.K_ESCAPE:
                    pause()
                elif event.key == pygame.K_o:
                    game_over = True

            if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
                time.sleep(0.5)
                snake_body = []
                life -= 1
                x = SCREEN_WIDTH / 2
                y = SCREEN_HEIGHT / 2

            if life == 0:
                game_over = True

        x += delta_x
        y += delta_y

        score_display = score_font_style.render(f"Score : {score}", True, YELLOW)
        score_rect = score_display.get_rect(center=(SCREEN_WIDTH / 2 + 10, 20))

        if life >= 3:
            life = 3
            display_life = pygame.transform.scale(start_life, (60, 20))
        elif life == 2:
            display_life = pygame.transform.scale(two_heart, (40, 20))
        elif life == 1:
            display_life = pygame.transform.scale(one_heart, (20, 20))

        snake_head = [x, y]
        snake_body.append(snake_head)
        if len(snake_body) > length_of_snake:
            del snake_body[0]

        for i in snake_body[:-1]:
            if i == snake_head:
                time.sleep(0.5)
                snake_body = []
                life -= 1
                x = SCREEN_HEIGHT / 2
                y = SCREEN_WIDTH / 2

            if life == 0:
                game_over = True

        SCREEN.fill(BLACK)
        draw_grid()

        update_snake(GRID_BLOCK, snake_body, WHITE, WHITE)

        SCREEN.blit(fruit, (fruit_x, fruit_y))
        SCREEN.blit(score_display, score_rect)

        if score % 100 == 0 and score != 0:
            SCREEN.blit(star, (star_x, star_y))
            if x == star_x and y == star_y:
                score += 100
                star_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                star_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK

        if score % 3000 == 0 and score != 0:
            SCREEN.blit(heart, (heart_x, heart_y))
            if x == heart_x and y == heart_y:
                life += 1
                score += 100
                heart_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                heart_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK

        if life == 3:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 70, 10))
        elif life == 2:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 50, 10))
        elif life == 1:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 30, 10))
        elif life == 0:
            SCREEN.blit(display_life, (SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.update()

        if x == fruit_x and y == fruit_y:
            fruit_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
            fruit_y = round(random.randrange(60, SCREEN_HEIGHT - 60) / GRID_BLOCK) * GRID_BLOCK
            score += 100
            length_of_snake += 1

        pygame.display.update()
        clock.tick(15)

    global SCORE
    SCORE = score
    game_over_screen()


def game_over_screen():
    while True:
        pygame.mouse.set_visible(True)
        game_over_mouse_pos = pygame.mouse.get_pos()

        global SCORE
        SCREEN.fill(BLACK)
        pygame.display.set_caption("Snake Game 2.0 Game Over")
        button_load = pygame.image.load("Pictures/Button.png")

        game_over_text = get_font(50).render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect(center=(310, 100))
        SCREEN.blit(game_over_text, game_over_rect)

        score_display = score_font_style.render(f"Score : {SCORE}", True, WHITE)
        score_rect = score_display.get_rect(center=(SCREEN_WIDTH / 2 + 10, 160))
        SCREEN.blit(score_display, score_rect)

        play_again_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 320),
                                   text_input="Play Again", font=get_font(30),
                                   base_color=WHITE, hovering_color=YELLOW)

        score_board_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 410),
                                    text_input="Score Board", font=get_font(30), base_color=WHITE,
                                    hovering_color=YELLOW)

        exit_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 500),
                             text_input="Exit", font=get_font(30), base_color=WHITE, hovering_color=YELLOW)

        main_menu_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 230),
                                  text_input="Main Menu", font=get_font(30), base_color=WHITE, hovering_color=YELLOW)

        for button in [play_again_button, score_board_button, exit_button, main_menu_button]:
            button.change_color(game_over_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.check_input(game_over_mouse_pos):
                    playing()
                if score_board_button.check_input(game_over_mouse_pos):
                    score_board()
                if exit_button.check_input(game_over_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if main_menu_button.check_input(game_over_mouse_pos):
                    main_menu()

        pygame.display.update()


def countdown(t):
    while t:
        print(t)
        time.sleep(1)
        t -= 1
        t_text = get_font(50).render(f"{t}", True, BLUE)
        t_rect = t_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        SCREEN.fill(WHITE)
        SCREEN.blit(t_text, t_rect)
        pygame.display.update()


def pause():
    pausing = True

    while pausing:
        pygame.mouse.set_visible(True)
        pausing_mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(BLACK)
        button_load = pygame.image.load("Pictures/Button.png")

        pygame.display.set_caption("Snake Game 2.0 Pause Screen")

        pause_text = get_font(45).render("Pause", True, BLUE)
        pause_rect = pause_text.get_rect(center=(310, 100))
        SCREEN.blit(pause_text, pause_rect)

        pause_back = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 500),
                            text_input="BACK", font=get_font(30), base_color=WHITE, hovering_color=YELLOW)

        pause_back.change_color(pausing_mouse_pos)
        pause_back.update(SCREEN)

        play_again_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 320),
                                   text_input="Play Again", font=get_font(30),
                                   base_color=WHITE, hovering_color=YELLOW)

        exit_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 410),
                             text_input="Exit", font=get_font(30), base_color=WHITE, hovering_color=YELLOW)

        main_menu_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 230),
                                  text_input="Main Menu", font=get_font(30), base_color=WHITE, hovering_color=YELLOW)

        for button in [play_again_button, exit_button, main_menu_button]:
            button.change_color(pausing_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.check_input(pausing_mouse_pos):
                    playing()
                if exit_button.check_input(pausing_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if main_menu_button.check_input(pausing_mouse_pos):
                    main_menu()
                if pause_back.check_input(pausing_mouse_pos):
                    pausing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausing = False

        pygame.display.update()

    countdown(4)


def score_board():
    while True:
        pygame.mouse.set_visible(True)
        score_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill(BLACK)
        pygame.display.set_caption("Snake Game 2.0 Score Board")

        score_text = get_font(45).render("Score board", True, "white")
        score_rect = score_text.get_rect(center=(310, 50))
        SCREEN.blit(score_text, score_rect)

        score_back = Button(image=None, pos=(307, 550),
                            text_input="BACK", font=get_font(40), base_color=WHITE, hovering_color=YELLOW)

        score_back.change_color(score_mouse_pos)
        score_back.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if score_back.check_input(score_mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:

        pygame.display.set_caption("Snake Game 2.0 Main Menu")
        SCREEN.blit(BG, (0, 0))

        button_load = pygame.image.load("Pictures/Button.png")

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(35).render("Snake Game", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH / 2, 120))

        play_button = Button(image=pygame.transform.scale(button_load, (120, 55)), pos=(SCREEN_WIDTH / 2, 190),
                             text_input="Play", font=get_font(20), base_color=WHITE, hovering_color=YELLOW)

        score_board_button = Button(image=pygame.transform.scale(button_load, (280, 55)), pos=(SCREEN_WIDTH / 2, 250),
                                    text_input="Score Board", font=get_font(20), base_color=WHITE,
                                    hovering_color=YELLOW)

        exit_button = Button(image=pygame.transform.scale(button_load, (120, 55)), pos=(SCREEN_WIDTH / 2, 310),
                             text_input="Exit", font=get_font(20), base_color=WHITE, hovering_color=YELLOW)

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, score_board_button, exit_button]:
            button.change_color(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_input(menu_mouse_pos):
                    playing()
                if score_board_button.check_input(menu_mouse_pos):
                    score_board()
                if exit_button.check_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
