import random
import sys
import time
import re
import pygame
from button import Button

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Snake Game 2.0")
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

user_name = ''
score_list = []
update = True

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

big_blue_potion = pygame.image.load("Pictures/blue_potion.png")
blue_potion = pygame.transform.scale(big_blue_potion, (GRID_BLOCK, GRID_BLOCK))

big_leaf = pygame.image.load("Pictures/leaf.png")
leaf = pygame.transform.scale(big_leaf, (GRID_BLOCK, GRID_BLOCK))

big_snail = pygame.image.load("Pictures/snail.png")
snail = pygame.transform.scale(big_snail, (GRID_BLOCK, GRID_BLOCK))

death_sound = pygame.mixer.Sound("SoundEffect/deathsound.ogg")
eat_sound = pygame.mixer.Sound("SoundEffect/eatingsound.ogg")
item_sound = pygame.mixer.Sound("SoundEffect/itemsound.wav")
life_sound = pygame.mixer.Sound("SoundEffect/lifesound.wav")
warp_sound = pygame.mixer.Sound("SoundEffect/warpsound.ogg")
pygame.mixer.music.load("SoundEffect/menumusic.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)


BLACK = (25, 25, 25)
WHITE = (220, 220, 220)
YELLOW = (227, 207, 87)
RED = (205, 51, 51)
VIOLET = (143, 0, 255)
BLUE = (93, 173, 226)
GREEN = (171, 235, 198)
PEACH = (253, 114, 114)
PINE_GLADE = (189, 197, 129)
GRAY = (202, 211, 200)

font_name = '8-BIT WONDER.TTF'
second_font_name = 'font.TTF'
score_font_style = pygame.font.Font(second_font_name, 50)
credit_font_style = pygame.font.Font(second_font_name, 70)

Menu_bg = pygame.image.load("Pictures/Menu-Background.jpg")
BG = pygame.transform.scale(Menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT + 75))


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


def save_score(name, score):
    if name != '' and update:
        scoreboard_file = open("Scoreboard.txt", "a+")
        scoreboard_file.write(f"{name}    -    {score}\n")
        scoreboard_file.close()


def sort_score():

    scoreboard_file = open("Scoreboard.txt", "r")
    readthefile = scoreboard_file.readlines()
    readthefile.sort(key=lambda s: int(re.search(r'\d+', s).group()), reverse=True)
    # debug
    print(readthefile)

    score_list.clear()
    for i in readthefile:
        score_list.append(i.strip())


