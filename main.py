import arcade
import math

# Размеры экрана
# Создаем базовую текстуру 1x1 пиксель для сплошной заливки
# Делаем текстуру не 1х1, а 30х30 пикселей (или CHARACTER_SIZE)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Путешествие по карте"

# Константы движения
MOVEMENT_SPEED = 100  # пикселей в секунду
CHARACTER_SIZE = 30
OFFSET = 35  # Расстояние между человечками (чтобы шли рядом)

BLANK_TEXTURE = arcade.make_soft_square_texture(CHARACTER_SIZE, arcade.color.WHITE, 255, 255)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_GREEN)

        # --- СПИСОК ПУТЕВЫХ ТОЧЕК (Траектория) ---
        # Координаты подобраны примерно под вашу картинку.
        # Начало сверху, идут по кругу, заканчивают у дерева слева.
        self.path_points = [
            (400, 550),  # 0. Старт (верх)
            (300, 500),  # 1. У пещеры
            (350, 400),  # 2. КОНТРОЛЬНАЯ ТОЧКА 1 (Черный квадрат)
            (400, 350),  # 3. У озера
            (600, 400),  # 4. Поворот направо
            (650, 300),  # 5. КОНТРОЛЬНАЯ ТОЧКА 2
            (600, 200),  # 6. У пенька
            (400, 150),  # 7. У медведя
            (200, 200),  # 8. У дерева внизу
            (200, 400),  # 9. ФИНИШ (Дерево сверху слева)
        ]

        # Индексы точек, которые являются контрольными (где нужно остановиться)
        self.checkpoint_indices = [1, 2, 4, 5, 7, 8]

        # Индексы точек, которые нужно отрисовать как черные квадраты
        self.checkpoint_sprites = arcade.SpriteList()

        # Спрайты человечков
        self.player1 = None
        self.player2 = None

        # ... (ваш код создания player1 и player2) ...

        # Логика движения
        self.current_target_index = 1  # Индекс точки, к которой идем
        self.is_moving = False

        self.setup()

    def setup(self):
        # --- НАСТРОЙКА ЧЕЛОВЕЧКОВ ---
        # Создаем обычные спрайты (текстура у них уже 30х30)
        self.player1 = arcade.Sprite(BLANK_TEXTURE)
        self.player1.color = arcade.color.RED

        self.player2 = arcade.Sprite(BLANK_TEXTURE)
        self.player2.color = arcade.color.BLUE

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player1)
        self.player_list.append(self.player2)

        # Ставим их на стартовую точку
        start_x, start_y = self.path_points[0]
        self.player1.center_x = start_x + OFFSET / 2
        self.player1.center_y = start_y
        self.player2.center_x = start_x - OFFSET / 2
        self.player2.center_y = start_y

        # --- НАСТРОЙКА КОНТРОЛЬНЫХ ТОЧЕК (Черные квадраты) ---
        # Для контрольных точек создадим отдельную маленькую текстуру
        cp_texture = arcade.make_soft_square_texture(20, arcade.color.WHITE, 255, 255)

        for index in self.checkpoint_indices:
            x, y = self.path_points[index]

            cp_sprite = arcade.Sprite(cp_texture)
            cp_sprite.color = arcade.color.BLACK

            cp_sprite.center_x = x
            cp_sprite.center_y = y
            self.checkpoint_sprites.append(cp_sprite)

    def on_draw(self):
        self.clear()

        # 1. Рисуем фон (позже сюда можно загрузить вашу картинку)
        # arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, texture)

        # 2. Рисуем линии пути (чтобы видеть траекторию)
        for i in range(len(self.path_points) - 1):
            start = self.path_points[i]
            end = self.path_points[i + 1]
            arcade.draw_line(start[0], start[1], end[0], end[1], arcade.color.BROWN, 5)

        # 3. Рисуем контрольные точки
        self.checkpoint_sprites.draw()

        # 4. Рисуем человечков
        self.player_list.draw()

        # 5. Инструкция на экране
        if not self.is_moving:
            arcade.draw_text("Нажмите ПРОБЕЛ, чтобы начать/продолжить движение",
                             SCREEN_WIDTH // 2, 30, arcade.color.BLACK, 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        # По нажатию пробела запускаем или останавливаем движение
        if key == arcade.key.SPACE:
            self.is_moving = True

    def on_update(self, delta_time):
        # Если игра на паузе (стоят на контрольной точке) - ничего не делаем
        if not self.is_moving:
            return

        # Если дошли до конца пути - останавливаемся навсегда
        if self.current_target_index >= len(self.path_points):
            self.is_moving = False
            return

        # Получаем текущую цель
        target_x, target_y = self.path_points[self.current_target_index]

        # Вектор от человечка 1 до цели
        dx = target_x - self.player1.center_x
        dy = target_y - self.player1.center_y

        # Расстояние до цели
        distance = math.hypot(dx, dy)

        # Если расстояние меньше шага за этот кадр - телепортируем в цель
        if distance < MOVEMENT_SPEED * delta_time:
            self.player1.center_x = target_x
            self.player1.center_y = target_y

            # Проверяем, является ли эта точка контрольной
            if self.current_target_index in self.checkpoint_indices:
                self.is_moving = False  # Останавливаемся, ждем пробел

            self.current_target_index += 1  # Переключаемся на следующую точку

        else:
            # Двигаемся к цели
            angle = math.atan2(dy, dx)

            # Двигаем первого человечка
            self.player1.center_x += math.cos(angle) * MOVEMENT_SPEED * delta_time
            self.player1.center_y += math.sin(angle) * MOVEMENT_SPEED * delta_time

        # --- ЛОГИКА ДЛЯ ВТОРОГО ЧЕЛОВЕЧКА (Идут рядом) ---
        # Вычисляем перпендикулярный угол, чтобы второй шел сбоку
        if self.current_target_index < len(self.path_points):
            target_x, target_y = self.path_points[self.current_target_index]
            dx = target_x - self.player1.center_x
            dy = target_y - self.player1.center_y
            angle = math.atan2(dy, dx)

            # Смещение вбок (перпендикулярно движению)
            perp_angle = angle + math.pi / 2
            self.player2.center_x = self.player1.center_x + math.cos(perp_angle) * OFFSET
            self.player2.center_y = self.player1.center_y + math.sin(perp_angle) * OFFSET


def main():
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()
