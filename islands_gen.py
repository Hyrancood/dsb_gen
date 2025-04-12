from islands_functions import *
from PIL import Image,ImageDraw
from random import randint
import numpy as np
from opensimplex import OpenSimplex


def generate_heightmap(size, scale, seed):
    noise = OpenSimplex(seed)
    heightmap = np.zeros((size, size))
    h, l = 0, 0
    for x in range(size):
        for y in range(size):
            nx, ny = x / scale, y / scale
            heightmap[x, y] = noise.noise2(nx, ny)
            if heightmap[x, y] > 0.8:
                h += 1
            if heightmap[x, y] < -0.8:
                l += 1
    print(f"h: {h}, l: {l}")
    return heightmap


def draw_heightmap(img, heightmap, img_size=4096):
    for x in range(img_size):
        for y in range(img_size):
            color = int((1+heightmap[x//16, y//16])*48)
            img.point((x, y), fill=(color, color, color))
    pass

#Составить список с координатами островов

for count in range(7):
    heightmap = generate_heightmap(256, 35, 237*7-count*13) #TODO: возможно стоит сменить способ генерации сида
    #Для рисовки островов визуально
    arr = [[0 for __ in range(4096)] for _ in range(4096)]

    x_center = 0
    y_center = 0

    new_img = Image.new("RGBA", (len(arr), len(arr)), "black")
    img = ImageDraw.Draw(new_img)
    draw_heightmap(img, heightmap)
    #Список с координатами островов
    output_arr = []
    #Файл для сохранения
    file_list = open(f'output/{count}.mcfunction', 'w', encoding='utf-8')
    while (len(output_arr) <= 350):
        output_arr = []
        #new_img = Image.new("RGBA", (len(arr), len(arr)), "black")
        img = ImageDraw.Draw(new_img)
        rad = 0
        for x in range(16): #кол-во колец
            #шаг угла
            alf = randint(-20, 35)

            if x<2: #каждую группу колец меняются значения
                alf_step = (80 - x*20, 120 - x*15)
                spread = (-13 - int(5*x**2.5), 13 + int(5*x**2.5)) #Разброс расположения островов на кольце (чтобы не четко на окружности)
                rad += randint(55,70) + randint(x*3, max(int(x**2.5), x*3 + 3)) #радиус от центра
            elif x<6:
                alf_step = (max(45 - int(x**2.5), 12), 70 - x*2)
                spread = (-15 - x**2, 15 + x**2)
                rad += randint(65, 70) + randint(x * 3, max(int(x ** 2), x * 5 + 3))
            else:
                alf = randint(-10, 40)
                alf_step = (30 - x*2, max(60 - int(x*4), 9))
                spread = (-40 - x*4, 40 + x*4)
                rad += randint(80, 90) + randint(x * 4, max(int(x ** 2.2), x * 5 + 3))
            #Рисует кольцо с заданным параметрами
            create_circle(arr,(x_center,y_center),rad,alf,alf_step,spread, heightmap, img,output_arr)
    #После отрисовки всех колец задаем им размер
    give_size(output_arr,img)
    #Добавление разных высот
    #add_diffenent_heights(output_arr)

    print(len(output_arr), "всего", end=" ")
    print([x[1] in range(150,300) for x in output_arr].count(True), "высоких", end=" ")
    print([x[1] in range(-60, 20) for x in output_arr].count(True), "низких")



    new_img.show('test_island.png')
    # list.write(f"{output_arr}")
    # list.close()
    new_img.save(f'output/{count}.png', dpi=(3, 3))
    file_list.write(f"data modify storage dsb_gen:gen Islands set value {output_arr}")
    file_list.close()
    print(count)
    # print('кол-во островов', len(output_arr))