def playing():

    game_over = False

    pygame.mixer.music.stop()
    pygame.mixer.music.load("SoundEffect/gamemusic.ogg")
    pygame.mixer.music.play(-1)

    SCREEN.fill(BLACK)
    draw_grid()

    score = 0
    life = 3
    snake_color = WHITE
    holding = 'nothing'
    fps = 15
    item = random.choice([star, blue_potion, leaf, snail])

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

    fruit_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
    fruit_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK

    heart_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
    heart_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK

    star_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
    star_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK

    blue_potion_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
    blue_potion_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK

    leaf_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
    leaf_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK

    snail_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
    snail_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK

    clock = pygame.time.Clock()

    while not game_over:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT and delta_x != GRID_BLOCK) or (
                        event.key == pygame.K_a and delta_x != GRID_BLOCK):
                    delta_x = -GRID_BLOCK
                    delta_y = 0
                if (event.key == pygame.K_RIGHT and delta_x != -GRID_BLOCK) or (
                        event.key == pygame.K_d and delta_x != -GRID_BLOCK):
                    delta_x = GRID_BLOCK
                    delta_y = 0
                if (event.key == pygame.K_UP and delta_y != GRID_BLOCK) or (
                        event.key == pygame.K_w and delta_y != GRID_BLOCK):
                    delta_x = 0
                    delta_y = -GRID_BLOCK
                if (event.key == pygame.K_DOWN and delta_y != -GRID_BLOCK) or (
                        event.key == pygame.K_s and delta_y != -GRID_BLOCK):
                    delta_x = 0
                    delta_y = GRID_BLOCK
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_o:
                    game_over = True

            if not holding == 'star_holding':
                if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
                    death_sound.play()
                    time.sleep(2)
                    snake_body = []
                    life -= 1
                    snake_color = WHITE
                    holding = 'nothing'
                    fps = 15
                    x = SCREEN_WIDTH / 2
                    y = SCREEN_HEIGHT / 2

            if life == 0:
                game_over = True

        score_display = score_font_style.render(f"Score : {score}", True, GREEN)
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
                death_sound.play()
                time.sleep(2)
                snake_body = []
                life -= 1
                snake_color = WHITE
                holding = 'nothing'
                fps = 15
                x = SCREEN_HEIGHT / 2
                y = SCREEN_WIDTH / 2

            if life == 0:
                game_over = True

        SCREEN.fill(BLACK)
        draw_grid()

        update_snake(GRID_BLOCK, snake_body, snake_color, snake_color)
        x += delta_x
        y += delta_y

        SCREEN.blit(fruit, (fruit_x, fruit_y))
        SCREEN.blit(score_display, score_rect)

        if score % 1000 == 0 and score != 0:
            if item == star:
                SCREEN.blit(star, (star_x, star_y))
                if x == star_x and y == star_y:
                    item = random.choice([star, blue_potion, leaf, snail])
                    score += 100
                    star_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                    star_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                    holding = 'star holding'
                    item_sound.play()
            elif item == blue_potion:
                SCREEN.blit(blue_potion, (blue_potion_x, blue_potion_y))
                if x == blue_potion_x and y == blue_potion_y:
                    item = random.choice([star, blue_potion, leaf, snail])
                    score += 200
                    blue_potion_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                    blue_potion_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                    holding = 'blue potion holding'
                    item_sound.play()
            elif item == leaf:
                SCREEN.blit(leaf, (leaf_x, leaf_y))
                if x == leaf_x and y == leaf_y:
                    item = random.choice([star, blue_potion, leaf, snail])
                    score += 100
                    leaf_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                    leaf_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                    holding = 'leaf holding'
                    item_sound.play()
            elif item == snail:
                SCREEN.blit(snail, (snail_x, snail_y))
                if x == snail_x and y == snail_y:
                    item = random.choice([star, blue_potion, leaf, snail])
                    score += 100
                    snail_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                    snail_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                    holding = 'snail holding'
                    item_sound.play()

        if holding == 'star holding':
            fps = 15
            snake_color = YELLOW
            if x >= SCREEN_WIDTH:
                warp_sound.play()
                x = 0
                y = y
            if x < 0:
                warp_sound.play()
                x = SCREEN_WIDTH
                y = y
            if y >= SCREEN_HEIGHT:
                warp_sound.play()
                x = x
                y = 0
            if y < 0:
                warp_sound.play()
                x = x
                y = SCREEN_HEIGHT
        if holding == 'blue potion holding':
            fps = 15
            snake_color = BLUE
            if x == fruit_x and y == fruit_y:
                fruit_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                fruit_y = round(random.randrange(60, SCREEN_HEIGHT - 60) / GRID_BLOCK) * GRID_BLOCK
                score += 200
                length_of_snake += 1
                eat_sound.play()
        if holding == 'leaf holding':
            snake_color = PINE_GLADE
            fps = 25
        if holding == 'snail holding':
            snake_color = PEACH
            fps = 10

        if score % 3000 == 0 and score != 0:
            SCREEN.blit(heart, (heart_x, heart_y))
            if x == heart_x and y == heart_y:
                life += 1
                score += 100
                holding = 'nothing'
                fps = 15
                snake_color = WHITE
                heart_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                heart_y = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
                life_sound.play()

        if life == 3:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 70, 10))
        elif life == 2:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 50, 10))
        elif life == 1:
            SCREEN.blit(display_life, (SCREEN_WIDTH - 30, 10))
        elif life == 0:
            SCREEN.blit(display_life, (SCREEN_WIDTH, SCREEN_HEIGHT))

        if x == fruit_x and y == fruit_y:
            fruit_x = round(random.randrange(60, SCREEN_WIDTH - 60) / GRID_BLOCK) * GRID_BLOCK
            fruit_y = round(random.randrange(60, SCREEN_HEIGHT - 60) / GRID_BLOCK) * GRID_BLOCK
            score += 100
            length_of_snake += 1
            eat_sound.play()
            item = random.choice([star, blue_potion, leaf])

        pygame.display.update()
        clock.tick(fps)

    global SCORE, update
    SCORE = score
    update = True
    save_score(user_name, SCORE)

    game_over_screen()


