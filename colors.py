dic = {0: "green", #forest
       1: "blue", #ocean
       2: (255,255,0), #desert - yellow
       3: "white", #snowy_plains
       4: (0,90,10), #dark_forest - dark_green
       5: (110,240,112), #jungle - light_green
       6: (122,165,111), #taiga gray-green
       7: (250,195,130), #savanna - light_orange
       8: (0,200,245), #warm_ocean - light_blue
       9: (7,18,160), #cold_ocean - dark_blue
       10: (148,206,204), #frozen_peaks
       11: (8,175,8), #plains
       12: (145,110,15), #swamp
       13: (255,150,0), #badlands - orange
       14: (255,0,132), #cherry_grove     
       15: (245,130,190), #mushrooms
       16: (0,0,0) #river
       }

relative_coords = [(x,y) for x in range(-1,2) for y in range(-1,2) if [x==0,y==0].count(True)!=2]
double_square_relative_coords = [(x,y) for x in range(-2,3) for y in range(-2,3) if [x==0,y==0].count(True)!=2]
triple_square_relative_coords = [(x,y) for x in range(-3,4) for y in range(-3,4) if [x==0,y==0].count(True)!=2]
relative_coords_cross = [(0,1),(0,-1),(1,0),(-1,0)]