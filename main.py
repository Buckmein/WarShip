import random

battlefield = [[]]
enemy_battlefield = [[]]
ships = []
e_ships = []


def new_game():
    """
    Функция начала новой игры 
    """
    clear_field()
    show_field()
    enemy_ships()
    ship_input()
    game()


def ship_input():
    """
    Ввод кораблей игрока
    :return:
    """
    global ships
    ships.clear()
    ostatok = [4, 2, 1]
    ship_type = ''  # Тип корабля
    cords0 = []  # Координаты начала
    cords1 = []  # Координаты конца
    for si in range(7):
        type_check = True
        cords_check = True
        while type_check:
            print(
                f'У вас осталось: {ostatok[2]} Трехмачтовых (3), {ostatok[1]} Двумачтовых (2) и {ostatok[0]} '
                f'Одномачтовых кораблей (1)')
            print("Введите тип корабля который хотите разместить")
            ship_type = input()
            if ship_type in ('1', '2', '3') and ostatok[int(ship_type) - 1] != 0:
                type_check = False
            else:
                print("!!!Нет такого типа кораблей!!!")
        while cords_check:
            if ship_type == "1":
                print("Введите координаты через пробел")
                ship_cords = input()
                cords0 = list(map(int, ship_cords.split()))
                cords1 = cords0
            else:
                print("Введите координаты начала через пробел")
                ship_cords = input()
                try:
                    cords0 = list(map(int, ship_cords.split()))
                except ValueError:
                    print("!!!Неверный формат ввода!!!")
                    continue
                print("Введите координаты конца через пробел")
                ship_cords = input()
                try:
                    cords1 = list(map(int, ship_cords.split()))
                except ValueError:
                    print("!!!Неверный формат ввода!!!")
                    continue
                if ((int(abs(cords0[0] - cords1[0])) != int(ship_type) - 1)
                    and (int((abs(cords0[1] - cords1[1])) != int(ship_type) - 1))) \
                        or (cords1[0] not in range(1, 7)) or (cords1[1] not in range(1, 7)) \
                        or (cords0[0] not in range(1, 7)) or (cords0[1] not in range(1, 7)) \
                        or all([cords0[0] - cords1[0] != 0, cords0[1] - cords1[1] != 0]):
                    print("!!!Неверно указаны координаты!!!")
                    continue
            if len(ships) == 0:
                cords_check = False
            for j in range(len(ships)):
                if cords0 in ships[j].get_space or cords1 in ships[j].get_space \
                        or cords0 in ships[j].get_parts or cords1 in ships[j].get_parts:
                    show_field(ships)
                    print("!!!корабль не вмещается, попробуйте другое место!!!")
                else:
                    cords_check = False

        ships.append(Ship(ship_type, *cords0, *cords1))
        ostatok[int(ship_type) - 1] -= 1
        show_field(ships)


def enemy_ships():
    """
    Создание кораблей оппонента
    :return:
    """
    global e_ships
    e_ships.clear()
    moved = False
    tries = 0
    x0 = random.randint(1, 6)
    if x0 > 4:
        x1 = x0 - 2
        moved = True
    elif x0 < 3:
        x1 = x0 + 2
        moved = True
    else:
        x1 = x0
        moved = False
    y0 = random.randint(1, 6)
    if y0 >= 3 and not moved:
        y1 = y0 - 2
    elif not moved:
        y1 = y0 + 2
    else:
        y1 = y0
    e_ships.append(Ship(3, int(x0), int(y0), int(x1), int(y1)))
    for si in range(2):
        space_check = True
        while space_check:
            space_check1 = False
            tries += 1
            if tries > 999:
                enemy_ships()
                return None
            x0 = random.randint(1, 6)
            y0 = random.randint(1, 6)
            if x0 > 3:
                x1 = x0 - 1
                moved = True
            elif x0 < 2:
                x1 = x0 + 1
                moved = True
            else:
                x1 = x0
                moved = False
            if y0 > 4 and not moved:
                y1 = y0 - 1
            elif not moved and y0 < 3:
                y1 = y0 + 1
            else:
                y1 = y0
            for j in range(len(e_ships)):
                if ([x0, y0] not in e_ships[j].get_parts) and ([x0, y0] not in e_ships[j].get_space) \
                        and ([x1, y1] not in e_ships[j].get_parts) and ([x1, y1] not in e_ships[j].get_space):
                    space_check = False
                else:
                    space_check1 = True
            space_check = space_check1 or space_check
        e_ships.append(Ship(2, int(x0), int(y0), int(x1), int(y1)))
    for si in range(4):
        space_check = True
        while space_check:
            tries += 1
            space_check1 = False
            if tries > 999:
                enemy_ships()
                return None
            x0 = random.randint(1, 6)
            x1 = x0
            y0 = random.randint(1, 6)
            y1 = y0
            for j in range(len(e_ships)):
                if ([x0, y0] not in e_ships[j].get_parts) and ([x0, y0] not in e_ships[j].get_space):
                    space_check = False
                else:
                    space_check1 = True
            space_check = space_check1 or space_check
        e_ships.append(Ship(1, int(x0), int(y0), int(x1), int(y1)))
    #show_field(e_ships)


