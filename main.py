battlefield = [[]]


def new_game():
    """
    Функция начала новой игры 
    """
    ship = []
    ostatok = [4, 2, 1]
    clear_field()
    show_field()
    for i in range(7):
        print(f"У вас осталось: {ostatok[2]} Трехмачтовых, {ostatok[1]} Двумачтовых и {ostatok[0]} Одномачтовых кораблей\n")
        print("Введите тип корабля который хотите разместить")
        ship_type = input()
        if ship_type == "1":
            print("Введите координаты через пробел")
            ship_cords = input()
        else:
            print("Введите координаты начала через пробел")
            ship_cords = input()
            print("Введите координаты конца через пробел")
            ship_cords += " " + input()
        ship_cords = ship_cords.split()
        print(ship_cords)
        ship.append(Ship(ship_type, *ship_cords))
        ostatok[int(ship_type)-1] -= 1
        show_field()


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
    Реализация ходов
    :return:
    """


class Ship:
    """
    Класс создания кораблей хранит делает
    """

    def __init__(self, ship_type, x0, y0, x1=0, y1=0):
        cords_begin = x0, y0
        cords_end = x1, y1
        type = ship_type

    @property
    def get_cords(self):
        return self.cords_begin, self.cords_end


new_game()

