import random
import uuid
import math
import socket
import json
import time

from colorama import Fore, Back, Style
from random import choice, randint
import requests

from recaptcha_main.image_handler import delete_img, render_img, get_img_name
from recaptcha_main.helper import test_dist, dist, dump_data, get_min_points, get_random_page
from recaptcha_main.coordinate_handler import check_endpoint, inbox, get_area, get_box_coordinates
from recaptcha_main.path_behaviour import behaviour
from timeit import default_timer as timer
from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha
from werkzeug.middleware.proxy_fix import ProxyFix

from waitress import serve



MAX_SPEED = 5
SQUARE_SIZE = 40
THRESHOLD = 130
offset = 40
offset2 = 80
img_first = 15
img_last = 22

# dump_flag = True if input("Do you want to dump the paths? (y/n): ") == 'y' else False
dump_flag = True # for now

user_data = {}


def point_inside_rectangle(point, rectangle):
    x, y = point
    x1, y1 = rectangle["left"], rectangle["top"]
    x2, y2 = rectangle["right"], rectangle["top"]
    x3, y3 = rectangle["left"], rectangle["bottom"]
    x4, y4 = rectangle["right"], rectangle["bottom"]
    
    # Check if the point is within the rectangle
    if (min(x1, x3) <= x <= max(x2, x4) and
        min(y1, y3) <= y <= max(y2, y4) and
        x >= min(x1, x3) and
        x <= max(x2, x4) and
        y >= min(y1, y3) and
        y <= max(y2, y4)):
        return True
    else:
        return False
    
def ball_obs_overlap(path, user_id):
    obs_areas = user_data[user_id]['obstacle_coords']
    for area in obs_areas:
        for point in path:
            if point[0] is not None and point[1] is not None:
                if point_inside_rectangle(point, area):
                    print(Fore.RED,"point is in area:",point, area)
                    print(Fore.WHITE,"")
                    return True
    return False



def start():
    '''
    Register the user, give an id
    Pick a random image, rotate it arbitarily and send to frontend.
    Generate the image box_positions, at random locations.
    Generate obstacles (obs) between image box and origin
    '''
    # GC_HEIGHT = int(request.args['gc_height']) if 'gc_height' in request.args else 700
    # GC_WIDTH = int(request.args['gc_width']) if 'gc_width' in request.args else 380
    # user_id = int(request.args['user_id']) if 'user_id' in request.args else 400
    # img_id = int(request.args['img_id']) if 'img_id' in request.args else 0
    GC_HEIGHT = 783
    GC_WIDTH = 412
    user_id = 1
    img_id = 1

    delete_img()
    user_data[user_id] = {}
    user_data[user_id]['start_time'] = timer()  
    rotate_90_by = random.randint(0,3)
    # number = random.randint(1, 10)
    ans = (4-rotate_90_by)%4 
    # ans = rotate_90_by
    user_data[user_id]['ans'] = ans
    user_data[user_id]['rotate'] = rotate_90_by
    box_pos = []
    obs_pos = []
    area_box = []
    get_obs_areas = []
    #distance needed between obstacle and box, 60*(2^0.5) is needed for perfect non overlap
    obstacle_ball_offset = 90
    for i, j in [(i,j) for i in [0,1] for j in [0,1]]:
        '''
        Select position from the L shape region
        '''
        sh = GC_HEIGHT//6 - offset
        sw = GC_WIDTH//6 - offset
        lh = GC_HEIGHT//2 - offset
        lw = GC_WIDTH//2 - offset
        borderw = GC_WIDTH//2 -offset -sw
        borderh = GC_HEIGHT//2 - offset -sh
        box_x, box_y = get_box_coordinates(sw,sh,lw,lh,borderw,borderh,i,j, GC_WIDTH, GC_HEIGHT)

        obs_x = GC_WIDTH//2 +  pow(-1,i+1)*random.randint( offset2, GC_WIDTH//3  - offset)
        obs_y = GC_HEIGHT//2 + pow(-1,j+1)*random.randint( offset2, GC_HEIGHT//3  - offset)

        while dist((obs_x,obs_y),(box_x,box_y)) < obstacle_ball_offset:
            print(Fore.GREEN,"Box in obstacle", obs_x, obs_y, box_x, box_y)
            print("Regenerating box coordinates")
            box_x, box_y = get_box_coordinates(sw,sh,lw,lh,borderw,borderh,i,j, GC_WIDTH, GC_HEIGHT)
            
        print(Fore.CYAN,"distance now is ",dist((obs_x,obs_y),(box_x,box_y)))
        print(Fore.WHITE)
        box_pos.append((box_x,box_y))
        obs_pos.append((obs_x,obs_y))
        area_box.append(get_area(box_x, box_y,img_id))
        get_obs_areas.append(get_area(obs_x, obs_y, img_id))

    user_data[user_id]['obs'] = obs_pos
    user_data[user_id]['captcha_box'] = box_pos 
    user_data[user_id]['boundary'] = area_box
    user_data[user_id]['obstacle_coords'] = get_obs_areas
    user_data[user_id]['gc_height'] = GC_HEIGHT
    user_data[user_id]['gc_width'] = GC_WIDTH
    #write box pos and obs pos to a file, write ans pos separately
    #write to a file
    write_data = {"ans":ans, "box": box_pos, "obs" : obs_pos}
    json.dump(write_data, f)
    print("User data written to file")
    return 0
    
    # return render_template('puzzle.html', user_id =user_id, offset=offset, offset2=offset2, gcheight = GC_HEIGHT, gcwidth=GC_WIDTH, box_pos=box_pos,obs_pos=obs_pos, img_name = img_name)
with open('../data/random_json.json', 'a') as f:
    for i in range(1000):
        start()
        f.write(',\n')
