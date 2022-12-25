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
    Ввод кораблейигрока
    :return:
    """
    ships = []
    ostatok = [4, 2, 1]
    for i in range(7):
        type_check = True
        print(f"У вас осталось: {ostatok[2]} Трехмачтовых, {ostatok[1]} Двумачтовых и {ostatok[0]} Одномачтовых кораблей\n")
        while type_check:
            print("Введите тип корабля который хотите разместить")
            ship_type = input()
            if ship_type in ('1', '2', '3') and ostatok[int(ship_type)-1] != 0:
                type_check = False
            else:
                print("Нет такого типа кораблей")
        if ship_type == "1":
            print("Введите координаты через пробел")
            ship_cords = input()
        else:
            print("Введите координаты начала через пробел")
            ship_cords = input()
            print("Введите координаты конца через пробел")
            ship_cords += " " + input()
        ship_cords = map(int, ship_cords.split())
        ships.append(Ship(ship_type, *ship_cords))
        ostatok[int(ship_type)-1] -= 1
        show_field()


def enemy_ships():
    """
    Создание кораблей опонента ДОПИСАТЬ
    :return:
    """
    e_ships = []
    e_ships.clear()
    x0 = random.randint(0, 5)
    if x0 > 4:
        x1 = x0-2
        moved = True
    elif x0 < 3:
        x1 = x0+2
        moved = True
    y0 = random.randint(0, 5)
    if y0 >= 3 and not moved:
        y1 = y0-2
    elif not moved:
        y1 = y0+2
    e_ships.append(Ship(3, x0, y0, x1, y1))
    for i in range(2):
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
        e_ships.append(Ship(2, int(x0), int(y0), int(x1), int(y1)))


def show_field():
    """
    Функциявывода поля на экран
    """
    print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
    for i in range(6):
        stroka = ''
        stroka += f"{i+1} |"
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
            battlefield[i].append('O')


def game():
    """
    Реализация хода игры
    :return:
    """


class Ship:
    """
    Класс создания кораблей хранит делает
    """

    def __init__(self, ship_type, x0, y0, x1=0, y1=0):
        parts = [[]]  # Части корабля
        space = []  # Пространство между кораблями
        size = ship_type
        health = int(size)
        if size == '3':
            parts = [[x0, y0], [int(x0+x1)//2, int(y0+y1)//2], [x1, y1]]
        elif size == '2':
            parts = [[x0, y0], [x1, y1]]
        else:
            print(1)
            parts = [[x0, y0]]
        for i in range(len(parts)):
            delta_y = -2
            for j in range(3):
                delta_x = -1
                delta_y += 1
                for k in range(3):
                    space.append([int(parts[i][0])+delta_x, int(parts[i][1])+delta_y])
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
■
'''
new_game()

