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
file_path = "./path_dump.json"
# Read data from the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)
#latest plots will be displayed first
humans = 0
robots = 0
leng = 0
MEAN_THRESHOLD = float(input("what threshold do you want to set?"))
INTERVALS_THRESHOLD = 0.75
true_robot = 0
total_mean_rmse = 0
mean_time = 0
times = []
rights = 0
for obj in reversed(data):
    if "path" in obj:
        path = [point for point in obj.get("path", []) if None not in point]

        interval = 10
        x_values, y_values = zip(*path)
        rmse_values = calculate_rmse_for_interval(path, interval)
        # plot_graph(x_values, y_values, rmse_values, interval, obj.get("status"))
        mean_rmse = sum(rmse_values)/len(rmse_values)
        count = 0
        for i in range(len(rmse_values)):
            if rmse_values[i] > INTERVALS_THRESHOLD:
                count += 1
        if count >= len(rmse_values)/3 and mean_rmse > MEAN_THRESHOLD:
            print(mean_rmse)
            humans += 1

        else:
            print(Fore.RED, "ROBOT")
            print(Fore.WHITE,"Mean RMSE: ", mean_rmse, obj.get("status"))
            print("Count is",count, "Len is", len(rmse_values))
            robots += 1
            if obj.get("status") == "Robot":
                true_robot = +1
        if obj.get("status") == "True":
            rights+=1
        total_mean_rmse+=mean_rmse
        leng+=1
        if 'time' in obj:
            tim= obj.get('time')
            times.append(tim)
result_file = "./results.txt"
with open(result_file, "a") as f:
    data = str([MEAN_THRESHOLD, INTERVALS_THRESHOLD, count/len(rmse_values), humans, robots])
    f.write(data)
    f.write('\n')

print("Humans: ", humans, "Robots: ", robots, "True Robots: ", true_robot)
total = humans + robots
print("Data points : ", total)
#plot times statistics
print("TIME STATS")
print("Mean time: ", sum(times)/len(times))
print("Max time: ", max(times))
print("Min time: ", min(times))
print("Median time: ", sorted(times)[len(times)//2])
plot_graph_t(times)
print(Fore.CYAN,"Rights: ", rights, "Wrongs", humans-rights, "Success rate: ", rights/humans * 100)
print(Fore.RED,"Total Mean RMSE: ", total_mean_rmse/leng)
print(Fore.WHITE,"Solving time: ", sum(times)/len(times))




