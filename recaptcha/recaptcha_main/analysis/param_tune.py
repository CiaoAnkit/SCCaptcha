from matplotlib import pyplot as plt

file = './parameter.txt'
with open(file, 'r') as f:
    data = f.readlines()
    data = [x.strip() for x in data]
X = []
Y = []
m = []
s = []
accuracy = []
precision = []
recall = []
f1_score = []
for x in data:
    print(x)
    X.append(float(x.split(",")[0][1:]))
    Y.append(float(x.split(",")[1]))
    m.append(float(x.split(",")[2]))
    s.append(float(x.split(",")[3]))
    accuracy.append(float(x.split(",")[4]))
    precision.append(float(x.split(",")[5]))
    recall.append(float(x.split(",")[6]))
    f1_score.append(float(x.split(",")[7][:-1]))
first_accuracy = {}
for x, y, acc in zip(X, Y, accuracy):
    if (x, y) not in first_accuracy:
        first_accuracy[(x, y)] = acc

# Extract unique X and Y values
unique_X = sorted(set(X))
unique_Y = sorted(set(Y))

# Plot the first accuracy value for each unique pair of X and Y
plt.figure(figsize=(8, 6))
# for x, y in first_accuracy:
#     plt.scatter(x, y, c='blue', s=100)  # Plot the point
#     plt.text(x, y, f'{first_accuracy[(x, y)]:.2f}', ha='center', va='center')  # Display the accuracy value
#  
plt.xlabel('X')
plt.ylabel('Y')
plt.xlim(min(unique_X) - 0.1, max(unique_X) + 0.1)
plt.ylim(min(unique_Y) - 0.1, max(unique_Y) + 0.1)
plt.title('First Accuracy Value for Unique Pairs of X and Y')
plt.grid(True)
plt.show()
