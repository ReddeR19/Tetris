import pygame
import random
import sys

pygame.init()
pygame.font.init()

# GLOBALS VARS/ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# MUSIC/МУЗЫКА
pygame.mixer.music.load('sounds/red.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# IMAGES/ИЗОБРАЖЕНИЯ
img = pygame.image.load('images/8bit.png')

# COLOR BUTTON/ЦВЕТ КНОПКИ
color_rect = (255, 0, 0)

# TEXT/ТЕКСТ
font = pygame.font.SysFont("miratrix", 40, bold=True)

# SHAPE FORMATS/ФИГУРЫ
S_s = [['.....',
        '.....',
        '..00.',
        '.00..',
        '.....'],
       ['.....',
        '..0..',
        '..00.',
        '...0.',
        '.....']]

Z_s = [['.....',
        '.....',
        '.00..',
        '..00.',
        '.....'],
       ['.....',
        '..0..',
        '.00..',
        '.0...',
        '.....']]

I_s = [['..0..',
        '..0..',
        '..0..',
        '..0..',
        '.....'],
       ['.....',
        '0000.',
        '.....',
        '.....',
        '.....']]

O_s = [['.....',
        '.....',
        '.00..',
        '.00..',
        '.....']]

J_s = [['.....',
        '.0...',
        '.000.',
        '.....',
        '.....'],
       ['.....',
        '..00.',
        '..0..',
        '..0..',
        '.....'],
       ['.....',
        '.....',
        '.000.',
        '...0.',
        '.....'],
       ['.....',
        '..0..',
        '..0..',
        '.00..',
        '.....']]

L_s = [['.....',
        '...0.',
        '.000.',
        '.....',
        '.....'],
       ['.....',
        '..0..',
        '..0..',
        '..00.',
        '.....'],
       ['.....',
        '.....',
        '.000.',
        '.0...',
        '.....'],
       ['.....',
        '.00..',
        '..0..',
        '..0..',
        '.....']]

T_s = [['.....',
        '..0..',
        '.000.',
        '.....',
        '.....'],
       ['.....',
        '..0..',
        '..00.',
        '..0..',
        '.....'],
       ['.....',
        '.....',
        '.000.',
        '..0..',
        '.....'],
       ['.....',
        '..0..',
        '.00..',
        '..0..',
        '.....']]

shapes = [S_s, Z_s, I_s, O_s, J_s, L_s, T_s]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):  # осн класс
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def pause():  # пауза

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        win.fill((0, 0, 0))
        win.blit(img, (-200, -245))
        draw_text(win, 'Paused', 80, (255, 255, 255))
        pygame.display.update()


def create_grid(locked_pos={}):  # игр сетка
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):  # конвертация фируг
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):  # игр пространство
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):  # проверка на проигрышь
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():  # выбор фигуры
    return Piece(5, 0, random.choice(shapes))


def draw_text(surface, text, size, color):  # текст
    font = pygame.font.SysFont("miratrix", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2),
                         top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, grid):  # рисовка сетки
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):  # очистка

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except Exception:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):  # след фигура
    font = pygame.font.SysFont('miratrix', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):  # обнов рекорда
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():  # макс рекорд
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score=0):  # окно
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('miratrix', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # нынишний рекорд
    font = pygame.font.SysFont('miratrix', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    # последний рекорд
    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))

    sx = top_left_x - 250
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 255, 255), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)


def main(win):  # игр цикл
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0

    while run:

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.10:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_p:
                    pause()

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 100

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text(win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def win_menu():  # окно меню
    pygame.draw.rect(win, color_rect,
                     (312, 270, 200, 75), 8)
    pygame.draw.rect(win, color_rect,
                     (312, 400, 200, 75), 8)
    mesg = font.render("Новая игра", True, (255, 255, 255))
    win.blit(mesg, [s_width / 2 - 75,
                    s_height / 2 - 55])
    mesg = font.render("Выйти", True, (255, 255, 255))
    win.blit(mesg, [s_width / 2 - 35,
                    s_height / 2 + 75])


def main_menu(win):  # меню
    run = True
    while run:
        win.fill((0, 0, 0))
        win.blit(img, (-200, -245))
        win_menu()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if (x > 250 and x < 600 and y > 120 and y < 320):
                        main(win)
                    elif (x > 250 and x < 600 and y > 350 and y < 550):
                        pygame.quit()
                        sys.exit()

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)
