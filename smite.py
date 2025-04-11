from random import randint
from PIL import Image,ImageDraw
from func import *
from colors import *



# file = open(r'D:\Games\Minecraft\game\saves\Generator\datapacks\generator\data\gen\functions\test.mcfunction','w',encoding='utf-8')
# temp_file = open(r'D:\Games\Minecraft\game\saves\Generator\datapacks\generator\data\gen\functions\old.mcfunction','w',encoding='utf-8')
# zoom_x4_list = open(r'D:\Games\Minecraft\game\saves\Generator\datapacks\generator\data\gen\functions\zoom_x4_list.mcfunction','w',encoding='utf-8')

# #Вода
# for x in range(20):
#     if biome_counter_on_map(arr,1) > 8:
#         break
#     random_create_biome(0,1,6,arr)
# for x in range(2):
#     expand_biome([0],1,relative_coords,2,(6,1),arr)
# remove_solo_biome(1,0,relative_coords,(2,1),arr)
#
# #Песок
# for x in range(20):
#     if biome_counter_on_map(arr,2) > 12:
#         break
#     random_create_biome(0,2,5,arr)
# expand_biome([0],2,relative_coords_cross,1,(9,4),arr)

def create():
    arr = [[0 for n in range(16)] for j in range(16)]

    #Вода
    while(biome_counter_on_map(arr,1) < 8):
        random_create_biome(0,1,6,arr)
    for x in range(2):
        expand_biome([0],1,relative_coords,2,(6,1),arr)
    remove_solo_biome(1,0,relative_coords,(2,1),arr)

    #Песок
    while(biome_counter_on_map(arr,2) < 12):
        random_create_biome(0,2,5,arr)
    expand_biome([0],2,relative_coords_cross,1,(9,4),arr)


    #Снег
    spawn_biome_with_condition(0,3,[2],[0],arr,relative_coords,(12,1))
    expand_biome([0],3,relative_coords_cross,1,(11,5),arr)

    ###
    ###Приближение x2 - 128x128
    ###
    arr = zoom(arr)

    #Если кол-во снега не в диапазоне 130-200, то добавляем еще
    if not(130 <= biome_counter_on_map(arr,3) <= 200):
        spawn_biome_with_condition(0, 3, [2],[0], arr, double_square_relative_coords, (15, 1))
        expand_biome([0],3,double_square_relative_coords,6,(9,3),arr)
    #Спавн темного леса
    spawn_biome_with_condition(0,4,[0,4],[8],arr,relative_coords,(9,3))
    expand_biome([0],4,double_square_relative_coords,4,(9,1),arr)
    remove_solo_biome(4,0,relative_coords,(2,1),arr)

    #Спавн джунглей
    spawn_biome_with_condition(0,5,[0,4,5],[8],arr,relative_coords,(9,2))
    expand_biome([0],5,relative_coords,2,(9,3),arr)
    remove_solo_biome(5,0,relative_coords,(3,3),arr)

    #Спавн равнин
    spawn_biome_with_condition(0,11,[0,4,11],[8],arr,relative_coords,(9,3))
    expand_biome([0],11,relative_coords,1,(9,5),arr)
    remove_solo_biome(11,0,relative_coords,(3,1),arr)


    ###
    #Приближение x4 - 64x64
    ###
    arr = zoom(arr)
    #Спавн холодного и теплого океана ОКОЛО пустынь и зимы
    spawn_biome_with_condition(1,8,[2],[1,2,3,4,5,6,7,8],arr,relative_coords,(1,2))
    spawn_biome_with_condition(1,9,[3],[1,2,3,4,5,6,7,8],arr,relative_coords,(1,2))
    #Спавн снежных гор
    spawn_biome_with_condition(3,10,[0,3,9],[8],arr,relative_coords,(8,1))
    expand_biome([3],10,relative_coords,2,(1,1),arr)
    #Удаление одиночных гор - замена на снег
    remove_solo_biome(10,6,relative_coords,(2,2),arr)

    ###
    #Приближение x8 - 32x32
    ###
    arr = zoom(arr)
    #на стыке зимы и пустыни на 2 пикселя появляется тайга
    replace(arr,[3],[2],6,double_square_relative_coords)
    #Тайга с соседствующей пустыней заменяется на лес
    replace(arr,[6],[2],0,relative_coords)
    expand_biome([3],6,double_square_relative_coords,2,(3,1),arr)

    #спавним саванну, рядом с тайгой и просто отдельно
    replace(arr,[2],[6],7,double_square_relative_coords)
    spawn_biome_with_condition(2,7,[0,1,8,9,11],[5,6,7,8],arr,relative_coords,(7,1))
    #Расширяем саванну
    expand_biome([2],7,double_square_relative_coords,2,(4,1),arr)
    expand_biome([2],7,relative_coords,1,(1,1),arr)

    #Если снега мало - добавляем
    for x in range(10):
        if biome_counter_on_map(arr,3) > 2300:
            break
        expand_biome([0],3,relative_coords_cross,1,(11,5),arr)
    #Если мало тайги - добавляем
    #   если снега меньше чем определенное кол-во, то forest меняет на тайгу, иначе snow на тайгу
    for x in range(2):
        if biome_counter_on_map(arr,6) > 180:
            break
        if biome_counter_on_map(arr,3) < 2700:
            spawn_biome_with_condition(0,6,[3],[4,5,6],arr,relative_coords,(3,1))
        else:
            spawn_biome_with_condition(3, 6, [0], [5,6,7], arr, relative_coords, (3, 1))
        expand_biome([3],6,relative_coords_cross,2,(3,4),arr)

    #Внутри океана спавним теплый или холодный, какой из них будет спавниться первым (то есть преобладать на карте) - рандом
    if randint(0,1) == 0:
        spawn_biome_with_condition(1,8,[1,8],[22,23,24,25],arr,double_square_relative_coords,(6,1))
        expand_biome([1],8,relative_coords_cross,2,(3,1),arr)
        spawn_biome_with_condition(1, 9, [1, 9], [22,23,24,25], arr, double_square_relative_coords, (6, 1))
        expand_biome([1],9,relative_coords_cross,2,(3,1),arr)
    else:
        spawn_biome_with_condition(1, 9, [1, 9], [22, 23, 24, 25], arr, double_square_relative_coords, (6, 1))
        expand_biome([1], 9, relative_coords_cross, 2, (3, 1), arr)
        spawn_biome_with_condition(1, 8, [1, 8], [22, 23, 24, 25], arr, double_square_relative_coords, (6, 1))
        expand_biome([1], 8, relative_coords_cross, 2, (3, 1), arr)
    remove_solo_biome(8,0,relative_coords,(3,3),arr)
    remove_solo_biome(9,0,relative_coords,(3,3),arr)

    #Болото, если рядом есть океан
    spawn_biome_with_condition(0,12,[1,8,9],[1,2,3,4],arr,relative_coords_cross,(4,2))
    expand_biome([0],12,relative_coords,2,(9,4),arr)
    remove_solo_biome(12,0,relative_coords,(0,1),arr)

    #Badlands
    spawn_biome_with_condition(2,13,[2,7,13],[47,48],arr,triple_square_relative_coords,(9,8))
    expand_biome([2],13,relative_coords_cross,2,(9,6),arr)
    remove_solo_biome(13,2,relative_coords,(0,1),arr)

    #cherry_grove
    for x in range(10):
        if biome_counter_on_map(arr,14) > 7:
            break
        spawn_biome_with_condition(11,14,[11],[23,24],arr,double_square_relative_coords,(4,1))
    expand_biome([11],14,relative_coords,2,(9,7),arr)

    ###
    #Приближение x16 - 16x16
    ###
    arr = zoom(arr)
    #Расширяем тайгу
    expand_biome([3],6,double_square_relative_coords,4,(1,1),arr)
    expand_biome([3],6,relative_coords_cross,3,(1,2),arr)
    #Расширяем саванну
    expand_biome([2],7,relative_coords_cross,2,(2,2),arr)

    #В зависимости от того, какого океана больше - расширяем меньший
    if biome_counter_on_map(arr,8) < biome_counter_on_map(arr,9):
        spawn_biome_with_condition(9,0,[8],[1,2,3,4,5,6,7,8],arr,relative_coords,(1,2))
    else:
        spawn_biome_with_condition(8, 0, [9], [1, 2, 3, 4, 5, 6, 7, 8], arr, relative_coords, (1, 2))

    #Удаление шума (пока не понятно надо или нет)
    # arr = fill_biomes(arr)

    #Удаление снега рядом с не теми биомами
    replace(arr,[3],[2,5,7,8,13,14],6,triple_square_relative_coords)

    #mushroom
    spawn_biome_with_condition(1,15,[1,8,9,15],[24,25],arr,double_square_relative_coords,(99,2))
    expand_biome([1,8,9],15,relative_coords,1,(9,3),arr)

    ###
    #Приближение x32 - 8x8
    ###
    arr = zoom(arr,replace_chance=15)
    #До появления реки
    # latest_arr = arr.copy()
    latest_arr = [x.copy() for x in arr]

    ban_biomes = list(range(0,16))
    #13 и 14 это биомы, находящиеся внутри выбранных, но там не нужны реки
    for x in [4,11,2,7,13,14]: ban_biomes.remove(x)
    replace_to_river(arr,[4,11,2,7],ban_biomes,relative_coords_cross)
    #Удаляем реки, рядом с которыми нет нужных биомов
    arr = remove_selected_biome(arr,latest_arr,16,[4,11,2,7],relative_coords_cross)

    #Если джунгли рядом с зимой или тайгой, то заменить на лес
    replace(arr,[5],[3,6],0,relative_coords)

    ###
    #Приближение x64 - 4x4
    ###
    # arr = zoom(arr)
    # #Расширение рек
    # expand_biome([4,11,2,7],16,relative_coords_cross,2,(2,2),arr)
    # remove_solo_biome(16,relative_coords_cross,(0,1),arr)
    #
    #До изменения рек
    # latest_arr = [x.copy() for x in arr]
    #Удаление рек рядом с океаном
    spawn_biome_with_condition(16,1,[1],list(range(2,5)),arr,relative_coords,(0,1))
    spawn_biome_with_condition(16,8,[8],list(range(2,5)),arr,relative_coords,(0,1))
    spawn_biome_with_condition(16,9,[9],list(range(2,5)),arr,relative_coords,(0,1))

    #Удаление одиночного блока реки
    arr = replace_biome_if_count(arr,latest_arr,16,[16],relative_coords,[0,1])
    # replace(arr,[16],[1,8,9],1,double_square_relative_coords)
    # remove_solo_biome(16,relative_coords_cross,(0,1),arr)

    #Спавн холодного и теплого океана ОКОЛО пустынь и зимы
    # replace(arr,[1],[2],8,double_square_relative_coords)
    # replace(arr,[1],[3],9,double_square_relative_coords)

    ###
    #Приближение до x256 - 1x1 (ПОКА ОПЦИОНАЛЬНО)
    ###
    # arr = zoom(arr)
    # arr = zoom(arr)
    return arr