def game_over_screen():
    while True:
        pygame.mouse.set_visible(True)
        game_over_mouse_pos = pygame.mouse.get_pos()

        global SCORE
        SCREEN.fill(BLACK)
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
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("SoundEffect/menumusic.ogg")
                    pygame.mixer.music.play(-1)
                    scoreboard()
                if exit_button.check_input(game_over_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if main_menu_button.check_input(game_over_mouse_pos):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("SoundEffect/menumusic.ogg")
                    pygame.mixer.music.play(-1)
                    main_menu()

        pygame.display.update()


def countdown(t):
    while t:
        t -= 1
        t_text = get_font(120).render(f"{t + 1}", True, BLUE)
        t_rect = t_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        SCREEN.fill(BLACK)
        SCREEN.blit(t_text, t_rect)
        pygame.display.update()
        pygame.time.wait(1000)


def pause():
    pausing = True

    while pausing:
        pygame.mouse.set_visible(True)
        pausing_mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(BLACK)
        button_load = pygame.image.load("Pictures/Button.png")

        pause_text = get_font(45).render("Pause", True, BLUE)
        pause_rect = pause_text.get_rect(center=(310, 100))
        SCREEN.blit(pause_text, pause_rect)

        pause_back = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 230),
                            text_input="Resume", font=get_font(30), base_color=WHITE, hovering_color=YELLOW)

        pause_back.change_color(pausing_mouse_pos)
        pause_back.update(SCREEN)

        play_again_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 320),
                                   text_input="Play Again", font=get_font(30),
                                   base_color=WHITE, hovering_color=YELLOW)

        exit_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 500),
                             text_input="Exit", font=get_font(30), base_color=WHITE, hovering_color=YELLOW)

        main_menu_button = Button(image=pygame.transform.scale(button_load, (370, 70)), pos=(SCREEN_WIDTH / 2, 410),
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
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("SoundEffect/menumusic.ogg")
                    pygame.mixer.music.play(-1)
                    main_menu()
                if pause_back.check_input(pausing_mouse_pos):
                    pausing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausing = False

        pygame.display.update()

    countdown(3)


def scoreboard():
    display = True
    global score_list, update
    if update:
        sort_score()
        update = False
    while display:
        pygame.mouse.set_visible(True)
        score_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill(BLACK)
        pygame.draw.rect(SCREEN, GRAY, [50, 100, 500, 400], 0)
        pygame.draw.rect(SCREEN, VIOLET, [50, 100, 500, 400], 8)

        score_text = get_font(45).render("Scoreboard", True, YELLOW)
        score_rect = score_text.get_rect(center=(300, 50))
        SCREEN.blit(score_text, score_rect)

        if len(score_list) > 0:
            top1 = score_list[0]
            top_1 = score_font_style.render(f"1  :   {top1}", True, VIOLET)
            SCREEN.blit(top_1, (75, 120))
        else:
            top_1 = score_font_style.render("1  : ", True, VIOLET)
            SCREEN.blit(top_1, (75, 120))

        if len(score_list) > 1:
            top2 = score_list[1]
            top_2 = score_font_style.render(f"2 :   {top2}", True, VIOLET)
            SCREEN.blit(top_2, (75, 200))
        else:
            top_2 = score_font_style.render("2 : ", True, VIOLET)
            SCREEN.blit(top_2, (75, 200))

        if len(score_list) > 2:
            top3 = score_list[2]
            top_3 = score_font_style.render(f"3 :   {top3}", True, VIOLET)
            SCREEN.blit(top_3, (75, 280))
        else:
            top_3 = score_font_style.render("3 : ", True, VIOLET)
            SCREEN.blit(top_3, (75, 280))

        if len(score_list) > 3:
            top4 = score_list[3]
            top_4 = score_font_style.render(f"4 :   {top4}", True, VIOLET)
            SCREEN.blit(top_4, (75, 360))
        else:
            top_4 = score_font_style.render("4 : ", True, VIOLET)
            SCREEN.blit(top_4, (75, 360))

        if len(score_list) > 4:
            top5 = score_list[4]
            top_5 = score_font_style.render(f"5 :   {top5}", True, VIOLET)
            SCREEN.blit(top_5, (75, 440))
        else:
            top_5 = score_font_style.render("5 : ", True, VIOLET)
            SCREEN.blit(top_5, (75, 440))

        score_back = Button(image=None, pos=(300, 550),
                            text_input="BACK", font=get_font(40), base_color=WHITE, hovering_color=YELLOW)

        score_back.change_color(score_mouse_pos)
        score_back.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if score_back.check_input(score_mouse_pos):
                    display = False
                    main_menu()

        pygame.display.update()


def name_input():

    input_rect = pygame.Rect(50, 200, 500, 80)
    box_color_active = pygame.Color(WHITE)
    box_color_passive = pygame.Color((44, 58, 71))
    active = False
    finish = False
    snake_pic = pygame.image.load("Pictures/Pixel_snake.png")
    button_load = pygame.image.load("Pictures/Button.png")
    global user_name

    while not finish:
        pygame.mouse.set_visible(True)
        name_input_mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(BLACK)
        name_input_back = Button(image=pygame.transform.scale(button_load, (140, 60)), pos=(150, 450),
                                 text_input="BACK", font=get_font(25), base_color=GREEN, hovering_color=PINE_GLADE)
        name_input_next = Button(image=pygame.transform.scale(button_load, (140, 60)), pos=(150, 370),
                                 text_input="NEXT", font=get_font(25), base_color=GREEN, hovering_color=PINE_GLADE)

        for button in [name_input_back, name_input_next]:
            button.change_color(name_input_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if name_input_back.check_input(name_input_mouse_pos):
                        main_menu()
                    if name_input_next.check_input(name_input_mouse_pos):
                        finish = True
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_name = user_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        finish = True
                    elif len(user_name) < 8:
                        user_name += event.unicode
        if active:
            box_color = box_color_active
        else:
            box_color = box_color_passive

        pygame.draw.rect(SCREEN, box_color, input_rect, 5)

        name_text_style = pygame.font.Font(second_font_name, 80)
        name_text = name_text_style.render("enter your name", True, GREEN)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH / 2, 100))

        input_name_style = pygame.font.Font(second_font_name, 70)
        input_name = input_name_style.render(user_name, True, GREEN)

        SCREEN.blit(input_name, (input_rect.x + 10, input_rect.y + 7))
        SCREEN.blit(snake_pic, (SCREEN_WIDTH / 2 - 50, 300))
        SCREEN.blit(name_text, name_rect)

        pygame.display.update()

    if user_name == '':
        user_name = 'GUEST'

    print(user_name)
    playing()


