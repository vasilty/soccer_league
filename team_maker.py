import csv
import json

from operator import itemgetter


with open('soccer_players.csv', newline='') as csvfile:
    childdata = csv.DictReader(csvfile)
    rows = list(childdata)

#  Sort children by height    
sorted_data = sorted(rows, key=itemgetter('Height (inches)'))

#  Create lists of experienced and non-experienced children from a sorted list
exp = []
nonexp = []
for row in sorted_data:
    if row['Soccer Experience'] == 'YES':
        exp.append(row)
    else:
        nonexp.append(row)
teams = [ {'Dragons': []}, {'Sharks': []}, {'Raptors': []} ]

#  To get teams with a similar average height, children are picked following
#  the pattern tallest + shortest
while True:
    for team in teams:
        for key, value in team.items():
            if len(exp):
                team[key].append(exp[0])
                exp.pop(0)
            if len(nonexp):
                team[key].append(nonexp[-1])
                nonexp.pop(-1)
    if len(exp) == 0  and len(nonexp) == 0:    
        break

# Print members of each team and average height of teams
for team in teams:
    for key, value in team.items():
        print('\nTeam {}:'.format(key))
        height = 0
        for child in value:
            height += int(child['Height (inches)'])
            print('{}  Experience: {}'.format(child['Name'],
                                              child['Soccer Experience']))
        print('Average height of {}: {}'.format(key, height/len(value)))

# Print files for a league and for each team
with open('league.txt', 'w') as leaguefile:
    json.dump(teams, leaguefile)
for team in teams:
    for key, value in team.items():
        name = key.lower() + '.txt'
    with open(name, 'w') as teamfile:
        json.dump(team, teamfile)

# Create letters
counter = 1
for team in teams:
    for key, value in team.items():
        if key == 'Dragons':
            date = 'March 17, 1pm'
        elif key == 'Sharks':
            date = 'March 17, 3pm'
        else:
            date = 'March 18, 1pm'
        for child in value:
            letter = 'letter ' + str(counter) + '.txt'
            with open(letter, 'w') as newletter:
                newletter.write(
'''Hello {},\n
congratulations, {} has been placed on the team {}! The first team practice
will take place {}.\n
See you there,
Tatiana'''.format(child['Guardian Name(s)'],
                         child['Name'], key, date)
                )
            counter += 1
