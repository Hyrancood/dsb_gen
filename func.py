from random import randint
from PIL import Image,ImageDraw


relative_coords = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
relative_coords_cross = [(0,1),(0,-1),(1,0),(-1,0)]

#Обычный зум
def default_zoom(arr):
    list_arr = [[0 for x in range(len(arr)*2)] for n in range(len(arr)*2)]

    for x in range(len(arr)):
        for y in range(len(arr)):
            n = arr[x][y]

            list_arr[x * 2][y * 2] = n
            list_arr[x * 2 + 1][y * 2] = n
            list_arr[x * 2][y * 2 + 1] = n
            list_arr[x * 2 + 1][y * 2 + 1] = n

    return list_arr


#Шанс на замену цвета с соседнего пикселя
def change_color(old_biome,biome_template,chance = 30):
    if randint(0,99) < chance:
        return biome_template
    return old_biome



#Функция проверяет координаты. Если координаты клетки находятся в матрице, значит её можно использовать в качестве выбора
def check_position(arr,*coords):
    correct_positions = []

    for i in range(1,3):
        if all(0 <= x < len(arr) for x in coords[i]):
            correct_positions.append(coords[i])
    return correct_positions

#Если клетка находится на краю.
def zoom_if_cell_in_edge(arr,new_array,x,y,replace_chance):
    current_biome = arr[x][y]

    #4 новых клетки. Первый элемент - координаты новой клетки. Второй и третий
    #   это координаты соседних клеток в старой системе координат
    t = [
        [[x * 2, y * 2], [x, y - 1], [x - 1, y]],
        [[x*2+1, y * 2], [x - 1, y], [x, y + 1]],
        [[x * 2, y*2+1], [x, y + 1], [x + 1, y]],
        [[x*2+1, y*2+1], [x + 1, y], [x, y - 1]],
    ]

    for i in range(4):
        cur_x = t[i][0][0]
        cur_y = t[i][0][1]
        #Проверка координат, относительно текущей позиции
        coords = check_position(arr,*t[i])
        #Если нет подходящих координат (например пиксель в углу), значит цвет остается прежним
        if len(coords) == 0:
            new_array[cur_x][cur_y] = current_biome
        else:
            #Иначе, цвет может поменяться на соседний (а какой из двух соседних - рандом)
            mas = coords[randint(0,len(coords)-1)]
            new_biome = arr[mas[0]][mas[1]]
            new_array[cur_x][cur_y] = change_color(current_biome,new_biome,chance=replace_chance)

    return new_array


#Увеличение ширины и высоты матрицы x2, каждый пиксель = 4 новым таким же
#replace_chance - шанс замены пикселя на соседний в функции change_color
#ЧЕМ БОЛЬШЕ replace_chance, тем больше ШУМА
def zoom(arr,replace_chance=30):
    list_arr = [[0 for x in range(len(arr)*2)] for n in range(len(arr)*2)]

    for x in range(len(arr)):
        for y in range(len(arr)):
            n = arr[x][y]
#[ ][ ][ ]   [ ][ ][ ][ ]
#[0][*][ ]   [0][*][*][ ]
#[ ][1][ ]   [0][*][*][ ]
#            [ ][1][1][ ]
#С небольшим шансом пиксель будет заменяться на соседний. Начинаем с левого верхнего, выбираем какой пиксель он возьмет (50/50)
#   если верхний, значит его сосед справа возьмет правый, дальше по часовой нижний правый пиксель возьмет нижний, и последний возьмет левый
#   (то что возьмет его цвет, не означает, что поменяется, это только даёт нам то, на какой цвет он будет меняться, если шанс сработает)

            #Первый случай - исходный пиксель не находится на краю матрицы (вокруг него есть пиксели)
            if (0 < x < len(arr)-1) and (0 < y < len(arr)-1):
                #Если все 5 пикселей равны между собой, то просто x2
                if arr[x][y] == arr[x + 1][y] == arr[x - 1][y] == arr[x][y - 1] == arr[x][y + 1]:
                    list_arr[x * 2][y * 2] = n
                    list_arr[x * 2 + 1][y * 2] = n
                    list_arr[x * 2][y * 2 + 1] = n
                    list_arr[x * 2 + 1][y * 2 + 1] = n

                #Левый верхний пиксель берет шаблон с верхнего соседа
                elif randint(0,1) == 0:
                    bt = arr[x-1][y]

                    list_arr[x*2][y*2] = change_color(n,bt,chance=replace_chance)
                    list_arr[x*2][y*2+1] = change_color(n, arr[x][y+1],chance=replace_chance)
                    list_arr[x*2+1][y*2+1] = change_color(n, arr[x+1][y],chance=replace_chance)
                    list_arr[x*2+1][y*2] = change_color(n, arr[x][y-1],chance=replace_chance)
                #Левый верхний пиксель берет шаблон с левого соседа
                else:
                    bt = arr[x][y-1]

                    list_arr[x * 2][y * 2] = change_color(n, bt,chance=replace_chance)
                    list_arr[x * 2][y * 2 + 1] = change_color(n, arr[x-1][y],chance=replace_chance)
                    list_arr[x * 2 + 1][y * 2 + 1] = change_color(n, arr[x][y+1],chance=replace_chance)
                    list_arr[x * 2 + 1][y * 2] = change_color(n, arr[x+1][y],chance=replace_chance)
            #Второй случай - клетка у края
            else:
                list_arr = zoom_if_cell_in_edge(arr,list_arr,x,y,replace_chance)
    return list_arr

#Подсчет всех биомов выбранного типа
def biome_counter_on_map(arr,id_biome):
    return [_ for x in arr for _ in x].count(id_biome)