def credit():
    snake_pic = pygame.image.load("Pictures/Snake-3.png")
    while True:
        pygame.mouse.set_visible(True)
        credit_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill(BLACK)

        credit_first_line_text = credit_font_style.render("Create by", True, PINE_GLADE)
        credit_first_line_rect = credit_first_line_text.get_rect(center=(310, 75))
        SCREEN.blit(credit_first_line_text, credit_first_line_rect)

        credit_second_line_text = credit_font_style.render("Vivat Techakosol", True, PINE_GLADE)
        credit_second_line_rect = credit_second_line_text.get_rect(center=(310, 175))
        SCREEN.blit(credit_second_line_text, credit_second_line_rect)

        credit_third_line_text = credit_font_style.render("ID 65011001", True, PINE_GLADE)
        credit_third_line_rect = credit_third_line_text.get_rect(center=(310, 275))
        SCREEN.blit(credit_third_line_text, credit_third_line_rect)

        SCREEN.blit(snake_pic, (SCREEN_WIDTH / 2 - 50, 350))

        credit_back = Button(image=None, pos=(307, 550),
                             text_input="BACK", font=get_font(40), base_color=PINE_GLADE, hovering_color=YELLOW)

        credit_back.change_color(credit_mouse_pos)
        credit_back.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if credit_back.check_input(credit_mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():
    running = True
    while running:

        SCREEN.blit(BG, (0, 0))

        button_load = pygame.image.load("Pictures/Button.png")

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(35).render("Snake Game", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH / 2, 120))

        play_button = Button(image=pygame.transform.scale(button_load, (120, 55)), pos=(SCREEN_WIDTH / 2, 185),
                             text_input="Play", font=get_font(20), base_color=WHITE, hovering_color=YELLOW)

        score_board_button = Button(image=pygame.transform.scale(button_load, (240, 55)), pos=(SCREEN_WIDTH / 2, 245),
                                    text_input="ScoreBoard", font=get_font(20), base_color=WHITE,
                                    hovering_color=YELLOW)

        exit_button = Button(image=pygame.transform.scale(button_load, (120, 55)), pos=(SCREEN_WIDTH / 2, 365),
                             text_input="Exit", font=get_font(20), base_color=WHITE, hovering_color=YELLOW)

        credit_button = Button(image=pygame.transform.scale(button_load, (150, 55)), pos=(SCREEN_WIDTH / 2, 305),
                               text_input="Credit", font=get_font(20), base_color=WHITE, hovering_color=YELLOW)

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, score_board_button, exit_button, credit_button]:
            button.change_color(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_input(menu_mouse_pos):
                    name_input()
                if score_board_button.check_input(menu_mouse_pos):
                    scoreboard()
                if exit_button.check_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if credit_button.check_input(menu_mouse_pos):
                    credit()

        pygame.display.update()


main_menu()
