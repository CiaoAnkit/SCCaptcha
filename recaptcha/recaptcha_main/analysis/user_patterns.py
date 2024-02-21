import json 
import numpy as np
from matplotlib import pyplot as plt

def get_data_person_0(data):
    n = 0
    solves  = []
    for obj in data:
        if obj['id'] == 0:
            if obj['status'] == "True":
                solves.append(1)
            elif obj['status'] == "False":
                solves.append(0)
            else :
                solves.append(2)
    # make 2d array of 10 solves each and 12 solves at last
    # solves_last = solves[-12:]
    # print(solves_last)
    solves = solves[:-2]
    correct = np.array(solves)
    data_2d = correct.reshape(101,10)
    # print(data_2d)
    # result = np.append(data_2d, np.array([solves_last]), axis=0)
    return data_2d
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
                    solves.append(2)
        if len(solves) >= n:
            num+=1
            for j in solves[:n]:
                correct.append(j)
    
    for i in range(1,110):
        if i not in checks:
            print("NOT IN IDS ", i )
    # call other function to add person 0's solves
    correct = np.array(correct)
    data_2d = correct.reshape(num,n)
    flag = input("Do you want to include person 0's data? (y/n): ")
    if flag == 'y':
        # data_2d = np.append(data_2d, get_data_person_0(data), axis=0)
        data_2d = get_data_person_0(data)
    corrects = np.sum(data_2d == 1, axis=0)
    wrongs = np.sum(data_2d == 0, axis=0)
    robots = np.sum(data_2d == 2, axis=0)
    print("FOR ", num, " PEOPLE :")
    print(corrects)
    print(wrongs)
    print(robots)
    bar_width = 0.8
    plt.rcParams.update({'font.size': 16})
    num_solves = n
    plt.bar(range(num_solves), wrongs, width= bar_width, label='Incorrect', color = 'g')
    plt.bar(range(num_solves), corrects,bottom=wrongs, width =bar_width, label='Correct')
    plt.bar(range(num_solves), robots, bottom=wrongs+corrects,width = bar_width, label='Robots')

    x_labels = [f'T{i}' for i in range(1, n + 1)]  # Generate labels T1, T2, ..., T10
    plt.xticks(range(num_solves), x_labels)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=3, markerscale=2.5)
    plt.show()
def check_robots_person0(data):
    n = 0
    for obj in data:
        if obj['status'] == "Robot":
            n+=1
    print(n)

with open('./../data/path_data.json', "r") as f:
    data = json.load(f)
# check_robots_person0(data)
m = int(input("Enter the number of solves: "))
get_correctness_over_time(data,m)
# get_data_person_0(data)