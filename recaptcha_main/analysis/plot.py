from matplotlib import pyplot as plt
import numpy as np
import json

#read json file random_json.json and store it in data
with open('../data/random_json.json') as f:
    data = json.load(f)

#extract box and obs positions from data
#append all box positions to box positions except fo ans psoition
box_pos = []
obs_pos = []
ans_pos = []
num = 0
for obj in data:
    if num == 1000:
        break
    num += 1
    for i in range(4):
        if i == obj['ans']:
            ans_pos.append(obj['box'][i])
        else:
            box_pos.append(obj['box'][i])
            
    for i in range(4):
        obs_pos.append(obj['obs'][i])

#plot box, ans and obs positions, label outside the coordinates
box_pos = np.array(box_pos)
obs_pos = np.array(obs_pos)
ans_pos = np.array(ans_pos)
plt.rcParams.update({'font.size': 18})

plt.scatter(box_pos[:,0], box_pos[:,1], c='r', label='Objects that\nare not answers', marker= '^')
plt.scatter(obs_pos[:,0], obs_pos[:,1], c='b', label='Obstacles', marker= 'x')
plt.scatter(ans_pos[:,0], ans_pos[:,1], c='g', label='Objects that\nare answers', marker= '.')
#increase font size of axis numbers and labels
plt.legend(loc='center', bbox_to_anchor=(1.5, 0.5), fancybox=True,ncol=1, markerscale=2.5)

plt.show()

    