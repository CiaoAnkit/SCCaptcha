import random
import uuid
import math
import socket
import json
import time

from flask import Flask, render_template, session, request, jsonify, redirect , url_for
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
app = Flask(__name__,static_folder='static',static_url_path='',template_folder='templates')
app.secret_key = '9fa39a52b44aaa7c7441435082af29d7c379ced38e72ae3535265bfda870fbd3'#
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
file_path = "./path_dump.json"
# dump_flag = True if input("Do you want to dump the paths? (y/n): ") == 'y' else False
dump_flag = True # for now

user_data = {}

def generate_captcha_string(user_id):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    captcha_string = ''.join(random.choice(characters) for _ in range(6))
    image = ImageCaptcha()
    data = image.generate(captcha_string)
    image.write(captcha_string, f'recaptcha_main/static/pics/temp/{user_id}.png')
    return captcha_string


def generate_audio_captcha(user_id):
    audio = AudioCaptcha()
    characters = '0123456789'
    captcha_text = ''.join(random.choice(characters) for _ in range(6))
    audio_data = audio.generate(captcha_text)
    audio_file = f"{user_id}.wav"
    audio.write(captcha_text, f'recaptcha_main/static/pics/temp/{audio_file}')  
    return captcha_text

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



def check_for_jumps(prevpoint, path):
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
            dist_trav = 0
            counter+=1
        else:
            dist_trav = test_dist(prevpoint,path[i], path)
        if dist_trav > THRESHOLD:
            print("Distance too long", dist_trav)
            return counter, 0
        prevpoint = path[i]
    return counter, 1


def verify_path(path,user_id, GC_HEIGHT, GC_WIDTH):
    '''
    Verify if the path is valid
    '''
    obs = user_data[user_id]['obs']
    captcha_box = user_data[user_id]['captcha_box'][user_data[user_id]['ans']]
    pathlen = len(path)
    MIN_POINTS = get_min_points(GC_WIDTH, GC_HEIGHT, captcha_box)
    if pathlen <= MIN_POINTS:
        message = "Path too short"
        return False, message
    prevpoint = path[1]
    counter, obs_check = check_for_jumps(prevpoint, path)
    if ball_obs_overlap(path,user_id):
        message = "Ball passed through obstacle"
        return 0, message
    if not inbox(path[-1],captcha_box):
        print("Not in box", path[-1], captcha_box)
        message = "Not in box"
        return 0, message
    if behaviour(path):
        message = "Robot like behaviour"
        return 2, message
    if counter > len(path)/3:
        message = "Too many null values"
        return 0, message
    if not obs_check:
        message = "Too many jumps in path"
        return 0, message
    
    
    return 1, "Valid path"






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

@app.route('/fallback', methods = ['GET'])
def fall_back():
    delete_img()
    num = random.randint(0,1)
    if num == 1:
        return redirect("/audio_captcha")
    # elif num == 1:
    #     return redirect("/image_captcha")
    else:
        return redirect("/text_captcha")

# Route for the custom captcha example
@app.route('/text_captcha', methods=['GET', 'POST'])
def text_captcha():
    user_id = uuid.uuid1().int
    if request.method == 'POST':
        user_input = request.form['captcha_input']
        captcha_text = request.form['captcha_text']
        user_id = user_id
        print(user_input, captcha_text)
        if user_input == captcha_text:
            return "Captcha passed!"
        else:
            return "Captcha failed!"
    else:
        captcha_text = generate_captcha_string(user_id)
        return render_template('text_captcha.html', captcha_text=captcha_text, user_id = user_id)

@app.route('/image_captcha', methods = ['GET','POST'])
def image_captcha():
    user_id = uuid.uuid1().int

    pass

@app.route('/audio_captcha', methods = ['GET', 'POST'])
def audio_captcha():
    user_id = uuid.uuid1().int
    if request.method == 'POST':
        user_input = request.form['captcha_input']
        captcha_text = request.form['captcha_text']
        user_id = user_id
        print(user_input, captcha_text)
        if user_input == captcha_text:
            return "Captcha passed!"
        else:
            return "Captcha failed!"
    else:
        captcha_text = generate_audio_captcha(user_id)
        return render_template('audio_captcha.html', captcha_text = captcha_text, user_id = user_id )


    

@app.route('/puzzle', methods=['POST', 'GET'])
def start():
    '''
    Register the user, give an id
    Pick a random image, rotate it arbitarily and send to frontend.
    Generate the image box_positions, at random locations.
    Generate obstacles (obs) between image box and origin
    '''
    
    GC_HEIGHT = int(request.args['gc_height']) if 'gc_height' in request.args else 700
    GC_WIDTH = int(request.args['gc_width']) if 'gc_width' in request.args else 380
    user_id = int(request.args['user_id']) if 'user_id' in request.args else 400
    img_id = int(request.args['img_id']) if 'img_id' in request.args else 0

    print(GC_HEIGHT, GC_WIDTH)

    delete_img()
    user_data[user_id] = {}
    user_data[user_id]['start_time'] = timer()  
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
    gc_height = user_data.get(user_id).get('gc_height')
    gc_width = user_data.get(user_id).get('gc_width')
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
        val, message = verify_path(path,user_id, gc_height, gc_width)
        print(message)
        user_data[user_id]['end_time'] = timer()
        time_taken = user_data[user_id]['end_time'] - user_data[user_id]['start_time']
        print(Fore.BLUE,"Time taken is ", time_taken)

        if val==1:
            response = {
                'bool': 'true',
                'ans': ans               
            }
            dump_data("True", path, file_path, dump_flag, time_taken)

        elif val == 2:
            response = {
                'bool' : 'false',
                'ans' : 8,
                'message': "Unusual behaviour, please try again"
            }
            dump_data("Robot", path, file_path, dump_flag, time_taken)
        else:
            response = {
                    'bool': 'false',
                    'ans': ans
            }
    else:
        user_data[user_id]['end_time'] = timer()
        time_taken = user_data[user_id]['end_time'] - user_data[user_id]['start_time']
        print(Fore.BLUE,"Time taken is ", time_taken)

        if result:
            print("Reached wrong desination")
            response = {
                'bool': 'true',
                'ans': 6,
            }
            dump_data("False", path, file_path, dump_flag, time_taken)
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
    # serve(app, host='0.0.0.0', port=5000)

