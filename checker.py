import csv

race_line =[]
candidate_line =[]
all_votes = []
entire_report = []
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
        entire_report.append(row_raw)
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
    race1 = prepare_race_data(races_with_info['Mayor - Oakland '], all_votes)
    print("3 - race1 from prepare_race_data", race1[:10])
    summed_round = sum_round(races_with_info['Mayor - Oakland '], race1)
    print("4 - summed_round from sum_round", summed_round[2:])
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

def prepare_race_data(race_from_races, all_votes):
    """Outputs list where each element is a ballot and each element in a ballot list represents a round (which indexes correspond with candidates)"""
    race_indexes = race_from_races[0]
    candidates = race_from_races[1]
    rounds_indexes = race_from_races[2]
    all_ballots = []
    for ind, whole_row in enumerate(all_votes):
        race_row = whole_row[race_indexes[0]: race_indexes[1] + 1]
        ballot = []
        if race_row.count("0") + race_row.count("1") > (len(candidates) * 5) - 3:
            for round_pair in rounds_indexes:
                ballot.append(race_row[round_pair[0]: round_pair[1] + 1])
            all_ballots.append(ballot)
    return all_ballots

def sum_round(race_from_races, race_votes, round_no = 0, categories = [], elimination_tracker =[]):
    """Outputs [race_from_races, ballot_tracker, round_no, categories, elimination_tracker, vote_tracker]"""
    race_indexes = race_from_races[0]
    candidates = race_from_races[1]
    if categories == []:
        categories = list(candidates) + ["Blanks", "Exhausted", "Overvote"]
    round_no += 1
    vote_tracker = []
    ballot_tracker = [] 
    if elimination_tracker == []:
        for cat in categories:
            elimination_tracker.append("I")
    for cat in categories:
        vote_tracker.append(0)
    ballot_no = 0
    for ballot in race_votes:
        ballot_no += 1
        blank_tracker = 0
        ballot_counted = False
        current_ballot = list(ballot)
        if ballot == ["BLANK"]:
            vote_tracker[-3] += 1
        elif ballot == ["EXHAUSTED"]:
            vote_tracker[-2] += 1
        elif ballot == ["OVERVOTE"]:
            vote_tracker[-1] += 1
        else:
            while ballot_counted == False:
                if current_ballot == []:
                    if blank_tracker == len(ballot):
                        vote_tracker[-3] += 1
                        ballot_tracker.append(["BLANK"])
                        ballot_counted = True
                    else:
                        vote_tracker[-2] += 1
                        ballot_tracker.append(["EXHAUSTED"])
                        ballot_counted = True
                elif current_ballot[0].count("1") > 1:
                    vote_tracker[-1] += 1
                    ballot_tracker.append(["OVERVOTE"])
                    ballot_counted = True
                elif current_ballot[0].count("1") == 0:
                    blank_tracker += 1
                    current_ballot = current_ballot[1:]
                else:
                    vote_index = current_ballot[0].index("1")
                    if elimination_tracker[vote_index] != "x":
                        vote_tracker[vote_index] += 1
                        ballot_tracker.append(current_ballot)
                        ballot_counted = True
    print(str(len(race_votes)) + " Ballots Entered. " + str(sum(vote_tracker)) + "Votes Counted.")
    return [race_from_races, ballot_tracker, round_no, categories, elimination_tracker, vote_tracker]


def round_elim([race_from_races, ballot_tracker, round_no, categories, elimination_tracker, vote_tracker]):
    sorted_vote_tracker = list(vote_tracker[:-3]).sort()
    lowest_count_ind = vote_tracker.find(sorted_vote_tracker[0])
    tb_eliminated = categories[lowest_count_ind]


run_code(race_line, candidate_line, all_votes)