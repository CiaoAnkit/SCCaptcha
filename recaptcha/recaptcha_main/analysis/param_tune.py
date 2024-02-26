from matplotlib import pyplot as plt

file = './parameter.txt'
with open(file, 'r') as f:
    data = f.readlines()
    data = [x.strip() for x in data]
T1 = []
T2 = []
m = []
s = []
accuracy = []
precision = []
recall = []
f1_score = []
new_t1 = []
new_t2 = []
new_m = []
new_recall = []
for x in data[:-3]:
    if int(x.split(",")[3])==3:
        print(x)
        T1.append(float(x.split(",")[0][1:]))
        T2.append(float(x.split(",")[1]))
        m.append(float(x.split(",")[2]))
        # s.append(float(x.split(",")[3]))
        accuracy.append(float(x.split(",")[4]))
        precision.append(float(x.split(",")[5]))
        recall.append(float(x.split(",")[6]))
        f1_score.append(float(x.split(",")[7][:-1]))
    else:
        new_t1.append(float(x.split(",")[0][1:]))
        new_t2.append(float(x.split(",")[1]))
        new_m.append(float(x.split(",")[2]))
        new_recall.append(float(x.split(",")[6]))
# print(T1
# first_accuracy = {}
# for x, y, acc in zip(X, Y, accuracy):
#     if (x, y) not in first_accuracy:
#         first_accuracy[(x, y)] = acc

# # Extract unique X and Y values
# unique_X = sorted(set(X))
# unique_Y = sorted(set(Y))

# # Plot the first accuracy value for each unique pair of X and Y

# # for x, y in first_accuracy:
# #     plt.scatter(x, y, c='blue', s=100)  # Plot the point
# #     plt.text(x, y, f'{first_accuracy[(x, y)]:.2f}', ha='center', va='center')  # Display the accuracy value
# #  
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.xlim(min(unique_X) - 0.1, max(unique_X) + 0.1)
# plt.ylim(min(unique_Y) - 0.1, max(unique_Y) + 0.1)
# plt.title('First Accuracy Value for Unique Pairs of X and Y')
# plt.grid(True)
# plt.show()
#plot T1 and recall as line plotwith dots
plt.figure(figsize=(10, 6))
plt.rcParams.update({'font.size': 20})

plt.plot(T1, recall, marker='o', label = "s = 1/3")
plt.plot(new_t1, new_recall, marker='o', color='red', label = "s = 1/2")
#annonate the points by adding T2, m and s

for i in range(len(T1)):
    plt.annotate(f"({T2[i]}, {m[i]})", (T1[i], recall[i]))

for i in range(len(new_t1)):
    plt.annotate(f"({new_t2[i]}, {new_m[i]})", (new_t1[i], new_recall[i]), ha = 'center', va='bottom')
# for i in range(len(T1)):
#     plt.text(T2,m,s, f'({T2[i]},{m[i]},{s[i]})')
plt.xlabel('T1')
plt.ylabel('Recall')
plt.title('T1 vs Recall')
plt.legend()
plt.show()
