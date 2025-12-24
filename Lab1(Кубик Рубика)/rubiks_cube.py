import pygame
import numpy as np
import random
import math
from OpenGL.GL import *
from OpenGL.GLU import *


class RubiksCube:
    def __init__(self):
        # Инициализация Pygame и OpenGL
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Кубик Рубика 3D")

        # Настройка OpenGL
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width / self.height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

        # Цвета граней
        self.colors = {
            'F': (1, 0, 0),  # Красный - Front
            'B': (1, 0.5, 0),  # Оранжевый - Back
            'U': (1, 1, 1),  # Белый - Up
            'D': (1, 1, 0),  # Желтый - Down
            'L': (0, 0, 1),  # Синий - Left
            'R': (0, 1, 0)  # Зеленый - Right
        }

        # Инициализация кубика
        self.reset_cube()

        # Углы вращения камеры
        self.rotation_x = 0
        self.rotation_y = 0

        # Анимация поворота
        self.animating = False
        self.animation_angle = 0
        self.target_angle = 0
        self.rotation_face = None
        self.rotation_layer = None
        self.rotation_direction = 1

    def reset_cube(self):
        self.cube = np.empty((3, 3, 3), dtype=object)

        # Заполняем кубик цветами в собранном состоянии
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if x == 0:
                        self.cube[x, y, z] = 'L'
                    elif x == 2:
                        self.cube[x, y, z] = 'R'
                    elif y == 0:
                        self.cube[x, y, z] = 'D'
                    elif y == 2:
                        self.cube[x, y, z] = 'U'
                    elif z == 0:
                        self.cube[x, y, z] = 'B'
                    elif z == 2:
                        self.cube[x, y, z] = 'F'
                    else:
                        self.cube[x, y, z] = None  # Внутренние кубики не видны

    def scramble(self):
        moves = ['F', 'B', 'U', 'D', 'L', 'R', 'F\'', 'B\'', 'U\'', 'D\'', 'L\'', 'R\'']
        for _ in range(20):  # 20 случайных ходов
            move = random.choice(moves)
            if "'" in move:
                self.rotate_face(move[0], -1)
            else:
                self.rotate_face(move, 1)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = f.read().strip().split('\n')
                for i, line in enumerate(data):
                    colors = line.split()
                    for j, color in enumerate(colors):
                        x, y, z = self.index_to_3d(i * 9 + j)
                        if color in self.colors:
                            self.cube[x, y, z] = color
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                for i in range(27):
                    x, y, z = self.index_to_3d(i)
                    color = self.cube[x, y, z] if self.cube[x, y, z] else 'X'
                    f.write(color + ' ')
                    if (i + 1) % 9 == 0:
                        f.write('\n')
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def index_to_3d(self, index):
        x = index % 3
        y = (index // 3) % 3
        z = index // 9
        return x, y, z

    def rotate_face(self, face, direction=1):
        if self.animating:
            print(f"Поворот {face} пропущен - идет анимация")
            return

        print(f"Начинаем поворот {face}, направление: {direction}")
        self.animating = True
        self.animation_angle = 0
        self.target_angle = 90 * direction
        self.rotation_face = face
        self.rotation_direction = direction

        # Определяем слой для поворота
        if face == 'F':
            self.rotation_layer = 2
        elif face == 'B':
            self.rotation_layer = 0
        elif face == 'U':
            self.rotation_layer = 2
        elif face == 'D':
            self.rotation_layer = 0
        elif face == 'L':
            self.rotation_layer = 0
        elif face == 'R':
            self.rotation_layer = 2

    def apply_rotation(self):
        face = self.rotation_face
        direction = self.rotation_direction

        # Создаем временную копию
        temp_cube = self.cube.copy()

        if face == 'F':  # Front face (z=2)
            for i in range(3):
                for j in range(3):
                    if direction == 1:  # По часовой
                        temp_cube[i, j, 2] = self.cube[2 - j, i, 2]
                    else:  # Против часовой
                        temp_cube[i, j, 2] = self.cube[j, 2 - i, 2]

        elif face == 'B':  # Back face (z=0)
            for i in range(3):
                for j in range(3):
                    if direction == 1:  # По часовой
                        temp_cube[i, j, 0] = self.cube[2 - j, i, 0]
                    else:  # Против часовой
                        temp_cube[i, j, 0] = self.cube[j, 2 - i, 0]

        elif face == 'U':  # Up face (y=2)
            for i in range(3):
                for j in range(3):
                    if direction == 1:  # По часовой
                        temp_cube[i, 2, j] = self.cube[2 - j, 2, i]
                    else:  # Против часовой
                        temp_cube[i, 2, j] = self.cube[j, 2, 2 - i]

        elif face == 'D':  # Down face (y=0)
            for i in range(3):
                for j in range(3):
                    if direction == 1:  # По часовой
                        temp_cube[i, 0, j] = self.cube[2 - j, 0, i]
                    else:  # Против часовой
                        temp_cube[i, 0, j] = self.cube[j, 0, 2 - i]

        elif face == 'L':  # Left face (x=0)
            for i in range(3):
                for j in range(3):
                    if direction == 1:  # По часовой
                        temp_cube[0, i, j] = self.cube[0, 2 - j, i]
                    else:  # Против часовой
                        temp_cube[0, i, j] = self.cube[0, j, 2 - i]

        elif face == 'R':  # Right face (x=2)
            for i in range(3):
                for j in range(3):
                    if direction == 1:  # По часовой
                        temp_cube[2, i, j] = self.cube[2, 2 - j, i]
                    else:  # Против часовой
                        temp_cube[2, i, j] = self.cube[2, j, 2 - i]

        self.cube = temp_cube
        self.animating = False

    def is_solved(self):
        # Проверяем каждую грань
        for face in ['F', 'B', 'U', 'D', 'L', 'R']:
            if face == 'F':
                check = self.cube[:, :, 2]
            elif face == 'B':
                check = self.cube[:, :, 0]
            elif face == 'U':
                check = self.cube[:, 2, :]
            elif face == 'D':
                check = self.cube[:, 0, :]
            elif face == 'L':
                check = self.cube[0, :, :]
            elif face == 'R':
                check = self.cube[2, :, :]

            # Все элементы грани должны быть одного цвета
            unique_colors = np.unique(check[check != None])
            if len(unique_colors) != 1:
                return False
        return True

    def draw_cube(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Позиция камеры
        glTranslatef(0, 0, -8)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # Рисуем кубики
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if self.cube[x, y, z] is not None:
                        self.draw_mini_cube(x - 1, y - 1, z - 1, self.cube[x, y, z])

        pygame.display.flip()

    def draw_mini_cube(self, x, y, z, color_char):
        color = self.colors[color_char]
        size = 0.5

        vertices = [
            [x - size, y - size, z - size], [x + size, y - size, z - size],
            [x + size, y + size, z - size], [x - size, y + size, z - size],
            [x - size, y - size, z + size], [x + size, y - size, z + size],
            [x + size, y + size, z + size], [x - size, y + size, z + size]
        ]

        faces = [
            [0, 1, 2, 3],  # задняя
            [4, 5, 6, 7],  # передняя
            [0, 1, 5, 4],  # нижняя
            [2, 3, 7, 6],  # верхняя
            [0, 3, 7, 4],  # левая
            [1, 2, 6, 5]  # правая
        ]

        glBegin(GL_QUADS)
        for face in faces:
            glColor3f(*color)
            for vertex in face:
                glVertex3f(*vertices[vertex])
        glEnd()

        # Черные линии между кубиками
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        for edge in [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
                     (0, 4), (1, 5), (2, 6), (3, 7)]:
            for vertex in edge:
                glVertex3f(*vertices[vertex])
        glEnd()

    def handle_events(self):
        try:
            events = pygame.event.get()
            if not events:
                return True
                
            for event in events:
                if event.type == pygame.QUIT:
                    return False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    
                    # Проверяем модификаторы для различения команд и поворотов
                    mods = pygame.key.get_mods()
                    shift_pressed = bool(mods & pygame.KMOD_SHIFT)
                    print(f"Нажата клавиша: {event.key}, Shift: {shift_pressed}, Анимируется: {self.animating}")
                    
                    # Команды управления (без Shift)
                    if not shift_pressed:
                        if event.key == pygame.K_r:
                            print("Сброс кубика")
                            self.reset_cube()
                        elif event.key == pygame.K_s:
                            print("Перемешивание")
                            self.scramble()
                        elif event.key == pygame.K_l:
                            print("Загрузка файла")
                            self.load_from_file("cube_state.txt")
                        elif event.key == pygame.K_p:
                            print("Сохранение файла")
                            self.save_to_file("cube_state.txt")
                        # Повороты по часовой (без Shift)
                        elif event.key == pygame.K_f:
                            print("Поворот F")
                            self.rotate_face('F', 1)
                        elif event.key == pygame.K_b:
                            print("Поворот B")
                            self.rotate_face('B', 1)
                        elif event.key == pygame.K_u:
                            print("Поворот U")
                            self.rotate_face('U', 1)
                        elif event.key == pygame.K_d:
                            print("Поворот D")
                            self.rotate_face('D', 1)
                        elif event.key == pygame.K_q:  # Используем Q для L
                            print("Поворот L")
                            self.rotate_face('L', 1)
                        elif event.key == pygame.K_e:  # Используем E для R
                            print("Поворот R")
                            self.rotate_face('R', 1)
                    
                    # Повороты против часовой (с Shift)
                    elif shift_pressed:
                        if event.key == pygame.K_f:
                            print("Поворот F'")
                            self.rotate_face('F', -1)
                        elif event.key == pygame.K_b:
                            print("Поворот B'")
                            self.rotate_face('B', -1)
                        elif event.key == pygame.K_u:
                            print("Поворот U'")
                            self.rotate_face('U', -1)
                        elif event.key == pygame.K_d:
                            print("Поворот D'")
                            self.rotate_face('D', -1)
                        elif event.key == pygame.K_q:  # Shift+Q для L'
                            print("Поворот L'")
                            self.rotate_face('L', -1)
                        elif event.key == pygame.K_e:  # Shift+E для R'
                            print("Поворот R'")
                            self.rotate_face('R', -1)

                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        rel_x, rel_y = event.rel
                        self.rotation_y += rel_x * 0.5
                        self.rotation_x += rel_y * 0.5
        except Exception as e:
            print(f"Ошибка обработки событий: {e}")
            import traceback
            traceback.print_exc()
            return True  # Продолжаем работу даже при ошибке

        return True

    def update_animation(self):
        if self.animating:
            self.animation_angle += 5 * self.rotation_direction
            if abs(self.animation_angle) >= abs(self.target_angle):
                print(f"Завершаем анимацию поворота {self.rotation_face}")
                self.apply_rotation()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        print("Управление:")
        print("F, B, U, D, Q (L), E (R) - поворот граней по часовой")
        print("Shift+F, Shift+B, Shift+U, Shift+D, Shift+Q, Shift+E - поворот против часовой")
        print("R - сброс, S - перемешать, L - загрузить, P - сохранить")
        print("ESC - выход")
        print("ЛКМ + движение - вращение камеры")

        while running:
            try:
                running = self.handle_events()
                self.update_animation()
                self.draw_cube()

                if self.is_solved():
                    print("Кубик собран!")

                clock.tick(60)
            except Exception as e:
                print(f"Ошибка в основном цикле: {e}")
                import traceback
                traceback.print_exc()
                break

        pygame.quit()