#Фунция вычисляет количество биомов вокруг заданной точки
#coords_for_checking принимает список с кортежами (), относительные координаты
#потом от заданной координаты будет находится точка, отклоненная на один шаг от заданной (и так все точки в списке)
def biomes_counter_around(arr,x,y,biome_number,coords_for_checking):
    count = 0

    for coord in coords_for_checking:
        new_x = x + coord[0]
        new_y = y + coord[1]

        if 0 <= new_x < len(arr) and 0 <= new_y < len(arr):
            if arr[new_x][new_y] == biome_number:
                count += 1

    return count

#Создание пикслея выбранного биома вместо указанного
def random_create_biome(replaceable_biome,new_biome,chance,arr):
    for x in range(len(arr)):
        for y in range(len(arr)):

            if arr[x][y] == replaceable_biome and randint(0,99) < chance:
                arr[x][y] = new_biome

#Спавн биома с определенным условием на другой биом вокруг, его количество
def spawn_biome_with_condition(old_biome,new_biome,biome_condition,count,arr,coords,chance):
    for x in range(len(arr)):
        for y in range(len(arr)):
            #Считает количество заданных биомов вокруг
            k = 0
            for current in biome_condition:
                k += biomes_counter_around(arr,x,y,current,coords)

            if arr[x][y] == old_biome and k in count:
                if randint(0,chance[0]) < chance[1]:
                    arr[x][y] = new_biome

#Расширяет биом. Если данного биомога вокруг (coords_list) меньше чем нужно (count_biomes
#_around), то с шансом chance(99,3) создаст биом
def expand_biome(old_biomes,new_biome,coords_list,count_biomes_around,chance,arr):
    for x in range(len(arr)):
        for y in range(len(arr)):

            count_biomes = biomes_counter_around(arr,x,y,new_biome,coords_list)

            if arr[x][y] in old_biomes and count_biomes >= count_biomes_around:
                if randint(0,chance[0]) < chance[1]:
                    arr[x][y] = new_biome

#Удаляет одиночный биом, заменяет его на землю, если вокруг (заданные координаты) нет нужного биома
def remove_solo_biome(biome,new_biome,coords_list,chance,arr):
    for x in range(len(arr)):
        for y in range(len(arr)):

            k = biomes_counter_around(arr, x, y, biome, coords_list)
            if arr[x][y] == biome and k == 0:
                if randint(0,chance[0]) < chance[1]: arr[x][y] = new_biome
                # arr[x][y] = 0

#Удаление рек, рядом с которыми нет нужных биомов
def remove_selected_biome(input_arr,latest_arr,id_biome,search_list,coords):
    output_arr = [x.copy() for x in input_arr]
    for x in range(1, len(input_arr) - 1):
        for y in range(1, len(input_arr) - 1):

            if input_arr[x][y] != id_biome:
                continue
            else:
                k = 0
                for current_biome in search_list:
                    k += biomes_counter_around(input_arr,x,y,current_biome,coords)
                if k==0:
                    output_arr[x][y] = latest_arr[x][y]
    return output_arr

#Удаление биома, если у него нет нужных соседей в нужном количестве (берет из прошлой версии матрицы)
def replace_biome_if_count(input_arr,latest_arr,id_biome,search_list,coords,count):
    # output_arr = [x.copy() for x in input_arr]
    for x in range(1, len(input_arr) - 1):
        for y in range(1, len(input_arr) - 1):

            if input_arr[x][y] != id_biome:
                continue
            else:
                k = 0
                for current_biome in search_list:
                    k += biomes_counter_around(input_arr,x,y,current_biome,coords)
                if k in count:
                    input_arr[x][y] = latest_arr[x][y]
    return input_arr

#Замена биомов на новый если рядом есть искомые (search_biomes)
def replace(arr,replaceable_biome,search_biomes,new_biome,coords_list):
    for x in range(len(arr)):
        for y in range(len(arr)):

            k = 0
            for current_biome in search_biomes:
                k += biomes_counter_around(arr, x, y, current_biome, coords_list)

            if arr[x][y] in replaceable_biome and k>0:
                arr[x][y] = new_biome

#Замена на краях выбранных биомов на реки
def replace_to_river(arr,replaceable_biome,search_biomes,coords_list):
    for x in range(len(arr)):
        for y in range(len(arr)):
            k = 0
            for current_biome in search_biomes:
                k += biomes_counter_around(arr, x, y, current_biome, coords_list)
            rivers = biomes_counter_around(arr,x,y,16,coords_list)

            if arr[x][y] in replaceable_biome and k>0 and rivers<3:
                arr[x][y] = 16

# def fill_biomes(arr):
#     for x in range(1,len(arr)-1):
#         for y in range(1,len(arr)-1):
#
#             if randint(0,1)==0: current_biome = arr[x-1][y]
#             else: current_biome = arr[x][y-1]
#
#             k = biomes_counter_around(arr,x,y,current_biome,relative_coords_cross)
#             if k>=3:
#                 arr[x][y] = current_biome
#     return arr



# #Если пиксель вода и вокруг есть >3 воды, то 70% что станет песком
# #Если пиксель не песок, то 5%, что им станет
# #Если блок - земля и рядом (крест) есть 2 песка, то 2/3 шанс что станет песком
# #Если это блок земли, вокруг (крест) есть блок воды и вокруг есть 1 песок, то 1/3 на песок
# #2/3 на удаление одиночного песка
# #Если блок земли и рядом нет песка - 10% снег
# #Если рядом нет песка и есть 1 сне, то 1/3 что станет снегом
# #Если рядом нет снега - земля



