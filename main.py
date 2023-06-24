import json
from cplex_model import *
from pyomo.opt import SolverFactory

# WEEKS GONE: 3, 4, 5, 6, 7, 8, 9, 10, 11
WEEK_NUMBER = 11


# Read content File

file_name = 'content_' + str(WEEK_NUMBER) + '.txt'
with open(file_name, 'r', encoding='utf8') as json_file:
    # convert json file to python dictionary: data
    data = json.load(json_file)


# Create void Data and constant

n = len(data['availablePlayers']) + len(data['availableTeams'])
role = temp_points = 0

names = []
roles = []
points = []
weights = []
budget = 1500000
limit_roles = 6

dict_data = {'players': [], 'teams': []}


# Init Data: Players

for player in data['availablePlayers']:

    name = player['name']
    position = player['position']
    if position == 'Top':
        role = 1
    elif position == 'Jungle':
        role = 10
    elif position == 'Mid':
        role = 100
    elif position == 'Bot':
        role = 1000
    elif position == 'Support':
        role = 10000
    score = float(player['scoreThisContest']['pointsPerGame'])
    salary = int(player['salary'])

    names.append(name)
    roles.append(role)
    points.append(score)
    weights.append(salary)

    dict_data['players'].append(
        {'name': name, 'role': position, 'points': score, 'salary': salary})


# Init Data: Teams

for team in data['availableTeams']:
    name = team['name']
    role = 100000
    score = float(team['scoreThisContest']['pointsPerGame'])
    salary = int(team['salary'])

    names.append(name)
    roles.append(role)
    points.append(score)
    weights.append(salary)

    dict_data['teams'].append(
        {'name': name, 'role': 'Team', 'points': score, 'salary': salary})


# Write a clean File with needed data (indent)

with open('data_indented.txt', 'w', encoding='utf8') as data_indented_file:
    # write data in a file (with indent)
    json.dump(dict_data, data_indented_file, indent=2)


# Prepare final File of best picks

with open('picks_week_' + str(WEEK_NUMBER) + '.txt', 'w', encoding='utf8') as picks_file:
    # write data in a file (with indent)
    picks_file.write('PICKS OF WEEK ' + str(WEEK_NUMBER) + '\n_____________________________________________')


# Solver function of Cplex Model

def solver(temp_points_param):
    picks_names = []
    picks_points = []
    picks_roles = []
    end_salary = end_points = end_roles = 0

    if temp_points_param == 0:
        model = buildmodel(n, budget, limit_roles, roles, points, weights)
        bool_best_picks = True

    else:
        model = buildmodel2(n, budget, limit_roles, roles, points, weights, temp_points_param)
        bool_best_picks = False

    # model.pprint()
    opt = SolverFactory('cplex_persistent')
    opt.set_instance(model)
    opt.write('knapsack.lp')
    res = opt.solve(tee=True)
    print('Obj = {}'.format(value(model.obj)))

    for p in model.x:

        print('x[{}] = {}'.format(p, value(model.x[p])))

        if value(model.x[p]) >= 0.9:
            if names[p] == 'Rogue':
                names[p] += '\t'
            picks_names.append(names[p])
            picks_points.append(points[p])
            picks_roles.append(roles[p])
            end_salary += weights[p]
            end_points += points[p]
            end_roles += roles[p]

    # Sort and Print

    picks_sorted = [x for _, x in sorted(zip(picks_roles, picks_names))]
    picks_points_sorted = [x for _, x in sorted(zip(picks_roles, picks_points))]

    print(picks_sorted)
    print(picks_points_sorted)
    print(end_salary)
    print(end_points)
    print(end_roles)
    print('\n\n__________________________________________________\n\n')

    string_file0 = '\n\nTOP:\t' + picks_sorted[0] + '\t\t - ' + str(picks_points_sorted[0])
    string_file1 = '\nJUNG:\t' + picks_sorted[1] + '\t\t - ' + str(picks_points_sorted[1])
    string_file2 = '\nMID:\t' + picks_sorted[2] + '\t\t - ' + str(picks_points_sorted[2])
    string_file3 = '\nADC:\t' + picks_sorted[3] + '\t\t - ' + str(picks_points_sorted[3])
    string_file4 = '\nSUPP:\t' + picks_sorted[4] + '\t\t - ' + str(picks_points_sorted[4])
    string_file5 = '\nTEAM:\t' + picks_sorted[5] + '\t - ' + str(picks_points_sorted[5])
    string_file6 = '\n\nSALARY TOT:\t' + str(end_salary)
    string_file7 = '\nPOINTS TOT:\t' + str(end_points)
    string_file8 = '\n(' + str(end_roles) + ')'
    string_file9 = '\n_____________________________________________'

    string_full_picks = string_file0 + string_file1 + string_file2 + string_file3 + string_file4 + \
                        string_file5 + string_file6 + string_file7 + string_file8 + string_file9

    with open('picks_week_' + str(WEEK_NUMBER) + '.txt', 'a', encoding='utf8') as picks_file:
        # write data in a file (with indent)
        picks_file.write(string_full_picks)

    if bool_best_picks:
        print(string_full_picks)

    # return new temp_points
    return end_points


# Write on final File of best picks (3 best choices)

for i in range(10):
    temp_points = solver(temp_points)


# END
