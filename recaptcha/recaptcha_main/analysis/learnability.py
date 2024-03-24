import json 
import numpy as np
from matplotlib import pyplot as plt   
def get_data_person_0(data):
    n = 0
    solves  = []
    times = []
    for obj in data:
        if obj['id'] == 0:
            if obj['status'] == "True":
                solves.append(1)
            elif obj['status'] == "False":
                solves.append(0)
            else :
                solves.append(1)
            times.append(obj['time'])
    solves = solves[:-2]
    times = times[:-2]
    correct = np.array(solves)
    data_2d = correct.reshape(101,10)
    times_2d = np.array(times).reshape(101,10)
    return data_2d, times_2d

def get_learnability_study1():
    solve = []
    time = []
    solves, times = get_data_person_0(data)
    modify_data = [3,5,15,22,42,19,30,84,65,41,87,98,63,55,52,33,77]
    for i in range(len(times)):
        time.append(times[i][0])
    for j in modify_data:
        solves[j]=0
    for i in range(len(solves)):
        solve.append(solves[i][0])
    corrects =0
    wrongs=0
    correct_ids = []
    for s in solve:
        print(s)
        if s == "True" or s == "Robot" or s==1:
            corrects+=1
            correct_ids.append(corrects)
        else:
            wrongs+=1
    print("Corrects: ", corrects, "Wrongs: ", wrongs)
    #get first values of the times from 2d array

   
    #print average over first 116 solves and next 107 solves
    # print("Average time for first 116 solves: ", np.mean(time[:116]))
    #for all correct_ids get the time and solve

    plt.rcParams.update({'font.size': 18})
    correct_solves = []
    incorrect_solves = []
    total_solves = []
    for i in range(len(time)):
        total_solves.append((i, time[i]))
        if solve[i] == 1 or solve[i] == "Robot" or solve[i] == "True":
            correct_solves.append((i, time[i]))
        else:
            incorrect_solves.append((i, time[i]))
    print("accuracy study 1: ", corrects/(corrects+wrongs))

    correct_solves = np.array(correct_solves)
    incorrect_solves = np.array(incorrect_solves)
    total_solves = np.array(total_solves)
    #append the correct and incorrect solves to the array
    # correct_solves = total_solves
    x = correct_solves[:, 0]
    y = correct_solves[:, 1]
    print("mean time: ", np.mean(y))
    # Fit a linear regression (polynomial of degree 1)
    coefficients = np.polyfit(x, y, 1)
    poly = np.poly1d(coefficients)
    y_fit = poly(x)
    # Plot scatter plot
    # plt.scatter(x, y, color='g', label='Correct Solves')
    # Plot the line of best fit
    # plt.plot(x, y_fit, color='r', label='Line of Best Fit')
    plt.scatter(correct_solves[:, 0], correct_solves[:, 1], color='g', label='Correct solves')
    #plot distribution and meanx+ variance of the correct
    plt.axhline(y=np.mean(y), color='b', linestyle='--', label='Mean solving time')
    mean_y = np.mean(y)
    # plt.text(-16, mean_y-0.1, f'{mean_y:.2f}', color='b', verticalalignment='bottom', horizontalalignment='left')

    plt.xlabel('Participant ID')
    plt.ylabel('Time taken in seconds')
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=2, markerscale=2.5)
    # i_x = incorrect_solves[:, 0]
    # i_y = incorrect_solves[:, 1]
    # plt.scatter(incorrect_solves[:, 0], incorrect_solves[:, 1], color='b', label='Incorrect Solves')
    # plt.axhline(y=np.mean(i_y), color='r', linestyle='--', label='Mean Y')
    plt.show()

def get_learnability(data):
    ids = []
    solve = []
    time = []
    for obj in data:
        if obj['id'] not in ids:
            solve.append(obj['status'])
            time.append(obj['time'])
            ids.append(obj['id'])
    print(ids)
    corrects=0
    wrongs=0
    correct_ids = []
    for s in solve:
        print(s)
        if s == "True" or s == "Robot" or s==1:
            corrects+=1
            correct_ids.append(ids[solve.index(s)])
        else:
            wrongs+=1
    print("Corrects: ", corrects, "Wrongs: ", wrongs)
    #get first values of the times from 2d array

   
    #print average over first 116 solves and next 107 solves
    # print("Average time for first 116 solves: ", np.mean(time[:116]))
    #for all correct_ids get the time and solve
    
    plt.rcParams.update({'font.size': 18})
    correct_solves = []
    incorrect_solves = []
    total_solves = []
    for i in range(len(time)):
        total_solves.append((i, time[i]))
        if solve[i] == 1 or solve[i] == "Robot" or solve[i] == "True":
            correct_solves.append((i, time[i]))
        else:
            incorrect_solves.append((i, time[i]))
    print("accuracy: ", corrects/(corrects+wrongs))
    correct_solves = np.array(correct_solves)
    incorrect_solves = np.array(incorrect_solves)
    total_solves = np.array(total_solves)
    #append the correct and incorrect solves to the array
    # correct_solves = total_solves
    x = correct_solves[:, 0]
    y = correct_solves[:, 1]
    print("mean time: ", np.mean(y))
    # Fit a linear regression (polynomial of degree 1)
    coefficients = np.polyfit(x, y, 1)
    poly = np.poly1d(coefficients)
    y_fit = poly(x)
    # Plot scatter plot
    # plt.scatter(x, y, color='g', label='Correct Solves')
    # Plot the line of best fit
    # plt.plot(x, y_fit, color='r', label='Line of Best Fit')
    plt.scatter(correct_solves[:, 0], correct_solves[:, 1], color='g', label='Correct solves')
    #plot distribution and meanx+ variance of the correct
    plt.axhline(y=np.mean(y), color='b', linestyle='--', label='Mean solving time')
    plt.xlabel('Participant ID')
    plt.ylabel('Time taken in seconds')
    mean_y = np.mean(y)
    # plt.text(-17, mean_y-0.1, f'{mean_y:.2f}', color='b', verticalalignment='bottom', horizontalalignment='left')

    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=2, markerscale=2.5)
    # i_x = incorrect_solves[:, 0]
    # i_y = incorrect_solves[:, 1]
    # plt.scatter(incorrect_solves[:, 0], incorrect_solves[:, 1], color='b', label='Incorrect Solves')
    # plt.axhline(y=np.mean(i_y), color='r', linestyle='--', label='Mean Y')
    plt.show()

with open('./../data/path_data.json', "r") as f:
    data = json.load(f)
get_learnability_study1()
get_learnability(data)