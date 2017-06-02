import json

with open('best.json', 'r') as f:
    json_data = json.load(f)
    print('JSON loaded')

pop_queue = []

l = len(json_data)

i = 0
c = 1
while c >= 1 and i + c < len(json_data) - 1:
    ind = i + c
    d1 = json_data[str(i)]['dist']
    d2 = json_data[str(ind)]['dist']
    if d1 == d2:
        pop_queue.append(i + c)
        c += 1
    else:
        print("{} is different than {} by {} meters".format(
                ind, i, round(d2-d1)))
        if ind - i > 50: 
            print("Gen diff: {}".format(ind-i))
        i = ind
        c = 1

for pop in pop_queue:
    json_data.pop(str(pop))

with open('best.min.json', 'w', newline='') as f:
    json.dump(json_data, f, separators=(',', ': '), indent=4)

print('Cut down JSON by {} items'.format(l-len(json_data)))