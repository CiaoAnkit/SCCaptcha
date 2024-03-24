from matplotlib import pyplot as plt
import numpy as np
import json

    
def get_effect_of_content(data):
    correct= []
    incorrect = []
    for obj in data:
        if obj['status'] == 1 or obj['status'] == "True" or obj['status'] == 'true':
            correct.append(obj['time'])
        elif obj['status'] == 0 or obj['status'] == "False" or obj['status'] == 'false':
            incorrect.append(obj['time'])
    print(len(correct), len(incorrect))
    print("accuracy: ", len(correct)/(len(correct)+len(incorrect)))
    print("mean time for correct: ", np.mean(correct))
    print("mean time for incorrect: ", np.mean(incorrect))
    print("mean solving time: ", np.mean(correct+incorrect))
with open('../data/path_data.json', 'r') as f:
    data = json.load(f)

get_effect_of_content(data[1936:])
get_effect_of_content(data[1012:1936])