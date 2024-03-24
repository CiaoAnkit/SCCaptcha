import json
import numpy as np
'''
We add user_ids and unique_ids to the data
'''
def get_approx_ball_speed(data):
    '''
    get the approximate speed of the ball for every person, that time is recorded
    '''
    ball_speed = []
    for obj in data:
        if obj.get('time') != None and obj.get('path') != None:
            ball_speed.append(len(obj['path'])/obj['time'])
    ball_speed = np.array(ball_speed)
    return np.mean(ball_speed)

def add_unique_ids(data):
    ball_speed = get_approx_ball_speed(data)
    with open('../data/path_ids.json', 'a') as f1:
        l = 0
        for obj in data:
            l+=1
            if obj.get('time'):
                time = obj['time']
            else:
                time = len(obj['path'])/ball_speed
            #write obj to another file, and add two extra keys inside the dictionary
            f1.write(json.dumps({'status': obj['status'], 'id': "", 'uid':l, 'path': obj['path'], 'time': time}) + ','+'\n')

# with open('../data/path_dump.json', "r") as f:
#     data = json.load(f)
# add_unique_ids(data)

#open status_id and path_id and fill in user_ids in the file

def fill_data(data, id_data):
    # if both data status and unique_id matches then fill user_id else show a pop up
    for x in data:
        for y in id_data:
            if x['uid']== y['uid'] and x['status'] == y['status'] and x['id'] == '':
                x['id'] = y['id']
    for x in data:
        if x['id'] == '':
            print(x['uid'])
    with open ("../data/path_data_final.json", "w") as f2:
            f2.write(json.dumps(data))

# with open('../data/path_ids.json', "r") as f:
#     data = json.load(f)

# with open('status_id.json', "r") as f1:
#     id_data = json.load(f1)

# fill_data(data, id_data)

