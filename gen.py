from random import randint
from PIL import Image,ImageDraw


def zoom(arr):
    list_arr = [[0 for x in range(len(arr)*2)] for n in range(len(arr)*2)]

    for x in range(len(arr)):
        for y in range(len(arr)):
            n = arr[x][y]

            list_arr[x * 2][y * 2] = n
            list_arr[x * 2 + 1][y * 2] = n
            list_arr[x * 2][y * 2 + 1] = n
            list_arr[x * 2 + 1][y * 2 + 1] = n

    return list_arr


#Фунция вычисляет количество биомов вокруг заданной точки
#coords_for_checking принимает список с кортежами (), относительные координаты
#потом от заданной координаты будет находится точка, отклоненная на один шаг от заданной (и так все точки в списке)
def biomes_counter(arr,x,y,biome_number,coords_for_checking):
    oceans = 0

    for coord in coords_for_checking:
        new_x = x + coord[0]
        new_y = y + coord[1]

        if 0 <= new_x < len(arr) and 0 <= new_y < len(arr):
            if arr[new_x][new_y] == biome_number:
                oceans += 1

    return oceans


arr = [[0 for n in range(16)] for j in range(16)]

file = open(r'D:\Games\Minecraft\game\saves\Generator\datapacks\generator\data\gen\functions\test.mcfunction','w',encoding='utf-8')
temp_file = open(r'D:\Games\Minecraft\game\saves\Generator\datapacks\generator\data\gen\functions\old.mcfunction','w',encoding='utf-8')
zoom_x4_list = open(r'D:\Games\Minecraft\game\saves\Generator\datapacks\generator\data\gen\functions\zoom_x4_list.mcfunction','w',encoding='utf-8')


#9% шанс, что пиксель станет океаном
for x in range(16):
    for y in range(16):
        #в print(randint(0,9))
        if (randint(0,99) in range(0,8+1)):
            arr[x][y] = 1

#добавление воды
for x in range(16):
    for y in range(16):
        k = biomes_counter(arr,x,y,1,[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)])

        # если сейчас пиксель - вода и вокруг нет воды, то 50% что станет землей
        if arr[x][y] == 1 and k == 0:
            if randint(0, 1) == 0:
                arr[x][y] = 0
        #Если сейчас земля и вокруг больше одной воды, то станет водой (20%)
        elif arr[x][y] == 0 and k >= 2:
            if randint(0,9) in (0,1):
                arr[x][y] = 1

#Если пиксель вода и вокруг есть >3 воды, то 70% что станет песком
for x in range(16):
    for y in range(16):
        k = biomes_counter(arr, x, y, 1,[(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

        if arr[x][y] == 1 and k>3:
            if randint(0,9) in range(0,6+1):
                arr[x][y] = 2




#Если пиксель не песок, то 5%, что им станет
for x in range(16):
    for y in range(16):

        if arr[x][y] != 2:
            if randint(0,99) in range(0,4+1):
                arr[x][y] = 2

#Если блок - земля и рядом (крест) есть 2 песка, то 2/3 шанс что станет песком
for x in range(16):
    for y in range(16):

        k = biomes_counter(arr,x,y,2,[(0,1),(0,-1),(1,0),(-1,0)])

        if arr[x][y] == 0 and k >= 2:
            if randint(0,3) in (0,1,3):
                arr[x][y] = 2

#Если это блок земли, вокруг (крест) есть блок воды и вокруг есть 1 песок, то 1/3 на песок
for x in range(16):
    for y in range(16):

        k = biomes_counter(arr,x,y,2,[(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
        oceans = biomes_counter(arr, x, y, 1, [(0,1),(0,-1),(1,0),(-1,0)])

        if arr[x][y] == 0 and k >= 1 and oceans >= 1:
            if randint(0,2) == 0:
                arr[x][y] = 2

#2/3 на удаление одиночного песка
for x in range(16):
    for y in range(16):
        k = biomes_counter(arr, x, y, 2, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

        if arr[x][y] == 2 and k==0:
            if randint(0,2) in (0,1):
                arr[x][y] = 0




#Если блок земли и рядом нет песка - 10% снег
for x in range(16):
    for y in range(16):
        k = biomes_counter(arr, x, y, 2, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

        if arr[x][y] == 0 and k == 0:
            if randint(0, 9) == 0:
                arr[x][y] = 3

#Если рядом нет песка и есть 1 сне, то 1/3 что станет снегом
for x in range(16):
    for y in range(16):
        k = biomes_counter(arr, x, y, 3, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
        sand = biomes_counter(arr, x, y, 2, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

        if arr[x][y] == 0 and sand==0 and k >= 1:
            if randint(0, 3) == 0:
                arr[x][y] = 3
#Если рядом нет снега - земля
for x in range(16):
    for y in range(16):
        k = biomes_counter(arr, x, y, 3, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

        if arr[x][y] == 3 and k==0:
            # if randint(0,2) in (0,1):
            arr[x][y] = 0


# temp_file.write(f'data modify storage dsbgen:start List set value {arr}')


# file.write(f'data modify storage dsbgen:start List set value {arr}')


# zoom_x4_list.write(f'data modify storage dsbgen:start List set value {arr}')

arr = zoom(arr)

new_img = Image.new("RGBA", (len(arr),len(arr)), "black")
img = ImageDraw.Draw(new_img)
dic = {0: "green", 1: "blue", 2: "yellow", 3: "white"}
for x in range(len(arr)):
    for y in range(len(arr)):

        img.point((x,y),fill = dic[arr[x][y]] )

# new_img.save(r"C:\Users\Максим\Desktop\test.png",dpi = (3,3))
new_img.save("test.png",dpi = (3,3))


###Версия Хуры
# for x in range(16):
#     for y in range(16):
#         if arr[x][y] == 1:
#             if not(any(arr[i][j] == 1 and [x==i,y==j].count(True)!=2 for j in range(max(0, y-1), min(15, y+1)+1) for i in range(max(0, x-1), min(15, x+1)+1))):
#                 print('yes')
#                 arr[x][y] = 0
###Версия хура 2.0
# for x in range(16):
#     for y in range(16):
#         if arr[x][y] == 1:
#             flag = False
#             for i in range(max(0, x-1), min(15, x+1)+1):
#                 for j in range(max(0, y-1), min(15, y+1)+1):
#                     if arr[i][j] == 1 and [x==i,y==j].count(True)!=2:
#                         flag = True
#                         break
#             if not flag:
#                 arr[x][y] = 0



