import csv

race_line =[]
candidate_line =[]
all_votes = []

with open('test_data.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    start_index = 0
    for ind1, row_raw in enumerate(csv_reader):
        if ind1 == 0:
            for ind2, element in enumerate(row_raw):
                if element == "BallotType":
                    start_index = ind2 + 2
        row = row_raw[start_index:]
        if line_count == 0:
            race_line = row
        elif line_count == 1:
            candidate_line = row
        else:
            all_votes.append(row) 
        line_count += 1

input = [race_line, candidate_line, all_votes]


def run_code(race_line, candidate_line, all_votes):
    races_only = check_races(race_line)
    print("1 - races from check races", races_only)
    races_with_info = check_rounds(races_only, candidate_line)
    print("2 - races from check_rounds", races_with_info)
    return

def check_races(race_line):
    """Outputs Dictionary where races["specific race"] = ["first index of race", "last index of race"] from race_line list"""
    races = {}
    start_index = 99999
    current_race = ""
    for ind, column in enumerate(race_line):
        cell = column.split("(RCV)")
        race = cell[0]
        if ind == len(race_line) - 1:
                races[current_race] = [start_index, ind]
        elif race != current_race:
            if current_race=="":
                current_race = race
                start_index = ind
            else:
                races[current_race] = [start_index, ind - 1]
                current_race = race
                start_index = ind
    return races



def check_rounds(races, candidate_line):
    """Outputs races = {"race1": [["first index of race", "last index of race"],[cand1, cand2, etc.],[[round1_start_ind, round1_end_ind], [round2_start_ind, round_2_end_ind], etc.]]}"""
    race_num = 0
    for race in races:
        race_num += 1
        start_ind = races[race][0]
        last_ind = races[race][1]
        race_data = candidate_line[start_ind: last_ind + 1]
        round_break = []
        candidate_list = []
        round_start_index = 0
        race_round_tracker = []
        for race_ind, cand_cell in enumerate(race_data):
            cand = cand_cell.split("(")[0]
            if cand not in candidate_list:
                candidate_list.append(cand)
            elif race_ind == len(race_data) - 1:
                race_round_tracker.append([round_start_index, race_ind])
                races[race] = [races[race], candidate_list, race_round_tracker]
            elif cand == candidate_list[0]:
                race_round_tracker.append([round_start_index, race_ind - 1])
                round_start_index = race_ind              
    return races

run_code(race_line, candidate_line, all_votes)