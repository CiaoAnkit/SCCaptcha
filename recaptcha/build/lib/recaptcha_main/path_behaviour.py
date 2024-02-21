import json
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



def behaviour(path, INTERVALS_THRESHOLD = 0.75, MEAN_THRESHOLD = 1.4):
    interval = 10
    x_values, y_values = zip(*path)
    rmse_values = calculate_rmse_for_interval(path, interval)
    mean_rmse = sum(rmse_values)/len(rmse_values)
    count = 0
    for i in range(len(rmse_values)):
        if rmse_values[i] > INTERVALS_THRESHOLD:
            rmse_values[i] = mean_rmse
            count += 1
    if count >= len(rmse_values)/3 and mean_rmse > MEAN_THRESHOLD:
        # print("Human", "Mean RMSE: ", mean_rmse, obj.get("status"))
        print(mean_rmse)
        return 0

    else:
        print(Fore.RED, "ROBOT")
        # print(Fore.WHITE,"Mean RMSE: ", mean_rmse, obj.get("status"))
        print(Fore.WHITE, "Mean_RMSE: ", mean_rmse )
        print("Count is",count, "Len is", len(rmse_values))
        return 1
    