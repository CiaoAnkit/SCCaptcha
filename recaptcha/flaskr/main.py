import random
import uuid
import math
import socket
import json

from flask import Flask, render_template, session, request, jsonify, redirect , url_for
from colorama import Fore, Back, Style
from random import choice, randint

from image_handler import delete_img, render_img, get_img_name
from helper import test_dist, dist
from coordinate_handler import check_endpoint, inbox, get_area, get_box_coordinates
from path_behaviour import behaviour


MAX_SPEED = 5
SQUARE_SIZE = 40 
THRESHOLD = 75
offset = 40
offset2 = 80
img_first = 0
img_last = 1
app = Flask(__name__,static_folder='static',static_url_path='')
app.secret_key = 'secretkey'#
file_path = "./path_dump.json"
# dump_flag = True if input("Do you want to dump the paths? (y/n): ") == 'y' else False
dump_flag = True # for now

user_data = {}

def check_for_obstacle(prevpoint, path):
    pathlen = len(path)
    counter = 0
    for i in range(2,pathlen):
        '''
        This is code for if obstacle is hit then return false
        print("path[i]",path[i])
        for corner in obs:
            if inbox(path[i],corner):
                print("Hit obstacle", path[i], corner)
                return 3
        '''
        if None in prevpoint or None in path[i]:
            #remove point from path
            path.pop(i)
            dist_trav = 0
            counter+=1
        else:
            dist_trav = test_dist(prevpoint,path[i], path)
        if dist_trav > THRESHOLD:
            print("Distance too long", dist_trav)
            return counter, 0
        prevpoint = path[i]
    return counter, 1

def verify_path(path,user_id):
    '''
    Verify if the path is valid
    '''
    obs = user_data[user_id]['obs']
    captcha_box = user_data[user_id]['captcha_box'][user_data[user_id]['ans']]
    pathlen = len(path)
    if pathlen <= 2:
        print("Path too short")
        return False
    prevpoint = path[1]
    
    counter, obs_check = check_for_obstacle(prevpoint, path)

    if not inbox(path[-1],captcha_box):
        print("Not in box", path[-1], captcha_box)
        return 0
    if counter > len(path)/3:
        print("Too many null values")
        return 0
    if not obs_check:
        return 0
    if behaviour(path):
        return 0
    
    return 1






@app.route('/', methods = ['GET'])
def main():
    return redirect('home')

@app.route('/home', methods = ['GET'])
def landing_page():
    user_id = uuid.uuid1().int
    img_id = random.randint(img_first,img_last)
    img_name = get_img_name(img_id)
    print(img_name)
    return render_template('index.html', user_id = user_id, img_id=img_id, img_name=img_name)

@app.route('/puzzle', methods=['POST', 'GET'])
def start():
    '''
    Register the user, give an id
    Pick a random image, rotate it arbitarily and send to frontend.
    Generate the image box_positions, at random locations.
    Generate obstacles (obs) between image box and origin
    '''
    
    GC_HEIGHT = int(request.args['gc_height']) if 'gc_height' in request.args else 700
    GC_HEIGHT -= 25
    GC_WIDTH = int(request.args['gc_width']) if 'gc_width' in request.args else 380
    user_id = int(request.args['user_id']) if 'user_id' in request.args else 400
    img_id = int(request.args['img_id']) if 'img_id' in request.args else 0

    print(GC_HEIGHT, GC_WIDTH)

    delete_img()
    user_data[user_id] = {}
  
    rotate_90_by = random.randint(0,3)
    session['user_id'] = user_id
    # number = random.randint(1, 10)
    ans = (4-rotate_90_by)%4 
    # ans = rotate_90_by
    user_data[user_id]['ans'] = ans
    user_data[user_id]['rotate'] = rotate_90_by
    box_pos = []
    obs_pos = []
    area_box = []
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
            
        
        box_pos.append((box_x,box_y))
        obs_pos.append((obs_x,obs_y))
        area_box.append(get_area(box_x, box_y,img_id))

    user_data[user_id]['obs'] = obs_pos
    user_data[user_id]['captcha_box'] = box_pos 
    user_data[user_id]['boundary'] = area_box

    render_img(img_id, box_pos, ans, user_id, GC_WIDTH, GC_HEIGHT, img_first, img_last)
    print("user_id being send is", user_id)
    return render_template('puzzle.html', user_id =user_id, offset=offset, offset2=offset2, gcheight = GC_HEIGHT, gcwidth=GC_WIDTH, box_pos=box_pos,obs_pos=obs_pos)


@app.route('/coordinates', methods=['POST'])
def coordinates():
    data = request.json
    GC_WIDTH = data.get('gc_width')
    GC_HEIGHT = data.get('gc_height')
    user_id = int(data.get('user_id'))
    img_id = int(data.get('img_id'))
    return redirect(f'/puzzle?img_id={img_id}&gc_width={GC_WIDTH}&gc_height={GC_HEIGHT}&user_id={user_id}')


@app.route('/guess', methods=['POST'])
def guess():
    user_id = session.get('user_id')
    ans = user_data.get(user_id).get('ans')
    path = request.json['path'][1:]
    
    # check if the end point is in which cat, 5 means no end point
    if len(path) > 2:
        end_point = path[-1]
        if end_point[0] is not None :
            result, guess = check_endpoint(end_point, user_data[user_id]['boundary'])
            print("guess and result : ", guess,result )
        else :
            result, guess = False, 5
    else :
        result = False
        guess = 5

    if ans is None:
        response = {
            'message': 'Please start a new game before guessing.',
        }
    elif guess == ans and result:
        # print("path is ", path)
        if verify_path(path,user_id)==1:
            response = {
                'bool': 'true',
                'ans': ans
                
            }
            if dump_flag:
                data_to_append = {"status": True, "path": path}
                with open(file_path, 'a') as file:
                    json.dump(data_to_append, file)
                    file.write(',\n')
        else:
            response = {
                    'bool': 'false',
                    'ans': ans
            }
    else:
        # print(result)
        if result:
            print("reached wrong destination")
            response = {
                'bool': 'true',
                'ans': 6
            }
            if dump_flag:
                data_to_append = {"status": False, "path": path}
                with open(file_path, 'a') as file:
                    json.dump(data_to_append, file)
                    file.write(',\n')
        else :
            response = {
                'bool': 'false',
                'ans': ans
            }
    return jsonify(response)

if __name__ == '__main__':
    delete_img()
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    app.run(host="0.0.0.0",debug=True,ssl_context=("ssl.cert", "ssl.key"))


