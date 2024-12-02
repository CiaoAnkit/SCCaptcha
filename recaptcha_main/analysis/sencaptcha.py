import json
import matplotlib.pyplot as plt
import math
import random
import numpy as np

'''
In this file we are going to analyse the sencaptcha passing rate. 
Scenerio 1
1. Calculate the how much distance ball has to move x coordinate 
2. Calculate the how much distance ball has to move y coordinate
3. See it has to take x or y to have shortest path

scnerio 2
1. Calculate the shortest path to reach the target given obstacles and see the deviation 
'''
def check_path(path, offset, main_x, main_y, acceptable_points):
    points= 0
    for x, y in path:
        if (main_x - offset <= y <= main_x + offset) and (main_y - offset <= x <= main_y + offset):
            points+=1
            
    if points/len(path) >= acceptable_points/100:
        return True
    return False

def scene1(paths, offset, acceptable_points):
    accuracy = 0
    for path in paths:
        x_start_value = path['path'][0][0]
        x_end_value = path['path'][-1][0]
        y_start_value = path['path'][0][1]
        y_end_value = path['path'][-1][1]
        # in a plain graph point these values
        x_values = [x_start_value, x_start_value, x_end_value]
        y_values = [y_start_value, y_end_value, y_end_value]
        path_1 = x_values, y_values   
        x2 = [x_start_value, x_end_value, x_end_value]
        y2 = [y_start_value,y_start_value, y_end_value]
        path2 = x2, y2
        # for each x, y in path['path'] see if it x falls between y_start + offset and y_start - offset and y value falls between x_end + offset and x_end - offset
        if check_path(path['path'], offset, x_end_value, y_start_value, acceptable_points):
            accuracy+=1
        elif check_path(path['path'], offset, x_start_value, y_end_value, acceptable_points):
            accuracy+=1
        # plot path1 and path['path'] is same garpgh
        # plt.plot(x_values, y_values, marker='o', linestyle='--')
        # plt.text(x_values[0], y_values[0], 'Start', fontsize=18, ha='right', va='bottom', color='red')
        # plt.text(x_values[-1], y_values[-1], 'Target', fontsize=18, ha='left', va='top', color='blue')

        # plt.plot(x2, y2, marker='o', linestyle='--')
        # # also plot the path['path']
        # x_values = [point[0] for point in path['path']]
        # y_values = [point[1] for point in path['path']]
        # plt.plot(x_values, y_values, marker='o', linestyle='-')
        # plt.xlabel("X coordinate")
        # plt.ylabel("Y coordinate")
        # # linestyle -- is expected path and - is actual path show in fancy box above table 
        # plt.legend(["Expected Path", "Expected Path", "Actual Path"], loc='upper center', bbox_to_anchor=(0.5, 1.20),
        #    fancybox=True, shadow=True, ncol=3)

        # plt.show()
    return accuracy/len(paths)


# Specify the file path
file_path = "../data/path_data.json"
# Read data from the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)
#latest plots will be displayed first

#get all paths where status is true 
paths = [path for path in data if path['status'] == ('True' or 1 )]
print("Number of paths with status True: ", len(paths))
# paths = random.sample(paths, 1)
offset = 1
accep = 100
plt.rcParams.update({'font.size': 20})
# scene1(paths, offset, accep)
# offset is applicable for both directions in both paths
# offset = int(input("Enter the offset value: "))
# print("Accuracy for offset: ", offset, " is: ", scene1(paths, offset))
markers = ['o', 'v', 'x', '+', '^']

for i, accep in enumerate(range(20,101,20)):
    accuracy = []
    for offset in range(0, 501, 50):
        accuracy.append(scene1(paths, offset, accep))
        print("Accuracy for offset: ", offset, " is: ", accuracy[-1])
    plt.plot(range(0, 501, 50), accuracy, marker=markers[i % len(markers)], label=f"{accep}%")
    plt.ylim(0, 1)
    plt.yticks(np.arange(0, 1.1, 0.2))
plt.xlabel("Offset in coordinates along the expected path (in pixels)")
plt.ylabel("Acceptance rate")
plt.legend(title='Perctange of acceptable points', loc='upper center', bbox_to_anchor=(0.5, 1.35),
           fancybox=True, shadow=True, ncol=len(range(20,101,20)))
plt.show()















