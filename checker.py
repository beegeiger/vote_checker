import csv

race_line =[]
candidate_line =[]
all_votes = []

with open('votes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count = 0:
            race_line = row
        elif line_count = 1:
            candidate_line = row
        else:
            all_votes.append(row) 

input = [race_line, candidate_line, all_votes]

def check_races(race_line):
    """Outputs Dictionary where race["specific race"] = ["first index of race", "last index of race"] from race_line list"""
    races = {}
    start_index = 99999
    current_race = ""
    for ind, column in enumerate(race_line[9:]):
        cell = column.split("(RCV)")
        race = cell[0]
        if race != "current_race":
            if len(races)==0:
                current_race = race
                start_index = ind
            else:
                races[curent_race] = [start_index, ind - 1]
                current_race = races
                start_index = ind
    return races