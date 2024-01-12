import random
from random import choice, randint

SQUARE_SIZE = 40
offset = 40
offset2 = 80

def check_endpoint(final_point, boundary):
    x,y = final_point
    if x is not None and y is not None:
        for i in range(4):
            if x < boundary[i]['right'] and x > boundary[i]['left'] and y < boundary[i]['bottom'] and y > boundary[i]['top']:
                print(i, "is the guess")
                return True, i
    return False, 5

def inbox(point,corner ,size=SQUARE_SIZE):
    for i in range(0,2):
        # print(point[i], corner[i]-size, corner[i] + size)
        if not (point[i] > corner[i]-size and point[i] < corner[i] + size):
            return False
    return True

def get_area(x,y, img_id, margin = 20, squareSize = 20):
    if img_id:
        squareSize = 30
    ans = {
        'left': x - offset - margin,
        'right': x - offset + squareSize + margin,
        'top': y - offset - margin,
        'bottom': y - offset + squareSize + margin
    }
    return ans

def get_box_coordinates(sw,sh,lw,lh,borderw, borderh,i,j, GC_WIDTH, GC_HEIGHT):
    area_choice=random.choices([0,1,2],weights=[sh*sw,(lh-offset)*sw,(lw-offset)*sh])
    box_x=0
    box_y=0
    if area_choice[0]==0:
        box_x =  GC_WIDTH//2 + pow(-1,i+1)*random.randint(borderw,borderw+sw)
        box_y =  GC_HEIGHT//2 + pow(-1,j+1)*random.randint(borderh,borderh+sh)
    elif area_choice[0]==1:
        box_x = GC_WIDTH//2 + pow(-1,i+1)*random.randint(borderw,borderw+sw)
        box_y = GC_HEIGHT//2 + pow(-1,j+1)*random.randint(offset,lh)
    else:
        box_x = GC_WIDTH//2 + pow(-1,i+1)*random.randint(offset,lw)
        box_y = GC_HEIGHT//2 + pow(-1,j+1)*random.randint(borderh,borderh+sh)
    return box_x, box_y
