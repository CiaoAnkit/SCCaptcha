import random
import uuid
import math
import os
import time

from PIL import Image
from flask import Flask, render_template, session, request, jsonify, redirect , url_for
from matplotlib import pyplot as plt
from PIL import Image
from itertools import product
from colorama import Fore, Back, Style


MAX_SPEED = 5
SQUARE_SIZE = 40 
THRESHOLD = 75
offset = 40
offset2 = 80
app = Flask(__name__,static_folder='static',static_url_path='')
app.secret_key = 'secretkey'

user_data = {}

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
    


def render_img(img_id, box_pos, ans, user_id, gcwidth, gcheight):

    img1 = Image.open(f"./static/pics/{img_id}.png")
    newsize = (50,50)
    img1 = img1.resize(newsize)
    image1copy = img1.copy()
    img2 = Image.new('RGBA', (gcwidth, gcheight), (255, 0, 0, 0))
    image2copy = img2.copy()
    angle = 90
    for i in range(len(box_pos)):
        pos = (box_pos[i][0],box_pos[i][1])
        if ans == i:
            image2copy.paste(image1copy, pos)
        else:
            image2copy.paste(image1copy.rotate(angle), pos)
            angle+=90


    image2copy.save(f"./static/pics/temp/{user_id}.png")
    return image2copy

def check_endpoint(final_point, boundary):
    x,y = final_point
    if x is not None and y is not None:
        for i in range(4):
            if x < boundary[i]['right'] and x > boundary[i]['left'] and y < boundary[i]['bottom'] and y > boundary[i]['top']:
                print(i, "is the guess")
                return True, i
    return False, 5

def test_dist(a,b,path):
    if a[0] is None or b[0] is None or a[1] is None or b[1] is None:
        print(path)   
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) #has a problem TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) #has a problem TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'

def inbox(point,corner ,size=SQUARE_SIZE):
    for i in range(0,2):
        # print(point[i], corner[i]-size, corner[i] + size)
        if not (point[i] > corner[i]-size and point[i] < corner[i] + size):
            return False
    return True


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
    counter = 0  #to check how many points in path are None
    for i in range(2,pathlen):
        # print("path[i]",path[i])
        # for corner in obs:
        #     if inbox(path[i],corner):
        #         print("Hit obstacle", path[i], corner)
        #         return 3
        if None in prevpoint or None in path[i]:
            dist_trav = 0
            counter+=1
        else:
            dist_trav = test_dist(prevpoint,path[i], path)
        if dist_trav > THRESHOLD:
            print("Distance too long", dist_trav)
            return 0
        prevpoint = path[i]
    if not inbox(path[-1],captcha_box):
        print("Not in box", path[-1], captcha_box)
        return 0
    if counter > len(path)/3:
        return 0
    return 1

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

@app.route('/', methods = ['GET'])
def main():
    return redirect('home')

@app.route('/home', methods = ['GET'])
def landing_page():
    user_id = uuid.uuid1().int
    return render_template('index.html', user_id = user_id)

@app.route('/puzzle', methods=['POST', 'GET'])
def start():
    '''
    Register the user, give an id
    Pick a random image, rotate it arbitarily and send to frontend.
    Generate the image box_positions, at random locations.
    Generate obstacles (obs) between image box and origin
    '''
    
    GC_HEIGHT = int(request.args['gc_height']) if 'gc_height' in request.args else 700
    GC_HEIGHT -=10
    GC_WIDTH = int(request.args['gc_width']) if 'gc_width' in request.args else 380
    user_id = int(request.args['user_id']) if 'user_id' in request.args else 400

    print(GC_HEIGHT, GC_WIDTH)

    delete_img()
    user_data[user_id] = {}
    img_id = random.randint(0, 1)
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
    obstacle_ball_offset = 85  
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

    render_img(img_id, box_pos, ans, user_id, GC_WIDTH, GC_HEIGHT)
    print("user_id being send is", user_id)
    return render_template('puzzle.html', user_id =user_id, offset=offset, offset2=offset2, gcheight = GC_HEIGHT, gcwidth=GC_WIDTH, box_pos=box_pos,obs_pos=obs_pos)


@app.route('/coordinates', methods=['POST'])
def coordinates():
    data = request.json
    GC_WIDTH = data.get('gc_width')
    GC_HEIGHT = data.get('gc_height')
    user_id = int(data.get('user_id'))
    return redirect(f'/puzzle?gc_width={GC_WIDTH}&gc_height={GC_HEIGHT}&user_id={user_id}')


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
        else :
            response = {
                'bool': 'false',
                'ans': ans
            }
    return jsonify(response)

if __name__ == '__main__':
    delete_img()
    app.run(host="0.0.0.0",debug=True,ssl_context=("ssl.cert", "ssl.key"))


