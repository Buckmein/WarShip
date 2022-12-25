import random

battlefield = [[]]
enemy_battlefield = [[]]


def new_game():
    """
    Функция начала новой игры 
    """
    clear_field()
    show_field()
    ship_input()


def ship_input():
    """
    Ввод кораблей игрока
    :return:
    """
    ships = []
    ships.clear()
    ostatok = [4, 2, 1]
    for i in range(7):
        type_check = True
        cords_check = True
        while type_check:
            print(
            f"У вас осталось: {ostatok[2]} Трехмачтовых, {ostatok[1]} Двумачтовых и {ostatok[0]} Одномачтовых кораблей")
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
                cords0 = map(int, ship_cords.split())
                cords1 = cords0
            else:
                print("Введите координаты начала через пробел")
                ship_cords = input()
                cords0 = map(int, ship_cords.split())
                print("Введите координаты конца через пробел")
                ship_cords = input()
                cords1 = map(int, ship_cords.split())
            if len(ships) == 0:
                cords_check = False
            for j in range(len(ships)):
                if cords0 in ships[j].get_space or cords1 in ships[j].get_space \
                        or cords0 in ships[j].get_parts or cords1 in ships[j].get_parts:
                    print("!!!корабль не вмещается, попробуйте другое место!!!")
                else:
                    cords_check = False

        ships.append(Ship(ship_type, *cords0, *cords1))
        ostatok[int(ship_type) - 1] -= 1
        show_field(ships)


def enemy_ships():
    """
    Создание кораблей опонента ДОПИСАТЬ
    :return:
    """
    e_ships = []
    e_ships.clear()
    x0 = random.randint(0, 5)
    if x0 > 4:
        x1 = x0 - 2
        moved = True
    elif x0 < 3:
        x1 = x0 + 2
        moved = True
    y0 = random.randint(0, 5)
    if y0 >= 3 and not moved:
        y1 = y0 - 2
    elif not moved:
        y1 = y0 + 2
    e_ships.append(Ship(3, x0, y0, x1, y1))
    for i in range(2):
        space_check = True
        while space_check:
            x0 = random.randint(0, 5)
            y0 = random.randint(0, 5)
            if x0 > 3:
                x1 = x0 - 2
                moved = True
            elif x0 < 2:
                x1 = x0 + 2
                moved = True
            if y0 >= 2 and not moved:
                y1 = y0 - 2
            elif not moved:
                y1 = y0 + 2
            for i in range(len(e_ships)):
                if [x0, y0] not in e_ships[i].get_parts or [x0, y0] not in e_ships[i].get_space or \
                        [x1, y1] not in e_ships[i].get_parts or [x1, y1] not in e_ships[i].get_space:
                    space_check = False
        e_ships.append(Ship(2, int(x0), int(y0), int(x1), int(y1)))
    for i in range(2):
        space_check = True
        while space_check:
            x0 = random.randint(0, 5)
            y0 = random.randint(0, 5)
            for i in range(len(e_ships)):
                if [x0, y0] not in e_ships[i].get_parts or [x0, y0] not in e_ships[i].get_space:
                    space_check = False
        e_ships.append(1, int(x0), int(y0))


def show_field(ships=[]):
    """
    Функциявывода поля на экран
    """
    print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
    if ships != 0:
        for i in range(len(ships)):
            cords = ships[i]
            for j in range(len(cords.get_space)):
                cord_x = int(cords.get_space[j][0]) - 1
                cord_y = int(cords.get_space[j][1]) - 1
                if cord_x >= 0 and cord_y >= 0:
                    battlefield[cord_x][cord_y] = '●'
            for j in range(len(cords.get_parts)):
                cord_x = int(cords.get_parts[j][0]) - 1
                cord_y = int(cords.get_parts[j][1]) - 1
                if cord_x >=0 and cord_y >= 0:
                    battlefield[cord_x][cord_y] = '■'
    for i in range(6):
        stroka = ''
        stroka += f"{i + 1} |"
        for j in range(6):
            stroka += f' {battlefield[i][j]} |'
        print(stroka)


def clear_field():
    """
    Функция очистки игрового поля
    """
    battlefield.clear()
    for i in range(6):
        battlefield.append([])
        for j in range(6):
            battlefield[i].append('◯')


def game():
    """
    Реализация хода игры
    :return:
    """


class Ship:
    """
    Класс создания кораблей хранит жизни, координтаны корабля и пустого пространства вокруг,
    """

    def __init__(self, ship_type, x0, y0, x1=0, y1=0):
        self.parts = []  # Части корабля
        self.space = []  # Пространство между кораблями
        self.size = ship_type
        self.health = int(self.size)
        if self.size == '3':
            self.parts = [[x0, y0], [int(x0 + x1) // 2, int(y0 + y1) // 2], [x1, y1]]
        elif self.size == '2':
            self.parts = [[x0, y0], [x1, y1]]
        else:
            print(1)
            self.parts = [[x0, y0]]
        for i in range(len(self.parts)):
            delta_y = -2
            for j in range(3):
                delta_x = -1
                delta_y += 1
                for k in range(3):
                    self.space.append([int(self.parts[i][0]) + delta_x, int(self.parts[i][1]) + delta_y])
                    delta_x += 1

    def hit(self, x, y):
        if [x, y] in self.get_parts:
            self.health -= 1
            if self.health == 0:
                return "Убил"
            else:
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
