import json

# with open("../data/path_dump.json") as f:
#     data = json.load(f)

# with open('status_only.json', 'a') as f1:
#     l = 0
#     for obj in data:
#         l+=1
#         #write status to another file along with new filed called id
#         f1.write(json.dumps({'status': obj['status'], 'id': "", 'uid':l}) + ','+'\n')

def show_data(data, n, uids_done):
    num = 0
    for obj in reversed(data):
        if obj['id'] == "":
            num+=1
            print(obj['status'], "-", num, "-", obj['uid'])
            n -= 1
        if n == 0:
            break

def insert_data(data,n,k,uids_done):
    new_data = []
    uids = []
    for obj in reversed(data):
        if obj['id'] == "" and obj['uid'] not in uids_done:
            obj['id'] = k
            new_data.append(obj)
            uids.append(obj['uid'])
            n -= 1
        if n == 0:
            break    
    with open("status_id.json", "a") as f:
        for obj in reversed(new_data):
            f.write(json.dumps(obj) + ',' + '\n')
    return uids


with open("status_only.json") as f:
    data = json.load(f)
uids_done = []
# for i in range(1923,2200):
#     uids_done.append(i)

while True:
    n = int(input("Enter the number of status you want to see: "))
    show_data(data, n, uids_done)
    m = int(input("Enter the number of status you want to insert: "))
    k = int(input("Enter the id from which you want to start inserting: "))
    uids = insert_data(data, m, k, uids_done)
    for uid in uids:
        uids_done.append(uid)
