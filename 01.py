import pygame
import time

pygame.init()


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = 0
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 10
        self.pole = []
        self.person = [0, 10]
        self.first = True
        self.floor = True
        self.geld = 0
        self.level = 1
        self.kolvo_levels = 2
        for i in range(width):
            a = []
            for j in range(height):
                a.append(0)
            self.pole.append(a)

    def level_load(self, level_number):
        name = 'level_' + str(level_number) + '.txt'
        text_level = open(name, 'r')
        q = []
        s = 0
        for line in text_level:
            q.append(line)
            self.pole[s] = list(line)
            s += 1
        print(self.pole)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        x = self.left
        y = self.top

        for i in range(self.height):
            for j in range(self.width):
                # пустота
                if self.pole[i][j] == '-':
                    pygame.draw.rect(screen, (255, 255, 255), ((x, y), (self.cell_size, self.cell_size)), 0)
                # опора
                if self.pole[i][j] == 'x':
                    pygame.draw.rect(screen, (100, 100, 100), ((x, y), (self.cell_size, self.cell_size)), 0)
                    screen.blit(op_image, [x, y])
                # лестница
                elif self.pole[i][j] == 'i':
                    pygame.draw.rect(screen, (200, 150, 100), ((x, y), (self.cell_size, self.cell_size)), 0)
                    screen.blit(lest_image, [x, y])
                # предмет
                elif self.pole[i][j] == 'm':
                    pygame.draw.rect(screen, (50, 150, 100), ((x, y), (self.cell_size, self.cell_size)), 0)
                    screen.blit(geld_image, [x, y])
                # персонаж
                elif self.pole[i][j] == 'p':
                    if self.first:
                        self.person = [i, j]
                        self.first = False
                    screen.blit(pers_image, [x, y])
                    #pygame.draw.rect(screen, (255, 100, 100), ((x, y), (self.cell_size, self.cell_size)), 0)
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_cell(self, mouse_pos):
        # print(mouse_pos[0])
        if mouse_pos[0] <= self.left + self.cell_size * self.width \
                and mouse_pos[0] >= self.left and mouse_pos[1] <= self.top + self.cell_size * self.height \
                and mouse_pos[1] >= self.top:
            result = [(mouse_pos[0] - self.left) // self.cell_size * self.cell_size + self.left,
                      (mouse_pos[1] - self.top) // self.cell_size * self.cell_size + self.top]
            if self.pole[(mouse_pos[0] - self.left) // self.cell_size][(mouse_pos[1] - self.top)
                                                                       // self.cell_size] == 0:
                self.pole[(mouse_pos[0] - self.left) // self.cell_size][(mouse_pos[1] - self.top) // self.cell_size] = 1
            elif self.pole[(mouse_pos[0] - self.left) // self.cell_size][(mouse_pos[1] - self.top)
                                                                         // self.cell_size] == 1:
                self.pole[(mouse_pos[0] - self.left) // self.cell_size][(mouse_pos[1] - self.top) // self.cell_size] = 2
            else:
                self.pole[(mouse_pos[0] - self.left) // self.cell_size][(mouse_pos[1] - self.top) // self.cell_size] = 0
            print('(' + str((mouse_pos[0] - self.left) // self.cell_size) + ', ' + str((mouse_pos[1] - self.top)
                                                                                       // self.cell_size) + ')')
            return result
        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords is None:
            pass
        else:
            self.draw_rect(cell_coords, self.color)

    def draw_rect(self, cell_coords, color):
        if self.pole[(cell_coords[0] - self.left) // self.cell_size][(cell_coords[1] - self.top)
                                                                     // self.cell_size] == 1:
            if self.color == 0:
                pygame.draw.line(screen, (0, 0, 255), cell_coords,
                                 (cell_coords[0] + self.cell_size, cell_coords[1] + self.cell_size), 2)
                pygame.draw.line(screen, (0, 0, 255), (cell_coords[0], cell_coords[1] + self.cell_size),
                                 (cell_coords[0] + self.cell_size, cell_coords[1]), 2)
                self.color = 1
            elif self.color == 1:
                pygame.draw.circle(screen, (255, 0, 0), (cell_coords[0] + self.cell_size // 2,
                                                         cell_coords[1] + self.cell_size // 2),
                                   self.cell_size // 2, 2)
                self.color = 0

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def left_key(self):
        self.pole[self.person[0]][(self.person[1])] = '-'
        self.person[1] -= 1
        self.pole[self.person[0]][(self.person[1])] = 'p'

    def right_key(self):
        self.pole[self.person[0]][(self.person[1])] = '-'
        self.person[1] += 1
        self.pole[self.person[0]][(self.person[1])] = 'p'

    def down(self):
        self.pole[self.person[0]][(self.person[1])] = '-'
        self.person[0] += 1
        self.pole[self.person[0]][(self.person[1])] = 'p'

    def fall(self):
        self.down()
        if board.person[0] > 30 or board.pole[board.person[0] + 1][board.person[1]] == 'x':
            self.floor = True

    def jump(self):
        if self.pole[self.person[0] - 2][self.person[1]] == 'i':
            self.pole[self.person[0]][(self.person[1])] = '-'
            self.person[0] -= 3
            self.pole[self.person[0]][(self.person[1])] = 'p'

    def bottom(self):
        if self.pole[self.person[0] + 1][self.person[1]] == 'i':
            self.pole[self.person[0]][(self.person[1])] = '-'
            self.person[0] += 2
            self.pole[self.person[0]][(self.person[1])] = 'p'

    def geld_check(self):
        if self.pole[self.person[0]][self.person[1] + 1] == 'm'\
                or self.pole[self.person[0]][self.person[1] - 1] == 'm':
            self.geld += 1
            if self.pole[self.person[0]][self.person[1] + 1] == 'm':
                self.pole[self.person[0]][self.person[1] + 1] = '-'
            else:
                self.pole[self.person[0]][self.person[1] - 1] = '-'


game_name = 'имя игры'
pygame.display.set_caption(game_name)
win_weight = 1000
win_height = 600
font = pygame.font.Font(None, 80)
font_small = pygame.font.Font(None, 25)
text_color = (255, 255, 255)
screen = pygame.display.set_mode((win_weight, win_height))
intro = True
running = True
start_screen = True

# заставка
while intro:
    text = font.render("Заставка", True, text_color)
    screen.blit(text, [win_weight // 2, win_height // 2])
    text = font_small.render("Для продолжения нажмите любую клавишу или щёлкните мышью", True, text_color)
    screen.blit(text, [win_weight // 2 - 100, win_height // 2 + 100])
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            intro = False
        elif event.type == pygame.QUIT:
            intro = False
            running = False
            start_screen = False
screen.fill((20, 20, 20))
# загрузка картинок
back_image = pygame.image.load("background.jpg").convert()
op_image = pygame.image.load("1.png").convert()
lest_image = pygame.image.load("2.png").convert()
geld_image = pygame.image.load("3.png").convert()
pers_image = pygame.image.load("4.png").convert()
win_image = pygame.image.load("win.png").convert()




screen.blit(back_image, [0, 0])
pygame.display.flip()
# кнопка начать
while start_screen:
    text = font.render("Начать", True, text_color)
    screen.blit(text, [win_weight // 2, win_height // 2])
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] >= 500 and event.pos[0] <= 700 and event.pos[1] >= 300 and event.pos[1] <= 400:
                start_screen = False
    pygame.display.flip()
screen.blit(back_image, [0, 0])
board = Board(50, 30)
board.set_view(50, 30, 18)
board.level_load(1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            g = 0
            for elem in board.pole:
                for el in elem:
                    if el == 'm':
                        g += 1
            pygame.draw.rect(screen, (100, 100, 100), ((100, 0), (230, 20)), 0)
            text = font_small.render("Осталось собрать: {} монет".format(str(g)), True, text_color)
            screen.blit(text, [100, 0])
            pygame.draw.rect(screen, (100, 100, 100), ((500, 0), (230, 20)), 0)
            text = font_small.render("Уровень {}".format(str(board.level)), True, text_color)
            screen.blit(text, [500, 0])
            if g == 0:
                board.level += 1
                if board.level == board.kolvo_levels:
                    screen.blit(win_image, [400, 300])
                else:
                    board.level_load(board.level)
            if event.key == pygame.K_LEFT:
                board.left_key()
            elif event.key == pygame.K_RIGHT:
                board.right_key()
            elif event.key == pygame.K_UP:
                board.jump()
            elif event.key == pygame.K_DOWN:
                board.bottom()
            board.geld_check()
            if board.pole[board.person[0] + 1][board.person[1]] != 'x'\
                    and board.pole[board.person[0] + 1][board.person[1]] != 'i':
                board.floor = False
                while not board.floor:
                    board.fall()
                    pygame.display.flip()
    board.render()
    pygame.display.flip()
