import json
import matplotlib.pyplot as plt
import math
from colorama import Fore, Back, Style

def calculate_perpendicular_distance(point, line_start, line_end):
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end
    if (x1 == x2):
        x1 += 0.0001
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    distance = abs((m * x - y + b) / math.sqrt(m**2 + 1))
    return distance

def calculate_deflection(path, line_start, line_end):
    """Calculate deflection of points in the path from the line."""
    distances = [calculate_perpendicular_distance(point, line_start, line_end) for point in path]
    return sum(distances)/len(distances)

def calculate_rmse_for_interval(path, interval):
    """Calculate RMSE between the first point and every z-th point in the path."""

    rmse_values = []
    for i in range(0, len(path) - interval, interval):
        subset_path = path[i : i + interval + 1]
        rmse = calculate_deflection(subset_path, path[i], path[i + interval])
        rmse_values.append(rmse)

    # Calculate RMSE for the last interval separately
    last_subset_path = path[-interval - 1:]
    last_rmse = calculate_deflection(last_subset_path, last_subset_path[0], path[-1])
    rmse_values.append(last_rmse)

    return rmse_values


def plot_graph(x_values, y_values, rmse_values, interval, status):
    plt.plot(x_values, y_values, marker='o', linestyle='-')
    plt.title("Path Plot (excluding null values)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()

def plot_graph_t(x_values):
    #plot x values versus frequency buckets more smoother than histogram
    plt.hist(x_values, bins=30)
    plt.title("Time Plot")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

   

# Specify the file path
file_path = "../data/path_data.json"
# Read data from the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)
#latest plots will be displayed first

humans = 0
robots = 0
leng = 0
# 1.4 and 0.75
MEAN_THRESHOLD = float(input("what threshold do you want to set?")) #aka T1
INTERVALS_THRESHOLD = float(input("what threshold do you want to set for the number of points above the threshold?")) # aka T2
true_robot = 0
total_mean_rmse = 0
mean_time = 0
times = []
rights = 0
true_pos = 0 #correctly solved and classified as human
true_neg = 0 #wrongly solved
false_neg = 0 # classified as robot but is human
false_pos = 0 #always zero 
correctly_solved = 0
print("following values need to be non zero")
m=int(input("what interval do you want to set? aka m"))
s = int(input("how many parts do you want the threshold to be satisfied by? aka s"))
len_rmses = []
mean_rmses = []
for obj in reversed(data):
    if obj.get("status") == "False" or obj.get("status") == "false" or obj.get("status") == 0:
        true_neg+=1
    else:
        correctly_solved+=1
        if "path" in obj:
            path = [[201, 390], [201, 392], [209, 388], [209, 393], [207, 398], [209, 398], [210, 398], [211, 398], [218, 398], [227, 398], [228, 398], [230, 398], [227, 406], [224, 414], [217, 421], [217, 429], [224, 429], [229, 429], [236, 429], [236, 434], [233, 437], [226, 445], [226, 453], [228, 453], [217, 466], [213, 477], [180, 567], [189, 564], [192, 564], [196, 560], [204, 560], [204, 563], [208, 563], [213, 587], [218, 597], [221, 597], [228, 597], [229, 587], [229, 583], [235, 583], [236, 586], [236, 581], [243, 581], [244, 581], [250, 587], [257, 587], [257, 584], [262, 563], [262, 572], [267, 572], [267, 580], [269, 592], [277, 592], [278, 595], [324, 551], [325, 551], [325, 557], [322, 562], [324, 562], [328, 562], [337, 562], [344, 562], [353, 562], [355, 562], [347, 599], [358, 600], [357, 596], [357, 590], [359, 590], [357, 585]]
            interval = m
            x_values, y_values = zip(*path)
            rmse_values = calculate_rmse_for_interval(path, interval)
            # plot_graph(x_values, y_values, rmse_values, interval, obj.get("status"))
            mean_rmse = sum(rmse_values)/len(rmse_values)
            count = 0
            len_rmses.append(len(rmse_values))
            mean_rmses.append(mean_rmse)
            for i in range(len(rmse_values)):
                if rmse_values[i] > INTERVALS_THRESHOLD:
                    count += 1
            if count >= len(rmse_values)/s and mean_rmse > MEAN_THRESHOLD:
                humans += 1
                print("Human")
                if obj.get("status") == "True" or obj.get("status") == 1:
                    rights+=1
                    true_pos+=1

            else:
                if obj.get("status") == "True" or obj.get("status") == 1:
                    rights+=1
                    false_neg+=1
                    # print(mean_rmse)

        
            total_mean_rmse+=mean_rmse
            leng+=1
            if 'time' in obj:
                tim= obj.get('time')
                times.append(tim)


total = rights+true_neg
accuracy = (true_pos+true_neg)/(true_pos+true_neg+false_pos+false_neg)
precision = true_pos/(true_pos+false_pos)
recall = true_pos/(true_pos+false_neg)
f1_score = 2*(true_pos/(true_pos+false_pos))*(true_pos/(true_pos+false_neg))/(true_pos/(true_pos+false_pos)+true_pos/(true_pos+false_neg))
print("accuracy: ", accuracy)
print("precision: ", precision)
print("recall: ", recall)
print("f1 score: ", f1_score)

# print("accuracy: ", (true_pos+true_neg)/(true_pos+true_neg+false_pos+false_neg))
# print("success rate: ", correctly_solved/total*100)
# print(correctly_solved)
# print("Number of Intervals:  mean: ", sum(len_rmses)/len(len_rmses), "median: ", sorted(len_rmses)[len(len_rmses)//2])
# print("Mean RMSE:  mean: ", sum(mean_rmses)/len(mean_rmses), "median: ", sorted(mean_rmses)[len(mean_rmses)//2], "max: ", max(mean_rmses), "min: ", min(mean_rmses))
# # print("Humans: ", humans, "Robots: ", robots, "True Robots: ", true_robot)
# # total = humans + robots
# # print("Data points : ", total)
# # #plot times statistics
# # print("TIME STATS")
# print("Mean time: ", sum(times)/len(times))
# # print("Max time: ", max(times))
# # print("Min time: ", min(times))
# print("Median time: ", sorted(times)[len(times)//2])
# # plot_graph_t(times)
# # print(Fore.CYAN,"Rights: ", rights, "Wrongs", humans-rights, "Success rate: ", rights/humans * 100)
# # print(Fore.RED,"Total Mean RMSE: ", total_mean_rmse/leng)
# # print(Fore.WHITE,"Solving time: ", sum(times)/len(times))
result_file = "./parameter.txt"
with open(result_file, "a") as f:
    data = str([MEAN_THRESHOLD, INTERVALS_THRESHOLD,m,s, accuracy,precision, recall, f1_score])
    f.write(data)
    f.write('\n')



