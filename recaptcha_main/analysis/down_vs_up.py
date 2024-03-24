from matplotlib import pyplot as plt
import json
#open file
def get_vals(study1, study2):
    with open('../data/path_data.json', 'r') as file:
        data = json.load(file)

    up=0
    down=0
    uptime = []
    downtime = []
    uptrue = []
    false = 0
    true = 0
    downtrue = []
    time_taken = []
    total_up = 0
    total_down = 0
    for obj in (data[:1012] if study1 else data[1012:]):
    # for obj in data:
            last = obj['path'][-1]
            time = obj['time']
            if last[0] < 412/2:
            # if last[1] < 786/2:
                total_up+=1
            else:
                total_down+=1
            if obj['status'] == False or obj['status']== 'False':
                false+= 1
                if last[0] < 412/2:
                # if last[1] < 786/2:
                    up+=1
                    uptime.append(time)
                    uptrue.append(obj['status'])
                else:
                    down+=1
                    downtime.append(time)
                    downtrue.append(obj['status'])
            else:
                true+= 1
            time_taken.append(time)
    print("False: ", false)
    print("True: ", true)
    print("accuracy: ", true/(true+false))
    print("Time: ", sum(time_taken)/len(time_taken))
    print("Up: ", up)
    print("Uptotal: ", total_up)
    print("Percentage up which are false : ", up/total_up)
    print("Down: ", down)
    print("Downtotal: ", total_down)
    print("Percentage down which are false : ", down/total_down)
    print("Up Time: ", sum(uptime)/len(uptime))
    print("Down Time: ", sum(downtime)/len(downtime))

study = int(input("Enter 1 for study 1 and 2 for study 2: "))
if study == 1:
    get_vals(True, False)
else:
    get_vals(False, True)

