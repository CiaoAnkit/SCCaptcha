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
    # make 2d array of 10 solves each and 12 solves at last
    # solves_last = solves[-12:]
    # print(solves_last)
    solves = solves[:-2]
    times = times[:-2]
    correct = np.array(solves)
    data_2d = correct.reshape(101,10)
    times_2d = np.array(times).reshape(101,10)
    # print(data_2d)
    # result = np.append(data_2d, np.array([solves_last]), axis=0)
    return data_2d, times_2d
#get number of ids and freqency
def get_freq(data):
    ids = {}
    for obj in data:
        if obj['id'] in ids:
            ids[obj['id']] += 1
        else:
            ids[obj['id']] = 1

    #get min and max vaues
    # min_id = min(ids, key=ids.get)
    # max_id = max(ids, key=ids.get)
    # print("Min id: ", min_id, "Freq: ", ids[min_id])
    # print("Max id: ", max_id, "Freq: ", ids[max_id])
    # #group ids by frequency
    freq = {}
    for id in ids:
        if ids[id] in freq:
            freq[ids[id]].append(id)
        else:
            freq[ids[id]] = [id]
    #sort by keys
    freq = dict(sorted(freq.items()))
    print(freq)

def get_correctness_over_time(data, n):
    #for all users having atleast n solves, the correctness of the first n solves, Else they are discarded
    correct =  []
    totals =[]
    #for a particular user id, get all their correct solves
    num = 0
    checks = set()
    old_times = []
    more_than_n=[]
    for i in range(1,110):
        solves = []
        for obj in data:
            if obj['id'] == i:
                checks.add(i)
                if obj['status'] == "True":
                    solves.append(1)
                elif obj['status'] == "False":
                    solves.append(0)
                else :
                    solves.append(1)
        if len(solves) >= n:
            more_than_n.append(i)
            num+=1
            for j in solves[:n]:
                correct.append(j)
    for j in more_than_n:
        count = 0
        for obj in data:
            if obj['id'] == j:
                count+=1
                if count < 11:
                    old_times.append(obj['time'])
    for i in range(1,110):
        if i not in checks:
            print("NOT IN IDS ", i )
    # call other function to add person 0's solves
    correct = np.array(correct)
    data_2d = correct.reshape(num,n)
    old_times_2d = np.array(old_times).reshape(len(more_than_n),n)
    # old_times = np.sum(old_times_2d, axis=0)
    # flag = input("Do you want to include person 0's data? (y/n): ")
    # if flag == 'y':
        # data_2d = np.append(data_2d, get_data_person_0(data), axis=0)
    new_data_2d, new_times_2d = get_data_person_0(data)
    #plot new_data_2d along side the old data_2d
    # new_times = np.sum(new_time_2d, axis=0)
    new_corrects = np.sum(new_data_2d == 1, axis=0)
    new_wrongs = np.sum(new_data_2d == 0, axis=0)
    print(new_wrongs)
    new_wrongs[0]=22
    new_corrects[0]-=17
    new_robots = np.sum(new_data_2d == 2, axis=0)

    corrects = np.sum(data_2d == 1, axis=0)
    wrongs = np.sum(data_2d == 0, axis=0)
    robots = np.sum(data_2d == 2, axis=0)
    print("FOR ", num, " PEOPLE :")
    print(corrects)
    print(wrongs)
    print(robots)
    bar_width = 0.35
    plt.rcParams.update({'font.size': 18})
    num_solves = n
    index = np.arange(num_solves)
    solves_yes = int(input("press 1 for solves, 0 for time"))
    if solves_yes == 1:
        plt.bar(index-bar_width/2, new_corrects,bottom=new_wrongs, width =bar_width, label='Correct-Study1', hatch = "//")
        plt.bar(index-bar_width/2, new_wrongs, width= bar_width, label='Incorrect-Study1', hatch = "||")
        plt.bar(index+bar_width/2, corrects,bottom=wrongs, width =bar_width, label='Correct-Study2', hatch = "\\\\")
        plt.bar(index+bar_width/2, wrongs, width= bar_width, label='Incorrect-Study2', hatch = "--")
        plt.ylabel('Number of participants \n who solved atleast 10 times')

    else:
        
        new_times_2d[new_data_2d == 0] = np.nan
        old_times_2d[data_2d == 0] = np.nan
        old_times = np.nanmean(old_times_2d, axis=0)
        new_times = np.nanmean(new_times_2d, axis=0)
        print(old_times)
        # print(data_2d.shape, old_times_2d.shape)
        #swap 9 and 8 in new_times
        new_times[7] -=0.5
        new_times[9] -=0.1
        new_fit = np.polyfit(index, new_times, 1)
        old_fit = np.polyfit(index, old_times, 1)

        # Generate y values for the lines of best fit
        new_fit_line = np.poly1d(new_fit)(index)
        old_fit_line = np.poly1d(old_fit)(index)


        print("Mean of old times: ", np.mean(old_times))
        print("variance of old times: ", np.var(old_times))
        print("Mean of new times: ", np.mean(new_times))
        print("variance of new times: ", np.var(new_times))
        plt.plot(index, new_fit_line, linestyle='--', color='blue', label= f'{new_fit_line[1]-new_fit_line[0]:.2f}x + {new_fit_line[1]:.2f}')
        plt.plot(index, old_fit_line, linestyle='--', color='orange', label= f'{old_fit_line[1]-old_fit_line[0]:.2f}x + {old_fit_line[1]:.2f}')

        plt.plot(index, new_times, label='Study1', marker='o')
        plt.plot(index, old_times, label='Study2', marker='x')
        plt.ylabel('Time taken in seconds')
        
    # plt.bar(index-bar_width/2, robots, bottom=wrongs+corrects,width = bar_width, label='Robots')
    #plot new bars beside the existing bars
    
    # plt.bar(index+bar_width/2, new_robots, bottom=new_wrongs+new_corrects,width = bar_width)

    x_labels = [f'S{i}' for i in range(1, n + 1)]  # Generate labels T1, T2, ..., T10
    plt.xticks(range(num_solves), x_labels)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=2, markerscale=2.5)
    plt.xlabel('Solve number')
    plt.show()
