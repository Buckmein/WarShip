import random

battlefield = [[]]
enemy_battlefield = [[]]
ships = []
e_ships = []


def ship_input():
    """
    Ввод кораблей игрока
    :return:
    """
    global ships
    ships.clear()
    print("Хотите самостоятельно разместить корабли ? y - Да, n - Нет")
    ok = True
    rand = input()
    if rand == 'n':
        while ok:
            ships = rand_ships()
            show_field(ships)
            print("Если поле осталось пустым перерасположите корабли")
            print("Играем или расположить корабли подругому?  y - Играем, n - Расположить по-другому")
            if input() != 'n':
                ok = False
    else:
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
                        break
                    else:
                        cords_check = False

            ships.append(Ship(ship_type, *cords0, *cords1))
            ostatok[int(ship_type) - 1] -= 1


def enemy_input():
    global e_ships
    e_ships = rand_ships()


def rand_ships():
    """
    Создание кораблей оппонента
    :return:
    """
    side = []
    side.clear()
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
    side.append(Ship(3, int(x0), int(y0), int(x1), int(y1)))
    for si in range(2):
        space_check = True
        while space_check:
            space_check1 = False
            tries += 1
            if tries > 999:
                side = rand_ships()
                return side
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
            for j in range(len(side)):
                if ([x0, y0] not in side[j].get_parts) and ([x0, y0] not in side[j].get_space) \
                        and ([x1, y1] not in side[j].get_parts) and ([x1, y1] not in side[j].get_space):
                    space_check = False
                else:
                    space_check1 = True
            space_check = space_check1 or space_check
        side.append(Ship(2, int(x0), int(y0), int(x1), int(y1)))
    for si in range(4):
        space_check = True
        while space_check:
            tries += 1
            space_check1 = False
            if tries > 999:
                side = rand_ships()
                return side
            x0 = random.randint(1, 6)
            x1 = x0
            y0 = random.randint(1, 6)
            y1 = y0
            for j in range(len(side)):
                if ([x0, y0] not in side[j].get_parts) and ([x0, y0] not in side[j].get_space):
                    space_check = False
                else:
                    space_check1 = True
            space_check = space_check1 or space_check
        side.append(Ship(1, int(x0), int(y0), int(x1), int(y1)))
    return side


def show_field(ships1=None, enemy=False):
    """
    Функция вывода поля на экран
    """
    clear_field()
    if ships1 is None:
        ships1 = []
    print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
    if enemy:
        for si in range(len(ships1)):
            cords = ships1[si]
            if cords.is_alive:
                pass
            else:
                for j in range(len(cords.get_space)):
                    cord_x = int(cords.get_space[j][0]) - 1
                    cord_y = int(cords.get_space[j][1]) - 1
                    if cord_x in range(0, 6) and cord_y in range(0, 6):
                        battlefield[cord_x][cord_y] = '◦'
            for j in range(len(cords.dead_cells)):
                cord_x = int(cords.dead_cells[j][0]) - 1
                cord_y = int(cords.dead_cells[j][1]) - 1
                try:
                    if cord_x in range(0, 6) and cord_y in range(0, 6):
                        battlefield[cord_x][cord_y] = '╳'
                except IndexError:
                    print(cord_x, cord_y)
    else:
        for si in range(len(ships1)):
            cords = ships1[si]
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
            for j in range(len(cords.dead_cells)):
                cord_x = int(cords.dead_cells[j][0]) - 1
                cord_y = int(cords.dead_cells[j][1]) - 1
                try:
                    if cord_x in range(0, 6) and cord_y in range(0, 6):
                        battlefield[cord_x][cord_y] = '╳'
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
    step = 0
    end = False
    while not end:
        step += 1
        if not step % 2:
            show_field(e_ships, enemy=True)
            end = player_turn()
        else:
            end = enemy_turn()

    new_game()


def player_turn():
    """
    Ход игрока, в случае победы возвращает True
    :return:
    """
    win = True
    for i in e_ships:
        win *= not i.is_alive
    if win:
        print("Вы победили!!!!")
        return win
    else:
        shot = ''  # Координаты выстрела
        try:
            print("Ваш ход, введите координаты залпа через пробел:")
            shot = input()
            shot = list(map(int, shot.split()))
        except ValueError:
            print("Ошибка ввода")
            return player_turn()

        try:
            for i in e_ships:
                if shot not in i.dead_cells and shot in i.get_parts:
                    if i.hit(*shot):
                        if i.is_alive:
                            print("Ранил!!!")
                            show_field(e_ships, True)
                            player_turn()
                            return False
                        else:
                            show_field(e_ships, True)
                            print("Убил!!!")
                            player_turn()
                            return False
                else:
                    print("Промах(((")
                    return False
        except TypeError:
            print("Ошибка ввода")
            return player_turn()


def enemy_turn():
    """
    Ход противника, в случае вашего проигрыша возвращает True
    :return:
    """
    lose = True
    for i in ships:
        lose *= not i.is_alive
    if lose:
        print("Вы проиграли(((")
        return lose
    else:
        shot_x = random.randint(1, 6)
        shot_y = random.randint(1, 6)
        for i in ships:
            if [shot_x, shot_y] not in i.dead_cells:
                if i.hit(shot_x, shot_y):
                    if i.is_alive:
                        show_field(ships)
                        print(shot_x, shot_y)
                        print("Ваш корабль подбит")
                        show_field(ships)
                        return enemy_turn()

                    else:
                        show_field(ships)
                        print(shot_x, shot_y)
                        print("Ваш корабль пошел ко дну")
                        return enemy_turn()
            else:
                print("Противник промахнулся)))")
                return False
        else:
            return enemy_turn()


class Ship:
    """
    Класс создания кораблей хранит жизни, координатны корабля и пустого пространства вокруг,
    """

    def __init__(self, ship_type, x0, y0, x1=0, y1=0):
        self.parts = []  # Части корабля
        self.space = []  # Пространство между кораблями
        self.dead_cells = []  # Подбитые ячейки корабля
        self.size = ship_type
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
            self.dead_cells.append([x, y])
            return True
        else:
            return False

    @property
    def is_alive(self):
        if len(self.dead_cells) == self.size:
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


def new_game():
    """
    Функция начала новой игры
    """
    show_field()
    ship_input()
    enemy_input()
    game()


new_game()