def show_field(ships=None):
    """
    Функция вывода поля на экран
    """
    clear_field()
    if ships is None:
        ships = []
    print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
    for si in range(len(ships)):
        cords = ships[si]
        for j in range(len(cords.get_space)):
            cord_x = int(cords.get_space[j][0]) - 1
            cord_y = int(cords.get_space[j][1]) - 1
            try:
                if cord_x in range(0, 6) and cord_y in range(0, 6):
                    battlefield[cord_x][cord_y] = '◦'
            except IndexError:
                print(cord_x, cord_y)
        for j in range(len(cords.get_parts)):
            cord_x = int(cords.get_parts[j][0]) - 1
            cord_y = int(cords.get_parts[j][1]) - 1
            try:
                if cord_x in range(0, 6) and cord_y in range(0, 6):
                    battlefield[cord_x][cord_y] = '■'
            except IndexError:
                print(cord_x, cord_y)
    for si in range(6):
        stroka = ''
        stroka += f"{si + 1} |"
        for j in range(6):
            stroka += f' {battlefield[si][j]} |'
        print(stroka)
    print('*******************')


def clear_field():
    """
    Функция очистки игрового поля
    """
    battlefield.clear()
    for si in range(6):
        battlefield.append([])
        for j in range(6):
            battlefield[si].append('◯')


def game():
    """
    Реализация хода игры
    :return:
    """
    i = 0
    while True:
        i += 1
        if not i % 2:
            pleer_turn()


def pleer_turn():
    print("Ваш ход, введите координаты залпа через пробел:")
    shot = input()
    shot = list(map(int, shot.split()))



class Ship:
    """
    Класс создания кораблей хранит жизни, координатны корабля и пустого пространства вокруг,
    """

    def __init__(self, ship_type, x0, y0, x1=0, y1=0):
        self.parts = []  # Части корабля
        self.space = []  # Пространство между кораблями
        self.dead_cells = []  # Подбитые ячейки корабля
        self.size = ship_type
        self.health = int(self.size)
        if self.size in ('3', 3):
            self.parts = [[x0, y0], [int(x0 + x1) // 2, int(y0 + y1) // 2], [x1, y1]]
        elif self.size in ('2', 2):
            self.parts = [[x0, y0], [x1, y1]]
        else:
            self.parts = [[x0, y0]]
        for si in range(len(self.parts)):
            delta_y = -2
            for j in range(3):
                delta_x = -1
                delta_y += 1
                for k in range(3):
                    self.space.append([int(self.parts[si][0]) + delta_x, int(self.parts[si][1]) + delta_y])
                    delta_x += 1
        for j in range(self.size):
            for si in self.space:
                if (self.space.count(si) > 1) or (si[0] > 6) or (si[1] > 6):
                    self.space.remove(si)

    def hit(self, x, y):
        if [x, y] in self.get_parts:
            self.health -= 1
            if self.health == 0:
                return "Убил"
            else:
                self.dead_cells.append([x, y])
                return "Ранил"
        else:
            return "Мимо"

    @property
    def is_alive(self):
        if self.health == 0:
            return False
        else:
            return True

    @property
    def get_parts(self):
        """
        Возвращает координаты частей корабля
        :return:
        """
        return self.parts

    @property
    def get_space(self):
        """
        Возвращает координаты пространства между кораблями
        :return:
        """
        return self.space

    @property
    def get_type(self):
        return self.size


'''
■  ◉ ◯
'''

new_game()

for i in range(10):
    clear_field()
    enemy_ships()
