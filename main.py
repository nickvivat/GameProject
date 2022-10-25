import random
import time
import pygame
from button import Button
import sys

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

icon = pygame.image.load("Pictures/Snake-3.png")
pygame.display.set_icon(icon)

big_fruit = pygame.image.load("Pictures/Fruit-RemovedBackground.jpg")
fruit = pygame.transform.scale(big_fruit, (20, 20))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 155, 255)
CYAN = (127, 255, 212)
YELLOW = (227, 207, 87)
GREEN = (150, 255, 150)

font_name = '8-BIT WONDER.TTF'
score_font_name = 'font.TTF'
score_font_style = pygame.font.Font(score_font_name, 30)

Menu_bg = pygame.image.load("Pictures/Menu-Background.jpg")
BG = pygame.transform.scale(Menu_bg, (600, 600))


def message(msg, color):
    mes = get_font(50).render(msg, True, color)
    SCREEN.blit(mes, [SCREEN_WIDTH / 2 - 220, SCREEN_HEIGHT / 2 - 40])


def get_font(size):
    return pygame.font.Font(font_name, size)


def playing():
    pygame.display.set_caption("Snake Game 2.0")

    game_over = False

    bg = pygame.image.load("Pictures/background.jpg")
    background = pygame.transform.scale(bg, (600, 600))

    score = 0
    life = 3

    start_life = pygame.image.load("Pictures/Three_heart.jpg")
    two_heart = pygame.image.load("Pictures/Two_heart.jpg")
    one_heart = pygame.image.load("Pictures/One_heart.jpg")

    display_life = pygame.transform.scale(start_life, (60, 20))

    x = SCREEN_HEIGHT / 2
    y = SCREEN_WIDTH / 2

    delta_x = 0
    delta_y = 0

    fruit_x = round(random.randrange(20, SCREEN_WIDTH - 20) / 10.0) * 10
    fruit_y = round(random.randrange(20, SCREEN_HEIGHT - 20) / 10.0) * 10

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    delta_x = -10
                    delta_y = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    delta_x = 10
                    delta_y = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    delta_x = 0
                    delta_y = -10
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    delta_x = 0
                    delta_y = 10
                elif event.key == pygame.K_o:
                    game_over = True

            if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
                life -= 1
                x = SCREEN_HEIGHT / 2
                y = SCREEN_WIDTH / 2

            if life == 0:
                game_over = True

        x += delta_x
        y += delta_y

        score_display = score_font_style.render(f"Score : {score}", True, WHITE)
        score_rect = score_display.get_rect(center=(SCREEN_WIDTH / 2 + 10, 15))

        if life >= 3:
            life = 3
            display_life = pygame.transform.scale(start_life, (60, 20))
        elif life == 2:
            display_life = pygame.transform.scale(two_heart, (40, 20))
        elif life == 1:
            display_life = pygame.transform.scale(one_heart, (20, 20))

        SCREEN.blit(background, (0, 0))
        pygame.draw.rect(SCREEN, WHITE, [x, y, 10, 10])
        SCREEN.blit(fruit, (fruit_x, fruit_y))
        SCREEN.blit(score_display, score_rect)

        if life == 3:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 70, 10))
        elif life == 2:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 50, 10))
        elif life == 1:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 30, 10))
        elif life == 0:
            SCREEN.blit(display_life, (SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.update()

        if x == fruit_x and y == fruit_y or x + 10 == fruit_x + 20 and y + 10 == fruit_y + 20:
            fruit_x = round(random.randrange(20, SCREEN_WIDTH - 20) / 10.0) * 10.0
            fruit_y = round(random.randrange(40, SCREEN_HEIGHT - 20) / 10.0) * 10.0
            score += 100

        pygame.display.update()
        clock.tick(30)
    SCREEN.fill(BLACK)
    message("Game Over", YELLOW)
    pygame.display.update()
    time.sleep(2)


def score_board():
    while True:
        score_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("black")

        score_text = get_font(45).render("Score board", True, "white")
        score_rect = score_text.get_rect(center=(310, 50))
        SCREEN.blit(score_text, score_rect)

        score_back = Button(image=None, pos=(307, 550),
                            text_input="BACK", font=get_font(40), base_color="white", hovering_color=YELLOW)

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

        pygame.display.set_caption("Snake Game 2.0 Menu")
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

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, score_board_button]:
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

        pygame.display.update()


main_menu()
