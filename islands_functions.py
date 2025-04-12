import math
from random import randint
from PIL import Image,ImageDraw


def get_height(noise_heightmap, x, y):
    h = noise_heightmap[int(2047 + x)//16, int(2047 + y)//16]
    m, h = 1 if h >= 0 else -1, abs(h)
    print(int(x), int(y), h, int(58 + m * math.tan((math.pi *h)/2)*math.exp(h)*(15/(1 + math.exp(-h)))))
    return min(200, max(-60, int(58 + m * math.tan((math.pi *h)/2)*math.exp(h)*(15/(1 + math.exp(-h))))))

#Базовая высота
def base_height():
    return randint(48, 68)

"""
arr список для визуальной картинки расположения. alf начальный угол, alf_step шаг угла. 
spread это разброс островов (ближе - дальше к центру), чтобы они не были четко на линии окружности
output_arr итоговый список с координатами островов
"""
def create_circle(arr: list,center: tuple,rad: int,alf: int,alf_step: tuple,spread: tuple, heightmap, image,output_arr):

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
    while alf < 628 - alf_step[1]*0.8:
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
            #По умолчанию высота, потом она меняется в зависимости от дальности колец и редкости островов
            output_arr.append([int(x), 0, int(y)])

            #Размер острова в зависимости от дистанции
            distance = ( x**2 + y**2 )**0.5
            if distance <= 150: #Только мелкие
                output_arr[-1].append(0)
                output_arr[-1][1] = get_height(heightmap, x, y)

            elif distance <= 250: #Мелкие и средние
                output_arr[-1].append(1)
                output_arr[-1][1] = get_height(heightmap, x, y)

            elif distance <= 500: #Мелкие, средние и большие (шанс меньше)
                output_arr[-1].append(2)
                output_arr[-1][1] = get_height(heightmap, x, y)

            else:
                output_arr[-1].append(3)
                output_arr[-1][1] = get_height(heightmap, x, y)
        except Exception as e:
            print(f"Ошибка: {e} на координатах x: {int(x)} y: {int(y)}")
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
        chance = randint(0,99)
        #10% на большой
        if chance < 10: return 2
        #65% средний
        if chance < 75: return 1
        #25 на мелкий
        return 0
    elif dist_num == 3:
        chance = randint(0, 99)
        # 70% на большой
        if chance < 70: return 2
        # 25% средний
        if chance < 95: return 1
        # 5 на мелкий
        return 0


dic_colors = {
    0: (255,255,255), #Маленький
    1: (35,255,30), #Средний
    2: (0,255,240), #Большой
    # 3: (20,0,255), #Огромный
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

        # Если остров большой, то в радиусе 30 блоков не должно быть никаких островов
        if size == 2:
            range_x = list(range(cur_x - 30, cur_x + 31))
            range_z = list(range(cur_z - 30, cur_z + 31))
            for cur in arr:
                if cur[0] in range_x and cur[2] in range_z: #Если нашелся остров в этом квадрате
                    if cur[0] != cur_x and cur[2] != cur_z: #При этом его координаты не равны исходному
                        size = 1
                        break

        # Если остров средний, то в радиусе 20 блоков не должно быть никаких островов
        if size == 1:
            range_x = list(range(cur_x - 20, cur_x + 21))
            range_z = list(range(cur_z - 20, cur_z + 21))
            for cur in arr:
                if cur[0] in range_x and cur[2] in range_z:  # Если нашелся остров в этом квадрате
                    if cur[0] != cur_x and cur[2] != cur_z:  # При этом его координаты не равны исходному
                        size = 0
                        break

        #Задаем размер
        arr[cur_island][3] = size

        #отрисовка
        for x in range(cur_x - 4, cur_x + 5):
            for y in range(cur_z - 4, cur_z + 5):
                image.point((x + 2047, y + 2047), fill=dic_colors[size])

def to_down(arr: list, current_index: int):
    if randint(0, 2) < 2:  # 2/3 на то что будет остров (структура) на -55
        arr[current_index][1] = randint(-55, -50)
    else:  # или выше
        arr[current_index][1] = randint(-20, 0)

def to_up(arr: list, current_index: int):
    arr[current_index][1] = randint(110, 190)

#Добавление высоких/низких островов при уловии, что остров средний или большой
def add_diffenent_heights(arr: list):
    for current in range(len(arr)):
        size = arr[current][-1]
        if size in [1,2]:
            chance = randint(0,99) #9% что опуститься вниз, 6% что поднимется вверх
            if chance < 9: to_down(arr, current)
            elif chance < 15: to_up(arr, current)
