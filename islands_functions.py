import math
from random import randint
from PIL import Image,ImageDraw

#Базовая высота
def base_height():
    return randint(45, 68)

"""
arr список для визуальной картинки расположения. alf начальный угол, alf_step шаг угла. 
spread это разброс островов (ближе - дальше к центру), чтобы они не были четко на линии окружности
output_arr итоговый список с координатами островов
"""
def create_circle(arr: list,center: tuple,rad: int,alf: int,alf_step: tuple,spread: tuple, image,output_arr):

    #зеленые полосы
    for x in range(628): #628, потому что длина окружности 2пи, 6,28 * 100 масштаб
        tx = rad * math.sin(x / 100) + center[0]
        ty = rad * math.cos(x / 100) + center[1]
        try:
            if image != None:
                image.point((tx + 2047, ty + 2047), fill="green")
        except:
            continue

    #Обход окружности
    while (alf < 628 - alf_step[1]*0.8):
        #точка со случайным смещением ближе/дальше от центра spread)
        x = rad * math.sin(alf / 100) + center[0] + randint(spread[0], spread[1])
        y = rad * math.cos(alf / 100) + center[1] + randint(spread[0], spread[1])
        #Шаг угла
        alf += randint(alf_step[0], alf_step[1])

        #Ограничение по карте
        if not(-2045 <= x <= 2045) or not(-2045 <= y <= 2045):
            continue

        try:
            #обрисовка острова цветов на картинке
            for cur_x in range(int(x) - 4, int(x) + 5):
                for cur_y in range(int(y) - 4, int(y) + 5):
                    arr[cur_x][cur_y] = 1
            #По умолчанию высота -100, потом она меняется в зависимости от дальности колец и редкости островов
            output_arr.append([int(x), -100, int(y)])

            #Размер острова в зависимости от дистанции
            distance = ( x**2 + y**2 )**0.5
            if distance <= 150: #Только мелкие
                output_arr[-1].append(0)
                output_arr[-1][1] = base_height()

            elif distance <= 250: #Мелкие и средние
                output_arr[-1].append(1)
                chance = randint(0,99)
                if chance < 13: #Шанс 13% что остров опуститься вниз
                    output_arr[-1][1] = randint(-10, 15)  # Высота
                elif 13 <= chance < 20: #7% на высокий остров
                    output_arr[-1][1] = randint(150, 300)
                else:
                    output_arr[-1][1] = base_height()

            elif distance <= 500: #Мелкие и средние
                output_arr[-1].append(2)
                chance = randint(0, 99)
                if chance < 17: # Шанс 17% что остров опуститься вниз
                    output_arr[-1][1] = randint(-20, 15)  # Высота
                elif 17 <= chance < 23: #6% на высокий остров
                    output_arr[-1][1] = randint(150, 300)
                else:
                    output_arr[-1][1] = base_height()

            #500-650 - 6ое кольцо, добавляем один остров с Морским царем
            # elif 500 <= distance <= 650:
            #     output_arr[-1].append(101)
            #     output_arr[-1][1] = base_height()




            elif distance <= 980: #Маленькие, большие, средние
                output_arr[-1].append(3)
                if randint(0, 9) < 2: #20% что опуститься вниз
                    if randint(0,2) < 2: #2/3 на то что будет остров (структура) на -55
                        output_arr[-1][1] = randint(-55, -45)
                    else: #или выше
                        output_arr[-1][1] = randint(-30, 10)  # Высота
                else:
                    output_arr[-1][1] = base_height()

            elif distance <= 1500: #+огромные
                output_arr[-1].append(4)
            else:
                output_arr[-1].append(5)
        except:
            continue


def rare_chance(dist_num: int):
    size = [0,1,2,3] #Размеры
    if dist_num == 0:
        return 0
    elif dist_num == 1:
        #20% средний
        if randint(0,9) < 2: return 1
        #80 на мелкий
        return 0
    elif dist_num == 2:
        #70% средний
        if randint(0,9) < 7: return 1
        #30 на мелкий
        return 0
    elif dist_num == 3:
        chance = randint(0,99)
        #62% средний
        if chance < 62: return 1
        #23% на большой
        elif 62 <= chance < 88: return 2
        #15% на маленький
        return 0
    elif dist_num == 4:
        chance = randint(0, 99)
        # 34% большой
        if chance < 34: return 2
        # 29% на средний
        elif 34 <= chance < 63: return 1
        # 32 на огромный
        elif 63 <= chance < 95: return 3
        # 5% на маленький
        return 0
    elif dist_num == 5:
        chance = randint(0, 99)
        # 35% большой
        if chance < 35: return 2
        # 25% на средний
        elif 35 <= chance < 60: return 1
        # 40 на огромный
        elif 60 <= chance < 99: return 3
        # 1% на маленький
        return 0


