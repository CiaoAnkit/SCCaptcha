import os
import time
from PIL import Image, ImageFilter
from itertools import product
from random import choice, randint


def delete_img():
    '''
    deletes all the files dates more than 2 minutes ago every time process starts
    '''
    now = time.time()
    folder = './static/pics/temp'

    files = [os.path.join(folder, filename) for filename in os.listdir(folder)]
    for filename in files:
        if (now - os.stat(filename).st_mtime) > 120:  # 2minutes
            os.remove(filename)
    return True

def render_img(img_id, box_pos, ans, user_id, gcwidth, gcheight, img_first, img_last):

    newsize = (50, 50)
    img2 = Image.new('RGBA', (gcwidth, gcheight), (255, 255, 255, 255))
    image2copy = img2.copy()
    # img3 = Image.open(f"./static/pics/noise1.png").convert('RGBA')
    # img3 = img3.resize(newsize)
    # img3copy = img3.copy()
    # #make it a more transparent
    # img3copy.putalpha(150)  
    # dumm3 = img3copy.copy()
    # dumm3.putalpha(150)

    angles = [0]
    name = 12
    for i in range(len(box_pos)):
        img_num = randint(img_first,img_last)
        angle_noise = randint(10,360)
        pos = (box_pos[i][0],box_pos[i][1])
        name+=1

        if ans == i:
            angle_animal = 1
            img1 = Image.open(f"./static/pics/images/{img_id}.png").convert('RGBA')
            img1 = img1.resize(newsize)
            image1copy = img1.copy()
            rot = image1copy.rotate(1)
            fff = Image.new('RGBA', rot.size, (255,)*4)
            out = Image.composite(rot, fff, rot)
            image2copy.paste(out, pos)
            # image2copy.paste(img3copy.rotate(angle_noise), pos, img3copy)
            # out.save(f"./static/pics/test/{name}.png")

        else:
            img1 = Image.open(f"./static/pics/images/{img_num}.png").convert('RGBA')
            img1 = img1.resize(newsize)
            image1copy = img1.copy()
            angle_animal = choice([i for i in range(10,360) if i not in angles])
            rot = image1copy.rotate(angle_animal)
            fff = Image.new('RGBA', rot.size, (255,)*4)
            out = Image.composite(rot, fff, rot)
            image2copy.paste(out, pos)
            # image2copy.paste(img3copy.rotate(angle_noise), pos, img3copy)
            angles.append(angle_animal)
            # out.save(f"./static/pics/test/{name}.png")

            


    image2copy.save(f"./static/pics/temp/{user_id}.png")
    return image2copy

def get_img_name(img_id):
    #cifar100 dataset
    if img_id == 0:
        return "mouse"
    elif img_id == 1:
        return "cat"
    elif img_id == 2:
        return "dinosaur"
    elif img_id == 3 or img_id == 4:
        return "camel"
    elif img_id == 5:
        return "butterfly"
    elif img_id == 6 or img_id == 7:
        return "elephant"
    elif img_id == 8:
        return "leopard"
    elif img_id == 9:
        return "bear"
    elif img_id == 10 or img_id == 11:
        return "rabbit"
    elif img_id == 12:
        return "turtle"
    elif img_id == 13 or img_id == 14:
        return "cockroach"
    # animal 10 dataset
    elif img_id == 15:
        return "elephant"
    elif img_id == 16:
        return "flamingo"
    elif img_id == 17 or img_id == 20:
        return "camel"
    elif img_id == 18:
        return "cat"
    elif img_id == 19:
        return "tiger"
    elif img_id == 21 or img_id == 22:
        return "horse"

    else :
        return "error"