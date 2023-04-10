import random
import uuid
from PIL import Image
from flask import Flask, render_template, session, request, jsonify
MAX_SPEED = 5
GC_WIDTH = 370
GC_HEIGHT = 700
offset = 35
offset2 = 70
app = Flask(__name__,static_folder='static',static_url_path='')
app.secret_key = 'secretkey'

user_data = {}

@app.route('/', methods=['GET'])
def start():
    '''
    Register the user, give an id
    Pick a random image, rotate it arbitarily and send to frontend.
    Generate the image box_positions, at random locations.
    Generate obstacles between image box and origin
    '''

    user_id = uuid.uuid1().int;
    user_data[user_id] = {}
    img_id = random.randint(0, 1)
    rotate_90_by = random.randint(0,3)
    org_img = Image.open(f"./static/pics/{img_id}.png")
    rotated_img = org_img.rotate(rotate_90_by*90) 
    rotated_img.save("./static/pics/tmp.png")
    session['user_id'] = user_id
    # number = random.randint(1, 10)
    ans = (4-rotate_90_by)%4 
    user_data[user_id]['ans'] = ans
    box_pos = []
    obs_pos = []
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
        # box_x = GC_WIDTH//2 + pow(-1,i+1)*random.randint(offset,lw)
        # box_y = GC_HEIGHT - offset
        print(sw,sh,borderw+sw,borderh+sh,GC_WIDTH,GC_HEIGHT)
        print((i,j),area_choice,box_x,box_y) 
        box_pos.append((box_x,box_y))

        obs_x = GC_WIDTH//2 +  pow(-1,i+1)*random.randint( offset2, GC_WIDTH//3  - offset)
        obs_y = GC_HEIGHT//2 + pow(-1,j+1)*random.randint( offset2, GC_WIDTH//3  - offset)
        obs_pos.append((obs_x,obs_y))
        # obstacle_pos.append(( offset + random.randint(i*(GC_WIDTH//2),  (i+1)*(GC_WIDTH)),
        #                 ( offset + random.randint(j*(GC_HEIGHT//2),  (j+1)*(GC_HEIGHT))) ))
    return render_template('index.html',offset=offset,offset2=offset2,gcheight = GC_HEIGHT,gcwidth=GC_WIDTH,box_pos=box_pos,obs_pos=obs_pos)

@app.route('/guess', methods=['POST'])
def guess():
    user_id = session.get('user_id')
    guess = request.json['guess']
    ans = user_data.get(user_id).get('ans')
    if ans is None:
        response = {
            'message': 'Please start a new game before guessing.',
        }
    elif guess == ans:
        response = {
            'bool': 'true',
        }
    else:
        response = {
            'bool': 'false',
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,ssl_context=("cert.pem", "key.pem"))


