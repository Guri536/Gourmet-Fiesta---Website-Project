import json, itertools
with open('app1/static/JSON/fin_data.json', 'r') as file:
    var_1 = json.load(file)

# print(var_1['1']['ingredients'])
# print([list(j.keys())[0] for j in var_1['1']['ingredients']])
for i in var_1:
    print(list(itertools.chain(*[k.split() for k in [list(j.keys())[0] for j in var_1[i]['ingredients']]])))
