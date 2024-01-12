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

    newsize = (50,50)
    img2 = Image.new('RGBA', (gcwidth, gcheight), (255, 0, 0, 0))
    image2copy = img2.copy()
    img3 = Image.open(f"./static/pics/noise1.png").convert('RGBA')
    img3 = img3.resize(newsize)
    img3copy = img3.copy()
    #make it a more transparent
    img3copy.putalpha(150)  
    angles = [0]

    for i in range(len(box_pos)):
        img_num = randint(img_first,img_last)
        angle_noise = randint(10,360)
        pos = (box_pos[i][0],box_pos[i][1])
        if ans == i:
            img1 = Image.open(f"./static/pics/{img_id}.png").convert('RGBA')
            img1 = img1.resize(newsize)
            image1copy = img1.copy()
            image2copy.paste(image1copy.rotate(1), pos, image1copy)
            image2copy.paste(img3copy.rotate(angle_noise), pos, img3copy)

        else:
            img1 = Image.open(f"./static/pics/{img_num}.png").convert('RGBA')
            img1 = img1.resize(newsize)
            image1copy = img1.copy()
            angle_animal = choice([i for i in range(10,360) if i not in angles])
            image2copy.paste(image1copy.rotate(angle_animal), pos, image1copy)
            image2copy.paste(img3copy.rotate(angle_noise), pos, img3copy)
            angles.append(angle_animal)
            


    image2copy.save(f"./static/pics/temp/{user_id}.png")
    return image2copy

def get_img_name(img_id):
    if img_id == 0:
        return "mouse"
    else:
        return "cat"