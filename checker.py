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
    """Outputs Dictionary where races["specific race"] = ["first index of race", "last index of race"] from race_line list"""
    races = {}
    start_index = 99999
    current_race = ""
    for ind, column in enumerate(race_line[9:]):
        cell = column.split("(RCV)")
        race = cell[0]
        if race != current_race:
            if len(races)==0:
                current_race = race
                start_index = ind
            elif ind == len(race_line) - 1:
                races[curent_race] = [start_index, ind]
            else:
                races[curent_race] = [start_index, ind - 1]
                current_race = races
                start_index = ind
    return races



def check_rounds(races, candidate_line):
    """Outputs races = {"race1": [["first index of race", "last index of race"],[cand1, cand2, etc.],[[round1_start_ind, round1_end_ind], [round2_start_ind, round_2_end_ind], etc.]]}"""
    for overall_ind,race in enumerate(races):
        start_ind = races[race][0]
        last_ind = races[race][1]
        race_data = candidate_line[start_ind: last_ind + 1]
        round_break = []
        candidate_list = []
        round_start_index = 9999
        race_round_tracker = []
        for race_ind, cand_cell in enumerate(race_data):
            cand = cand_cell.split("(")[0]
            if cand not in candidate_list:
                candidate_list += cand
                if len(candidate_list) == 1:
                    round_start_index = 0
            elif cand == candidate_list[0]:
                race_round_tracker.append([round_start_index, race_ind - 1])
            elif race_ind == len(race_data) - 1:
                race_round_tracker.append([round_start_index, race_ind])
                races[race] = [races[race], candidate_list, race_round_tracker]
        return races