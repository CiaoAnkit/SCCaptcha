import math
import json
from colorama import Fore
def test_dist(a,b,path):
    if a[0] is None or b[0] is None or a[1] is None or b[1] is None:
        print(path)   
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) #has a problem TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) #has a problem TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'

def dump_data(status, path, file_path, dump_flag, time_taken):
    if dump_flag:
        data_to_append = {"status": status, "path": path, "time": time_taken}
        with open(file_path, 'a') as file:
            json.dump(data_to_append, file)
            file.write(',\n')

def get_min_points(width, height, captcha_box):
    #we set values little less than actual values at which we measure due to possible inconsistencies &async issues
    sampling_rate = 0.1
    ball= [math.ceil(0.45*width), height//2]
    distance = dist(ball, captcha_box)
    sampling_interval = 1/sampling_rate
    num_points = distance /sampling_interval
    return int(num_points)

def get_random_page(num):
    if num == 1:
        return "./task/acc-task1.html"
    elif num == 2:
        return "./task/acc-task2.html"
    elif num == 3:
        return "./task/als-task1.html"
    elif num == 4:
        return "./task/als-task2.html"
    elif num == 5:
        return "./task/fallback.html"
    elif num == 6:
        return "./task/gyro-task1.html"
    elif num == 7:
        return "./task/gyro-task2.html"
