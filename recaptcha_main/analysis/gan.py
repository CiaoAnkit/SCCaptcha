import numpy as np

def generate_path(start, end, avoid_ranges, min_points=70, min_rmse=0.75):
    path = [start]
    current_point = np.array(start)
    end_point = np.array(end)

    while len(path) < min_points or np.sqrt(np.mean(np.square(np.diff(path[-10:], axis=0)))) < min_rmse:
        direction = np.random.randint(0, 4)  # 0: up, 1: down, 2: left, 3: right

        # Generate a random distance to move
        distance = np.random.randint(1, 10)

        # Move in the selected direction
        if direction == 0:
            current_point[1] += distance
        elif direction == 1:
            current_point[1] -= distance
        elif direction == 2:
            current_point[0] -= distance
        elif direction == 3:
            current_point[0] += distance

        # Check if the new point is within the avoidance ranges
        avoid_flag = False
        for avoid_range in avoid_ranges:
            if avoid_range[0] <= current_point[0] <= avoid_range[1] and avoid_range[2] <= current_point[1] <= avoid_range[3]:
                avoid_flag = True
                break

        if not avoid_flag:
            # Check if the new point is getting closer to the end point
            if np.linalg.norm(current_point - end_point) < np.linalg.norm(path[-1] - end_point):
                path.append(list(current_point))

    return path

# Define the starting and ending points
start_point = [201, 390]
end_point = [361, 583]
avoid_ranges = [(281, 321, 0, float('inf')), (420, 460, 0, float('inf'))]  # Ranges to avoid

# Generate the path
path = generate_path(start_point, end_point, avoid_ranges)

print("Generated Path:")
print(path)
print("Number of points:", len(path))