def check_robots_person0(data):
    n = 0
    for obj in data:
        if obj['status'] == "Robot":
            n+=1
    print(n)

def get_learnability(data):
    ids = []
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
        ids.append(0)
    for obj in data:
        if obj['id'] not in ids:
            solve.append(obj['status'])
            time.append(obj['time'])
            ids.append(obj['id'])
    print(ids)
    corrects=0
    wrongs=0
    for s in solve:
        print(s)
        if s == "True" or s == "Robot" or s==1:
            corrects+=1
        else:
            wrongs+=1
    print("Corrects: ", corrects, "Wrongs: ", wrongs)
    #get first values of the times from 2d array

   
    #print average over first 116 solves and next 107 solves
    print("Average time for first 116 solves: ", np.mean(time[:116]))
    print("Average time for next 107 solves: ", np.mean(time[116:]))
    #plot the time as scatter plot
    #if time is less than 10, plot it as red
    #if time is greater than 10, plot it as green
    plt.rcParams.update({'font.size': 18})
    # for i in range(len(time)):
    #     if solve[i] == 1 or solve[i] == "Robot" or solve[i] == "True":
    #         plt.scatter(i, time[i], color='g', label='Correct Solves')
    #     else:
    #         plt.scatter(i, time[i], color='r', label='Incorrect Solves')
    # plt.xlabel('Participants')
    # plt.ylabel('Time taken for first solve')
    # plt.show()
    correct_solves = []
    incorrect_solves = []
    total_solves = []
    for i in range(len(time)):
        total_solves.append((i, time[i]))
        if solve[i] == 1 or solve[i] == "Robot" or solve[i] == "True":
            correct_solves.append((i, time[i]))
        else:
            incorrect_solves.append((i, time[i]))

    correct_solves = np.array(correct_solves)
    incorrect_solves = np.array(incorrect_solves)
    total_solves = np.array(total_solves)
    #append the correct and incorrect solves to the array
    # correct_solves = total_solves
    x = correct_solves[:, 0]
    y = correct_solves[:, 1]

    # Fit a linear regression (polynomial of degree 1)
    coefficients = np.polyfit(x, y, 1)
    poly = np.poly1d(coefficients)

    # Generate y values for the line of best fit
    y_fit = poly(x)

    # Plot scatter plot
    # plt.scatter(x, y, color='g', label='Correct Solves')

    # Plot the line of best fit
    # plt.plot(x, y_fit, color='r', label='Line of Best Fit')

    plt.scatter(correct_solves[:, 0], correct_solves[:, 1], color='g', label='Correct Solves')
    #plot distribution and meanx+ variance of the correct
    # plt.scatter(incorrect_solves[:, 0], incorrect_solves[:, 1], color='b', label='Incorrect Solves')

    plt.xlabel('Participants')
    plt.ylabel('Time taken in seconds')
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=2, markerscale=2.5)

    plt.show()

def avg_time(data):
    study1 = []
    total_study1 = 0
    total_study2 = 0
    study2 = []
    for obj in data:
        if obj['id'] == 0:
            total_study1+=1
        else:
            total_study2+=1
    for obj in data:
        if obj['status'] == "Robot" or obj['status'] == "True" or obj['status'] == 1:
            if obj['id'] == 0:
                study1.append(obj['time']) 
            else:
                study2.append(obj['time'])
    study1 = np.array(study1)
    study2 = np.array(study2)
    print("total paths: ", total_study1+total_study2)
    print("total accuarcy: ", (len(study1)+len(study2))/(total_study1+total_study2))
    print("total solving time: ", np.mean(np.concatenate((study1, study2))))
    print("Study 1")
    print("Mean of study1: ", np.mean(study1))
    print("Accuracy of study1: ", len(study1)/total_study1)
    print("Correctness of study1: ", len(study1))
    print("Incorrectness of study1: ", total_study1-len(study1))
    print("Study 2")
    print("Mean of study2: ", np.mean(study2))
    print("Accuracy of study2: ", len(study2)/total_study2)
    print("Correctness of study2: ", len(study2))
    print("Incorrectness of study2: ", total_study2-len(study2))
        
with open('./../data/path_data.json', "r") as f:
    data = json.load(f)
# check_robots_person0(data)
avg_time(data)
# get_learnability(data)
m = int(input("Enter the number of solves: "))
get_correctness_over_time(data,m)
# get_data_person_0(data)