dic_colors = {
    0: (255,255,255), #Маленький
    1: (35,255,30), #Средний
    2: (0,255,240), #Большой
    3: (20,0,255), #Огромный
    101: (224,34,208),
    102: (246,255,0),
    103: (255,126,0),
    104: (255,0,0)
       }



def give_size(arr: list, image):
    #Житель квестовый
    #Подходящие позиции, то есть острова на первых двух линиях
    quests = [cur for cur in arr if 80 <= (cur[0]**2 + cur[2]**2)**0.5 <= 160]
    index = randint(0, len(quests)-1)
    quests[index][3] = 101
    # #Морской царь
    # quests = [cur for cur in arr if 500 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 <= 650]
    # index = randint(0, len(quests) - 1)
    # quests[index][3] = 102
    # #Песчаная библиотека
    # quests = [cur for cur in arr if 830 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 <= 920]
    # index = randint(0, len(quests) - 1)
    # quests[index][3] = 103
    # #Элеум Лойс
    # quests = [cur for cur in arr if 1430 <= (cur[0] ** 2 + cur[2] ** 2) ** 0.5 <= 1700]
    # index = randint(0, len(quests) - 1)
    # quests[index][3] = 104


    for cur_island in range(len(arr)):
        cur_x = arr[cur_island][0]
        cur_z = arr[cur_island][2]

        if arr[cur_island][3] in (101,102,103,104):
            # отрисовка квестового острова
            for x in range(cur_x - 4, cur_x + 5):
                for y in range(cur_z - 4, cur_z + 5):
                    image.point((x + 2047, y + 2047), fill=dic_colors[arr[cur_island][3]])
            continue

        #В зависимости от дальности разный размер
        size = rare_chance(arr[cur_island][3])
        #Высота
        if arr[cur_island][1] == -100:
            if size == 2:
                if randint(0, 9) < 1:  # 10% что опуститься вниз
                    if randint(0, 2) < 2:  # 2/3 на то что будет остров (структура) на -55
                        arr[cur_island][1] = randint(-55, -45)
                    else:  # или выше
                        arr[cur_island][1] = randint(-30, 10)  # Высота
                else:
                    arr[cur_island][1] = base_height()
            elif size == 3:
                if randint(0, 99) < 5:  # 5% что опуститься вниз
                    if randint(0, 2) < 1:  # 1/3 на то что будет остров (структура) на -55
                        arr[cur_island][1] = randint(-55, -45)
                    else:  # или выше
                        arr[cur_island][1] = randint(-30, 10)  # Высота
                else:
                    arr[cur_island][1] = base_height()
            else:
                arr[cur_island][1] = base_height()


        # Если остров огромный, то в радиусе 80 блоков не должно быть никаких островов
        if size == 3:
            range_x = list(range(cur_x - 80, cur_x + 81))
            range_z = list(range(cur_z - 80, cur_z + 81))
            for cur in arr:
                if cur[0] in range_x and cur[2] in range_z: #Если нашелся остров в этом квадрате
                    if cur[0] != cur_x and cur[2] != cur_z: #При этом его координаты не равны исходному
                        size = 2
                        break

        # Если остров большой, то в радиусе 50 блоков не должно быть никаких островов
        if size == 2:
            range_x = list(range(cur_x - 50, cur_x + 51))
            range_z = list(range(cur_z - 50, cur_z + 51))
            for cur in arr:
                if cur[0] in range_x and cur[2] in range_z: #Если нашелся остров в этом квадрате
                    if cur[0] != cur_x and cur[2] != cur_z: #При этом его координаты не равны исходному
                        size = 1
                        break

        # Если остров средний, то в радиусе 30 блоков не должно быть никаких островов
        if size == 1:
            range_x = list(range(cur_x - 30, cur_x + 31))
            range_z = list(range(cur_z - 30, cur_z + 31))
            for cur in arr:
                if cur[0] in range_x and cur[2] in range_z:  # Если нашелся остров в этом квадрате
                    if cur[0] != cur_x and cur[2] != cur_z:  # При этом его координаты не равны исходному
                        size = 1
                        break



        #Задаем размер
        arr[cur_island][3] = size

        #отрисовка
        for x in range(cur_x - 4, cur_x + 5):
            for y in range(cur_z - 4, cur_z + 5):
                image.point((x + 2047, y + 2047), fill=dic_colors[size])

#Добавление высоких островов при уловии, что остров средний или большой
def add_high_islands(arr: list):
    for current in range(len(arr)):
        if arr[current][-1] in [1,2] and arr[current][1] in list(range(45,70)):
            if randint(0,99) < 8:
                arr[current][1] = randint(150,300)
