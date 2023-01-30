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

def check_races(input[0]):