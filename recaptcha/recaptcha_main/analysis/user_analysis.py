from matplotlib import pyplot as plt
import numpy as np
import json
import random
def plot_responses(robots, wrongs, rights):
    labels = 'Robots', 'Incorrect', 'Correct'
    sizes = [robots, wrongs, rights]
    explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Incorrect')
    plt.rcParams.update({'font.size': 22})
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',  startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Responses')
    plt.show()
    plt.savefig('./plots/responses-pie.png')

def plot_learnability(data):
    #for every 10 responses, calculate the percentage of correct responses
    '''
    correct responses for every person
    '''
    learnability = []
    for i in range(0, len(data), 10):
        correct = 0
        for j in range(i, i+10):
            if j < len(data) and data[j]['status'] == 'True':
                correct += 1
        learnability.append(correct/10)
    plt.plot(learnability)
    plt.title('Learnability')
    plt.show()

def plot_solving_times (data, ball_speed):
    '''
    plot the solving times for each captcha
    '''
    solving_times = []
    for obj in data:
        solving_times.append(len(obj['path'])/ball_speed)
    plt.plot(solving_times)
    plt.title('Solving Times')
    plt.show()
    

def plot_solving_times_averaged_over_persons_each_solve(data, ball_speed, num_solves):
    #calculate the average solving time for every 10th
    solving_time = []
    data = data[:len(data)//num_solves*num_solves]
    for obj in data:
        solving_time.append(len(obj['path'])/ball_speed)
    solving_time = np.array(solving_time)
    print("number of people ", len(data)//num_solves)
    data_2d = solving_time.reshape(len(data)//num_solves,num_solves)
    averaged = np.mean(data_2d, axis=0)
    # plt.plot(averaged)
    # plt.title('Solving Times Averaged Over Persons')
    # plt.show()
    #plot a bar graph for averaged and let y axis be 5 to 6
    plt.rcParams.update({'font.size': 20})
    plt.bar(range(num_solves), averaged)
    plt.ylim(5, 6)
    x_labels = [f'T{i}' for i in range(1, num_solves + 1)]  # Generate labels T1, T2, ..., T10
    plt.xticks(range(num_solves), x_labels)
    plt.ylabel('Solving Time (s)')
    plt.show()

def plot_correctness_over_solves(data, num_solves):
    correct =  []
    totals =[]
    data = data[:len(data)//num_solves*num_solves]
    for obj in data:
        if obj['status'] == "True":
            correct.append(1)
        elif obj['status'] == "False":
            correct.append(0)
        else:
            correct.append(2)
    correct = np.array(correct)
    data_2d = correct.reshape(len(data)//num_solves,num_solves)
    #plot corrects, wrongs, and robots over bar graph and display percetanges inside
    corrects = np.sum(data_2d == 1, axis=0)
    wrongs = np.sum(data_2d == 0, axis=0)
    robots = np.sum(data_2d == 2, axis=0)
    bar_width = 0.8
    plt.rcParams.update({'font.size': 16})

    plt.bar(range(num_solves), wrongs, width= bar_width, label='Incorrect', color = 'g')
    plt.bar(range(num_solves), corrects,bottom=wrongs, width =bar_width, label='Correct')
    plt.bar(range(num_solves), robots, bottom=wrongs,width = bar_width, label='Robots')

    for i in range(num_solves):
        totals= corrects[i] + wrongs[i] + robots[i]
        plt.text(i, wrongs[i]/2, f'{wrongs[i] / totals * 100:.1f}%', ha='center', va='center', color='black')
    x_labels = [f'T{i}' for i in range(1, num_solves + 1)]  # Generate labels T1, T2, ..., T10
    plt.xticks(range(num_solves), x_labels)
    plt.ylabel('No. of Solves')
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=3, markerscale=2.5)
    plt.show()
    
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
        
    
#read data from path_dump.json
with open('path_dump.json') as f:
    data = json.load(f)


robots  = 0
wrongs = 0
rights = 0

for obj in data:
    if obj['status'] == 'True':
        rights += 1
    elif obj['status'] == 'False':
        wrongs += 1
    else:
        robots += 1

plot_responses(robots, wrongs, rights)
# plot_learnability(data)
# ball_speed = get_approx_ball_speed(data)
# # print("ball speed: ", ball_speed, "m/s")
# num_solves = int(input("Enter the number of solves: "))
# # plot_solving_times_averaged_over_persons_each_solve(data, ball_speed, num_solves)
# plot_correctness_over_solves(data, num_solves)