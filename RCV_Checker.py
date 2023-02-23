import csv
import datetime
from tkinter import *

# import filedialog module
from tkinter import filedialog

race_line =[]
candidate_line =[]
all_votes = []
entire_report_import = []
#ballot_info = [[ballot_id1, precinct1, ballot_batch1], [ballot_id2, precinct2, ballot_batch2]]
ballot_info = []
all_races = []
all_precincts = []
all_batches = []
time_per_10000 = []
races_only = []

export_report = []
tkinter_file_input_name = ""

def clear_export_report():
    export_report = []
    return

def open_import_file(filename, sample_grouping = "None", file_grouping ="Together", output_file_name="RCV_Report", suspend_undervote="False"):
    update_root()
    time_tracker = datetime.datetime.now()
    global race_line
    global candidate_line
    global all_votes
    global entire_report_import
    global ballot_info
    global all_races
    global all_precincts
    global all_batches
    global time_per_10000
    start = datetime.datetime.now()
    print("STARTING AT DATETIME: ", start)
    print("Reading Input File and Compiling Data...")
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        start_index = 0
        for ind0, row_raw in enumerate(csv_reader):
            if line_count % 1000 == 0 and line_count > 0:
                if line_count < 9500:
                    print("Importing Data; Currently on ballot number: ", line_count)
                elif line_count % 10000 == 0:
                    time_taken =  datetime.datetime.now() - time_tracker
                    time_per_10000.append(time_taken)
                    print("Importing Data; Currently on ballot number: ", line_count, time_taken)
                    time_tracker = datetime.datetime.now()
            if ind0 == 0 and row_raw == [] or row_raw[:4] == ["","","","",""]:
                line_count -= 1
            if ind0 % 50 == 0:
                update_root()
            ind1 = ind0 - 1
            if line_count == 0:
                for ind2, element in enumerate(row_raw):
                    if element == "BallotType":
                        start_index = ind2 + 2
            row = row_raw[start_index:]
            entire_report_import.append(row_raw)
            if line_count == 0:
                race_line = row
            elif line_count == 1:
                candidate_line = row
            elif line_count > 2 and row_raw[7] != "TOTAL":
                ballot_id_split = row_raw[4].split("-")
                # print("BALLOT ID SPLIT: ", ballot_id_split, row_raw[4])
                batch = (ballot_id_split[0] + "-" + ballot_id_split[1])
                ballot_info.append([row_raw[4], row_raw[6], batch])
                if row_raw[4] not in all_races:
                    all_races.append(row_raw[4])
                if row_raw[6] not in all_precincts:
                    all_precincts.append(row_raw[6])
                if batch not in all_batches:
                    all_batches.append(batch)
                all_votes.append([[row_raw[4], row_raw[6], batch], row])
            line_count += 1
        all_precincts.sort()
        all_batches.sort()
    run_rcv_entire_report(race_line, candidate_line, all_votes, entire_report_import, sample_grouping, file_grouping, output_file_name, suspend_undervote)
    end = datetime.datetime.now()
    change = end-start
    all_cells = len(all_votes)*len(race_line)
    print("ENDING AT DATETIME: ", end)
    print("TOTAL TIME: ", change)
    print("TOTAL CELLS PROCESSED: ", all_cells)
    write_to_log(change, all_cells, len(all_votes), len(race_line), sample_grouping, file_grouping, suspend_undervote, filename, output_file_name, start, end)
    return

def write_to_log(total_time, total_cells, number_ballots, number_columns, sample_grouping, file_grouping, suspend_undervote, filename, output_file_name, start_time, end_time):
    global time_per_10000
    global races_only
    print("Writing Report Info to Log.")
    log = []
    with open("RCV_Checker_Log.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            if line != []:
                log.append(line)
    print("Imported Log: ", log)
    log.append(["Total Time", "Total Cells", "Number of Ballots", "Number of Columns", "Sample Grouping", "File Grouping", "Suspend Undervote?", "Input File Name", "output_file_name", "Start DateTime", "End DateTime", "Number of Races"])
    log.append([total_time, total_cells, number_ballots, number_columns, sample_grouping, file_grouping, suspend_undervote, filename, output_file_name, start_time, end_time, len(races_only)])
    log.append(["Time Taken Per 10,000 Votes Imported: "] + time_per_10000)
    log.append(["-","-","-","-","-","-","-","-","-","-","-","-"])
    print("LOG", log)
    with open("RCV_Checker_Log.csv", 'w', newline = '') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(log)
    return

def write_exported_file(export_report, output_file_name):
    with open(output_file_name + ".csv", 'w', newline='') as f:
      # using csv.writer method from CSV package
      write = csv.writer(f)
      write.writerows(export_report)
    return


input = [race_line, candidate_line, all_votes]

def run_rcv_entire_report(race_line, candidate_line, all_votes, entire_report_import, report_grouping = "None", file_grouping="Together", export_report_name="RCV_Report", suspend_undervote="False"):
    print("Race Data is being grouped and consolidated...")
    races_only1 = check_races(race_line)
    races_with_info = check_rounds(races_only1, candidate_line)
    for race in races_only1:
        update_root()
        if file_grouping == "Separate":
            clear_export_report()
        print("Current Race Being Processed: ", race)
        race_from_races = races_with_info[race]
        race_ballots = prepare_race_data(race_from_races, all_votes)
        if report_grouping == "None":
            run_rcv_for_one_race_sample(race_from_races, race_ballots, [race, "ALL", "ALL"], suspend_undervote)
        elif report_grouping == "Precinct":
            prepared_precinct_data = prepare_race_data_by_precinct(race_ballots, race)
            race_ballots_by_precinct = prepared_precinct_data[0]
            all_precinct_idents = prepared_precinct_data[1]
            for ident in all_precinct_idents:
            #     # print("RACE BALLOTS BY PRECINCT: ", rbp, race_ballots_by_precinct[rbp])
                run_rcv_for_one_race_sample(race_from_races, race_ballots_by_precinct[ident], ident, suspend_undervote)
        elif report_grouping == "Batch":
            prepared_batch_data = prepare_race_data_by_batch(race_ballots, race)
            race_ballots_by_batch = prepared_batch_data[0]
            all_batch_idents = prepared_batch_data[1]
            for iden in all_batch_idents:
                run_rcv_for_one_race_sample(race_from_races, race_ballots_by_batch[iden], iden, suspend_undervote)
        if file_grouping == "Separate":
            write_exported_file(export_report, export_report_name + " - " + race)
    if file_grouping == "Together":
        write_exported_file(export_report, export_report_name)
    print("THE ALGORITHM HAS CONCLUDED AND YOUR FILE IS NOW READY!")
    root.destroy()
    return export_report



def run_rcv_for_one_race_sample(race_from_races, race_ballots, sample_details_raw, suspend_undervote="False", qualified_write_in = "False"):
    if isinstance(sample_details_raw, str):
        sample_details = sample_details_raw.split("/")
    else:
        sample_details = sample_details_raw
    race_name = sample_details[0]
    precinct = sample_details[1]
    batch = sample_details[2]
    sample_report = []
    all_rounds_complete = False
    loop_no = 0
    summed_round = []
    post_elimination_round = []
    while all_rounds_complete == False:
        # print("RACE IN PROGRESS: ", race_from_races[-1])
        # print("RUN FOR ONE SAMPLE NEW LOOP: ", loop_no)
        # print("SUMMED ROUND BEFORE: ", summed_round[2:])
        if loop_no == 0:
            summed_round = sum_round(race_from_races, race_ballots, -1, [], [], suspend_undervote)
        else:
            summed_round = sum_round(race_from_races, post_elimination_round[0], loop_no, post_elimination_round[2], post_elimination_round[3], suspend_undervote)
        # print("SUMMED ROUND AFTER: ", summed_round[2:])
        if len(post_elimination_round) > 2 or loop_no == 10:
            if post_elimination_round[3][:-3].count("I") <= 2  or loop_no == 10:
                # print("TRIGGER 2")
                highest_vote_count = max(summed_round[5])
                highest_vote_index = summed_round[5].index(highest_vote_count)
                if suspend_undervote == "False":
                    export_report.append([race_name, precinct, batch, sum(summed_round[5]), loop_no] + summed_round[5] + ["","", loop_no] + post_elimination_round[3] + ["", sum(post_elimination_round[4]), loop_no] + post_elimination_round[4])
                else:
                    export_report.append([race_name, precinct, batch, sum(summed_round[5])  + summed_round[6][1], loop_no] + summed_round[5] + [summed_round[6][0], summed_round[6][1], "","", loop_no] + post_elimination_round[3] + ["", sum(post_elimination_round[4]) + post_elimination_round[5][0], loop_no] + post_elimination_round[4] + [post_elimination_round[5][0]])
                export_report.append(["", "", "", "WINNER: ", summed_round[3][highest_vote_index]])
                export_report.append([])
                all_rounds_complete = True
                # print("RUN FOR ONE SAMPLE completed.")
                break
        # print("POST ELIM ROUND BEFORE: ", post_elimination_round)
        if loop_no == 0 and suspend_undervote == "False":
            export_report.append(["Race","Precinct", "Batch", "Total Votes", "Round"] + summed_round[3] + ["", "Candidates Eliminated", "Round"] + summed_round[3] + ["", "Where Elimated Candidates Votes Go", "Round"] + summed_round[3])
        elif loop_no == 0:
            export_report.append(["Race","Precinct", "Batch", "Total Votes", "Round"] + summed_round[3] + ["New Suspended", "All Suspended"] + ["", "Candidates Eliminated", "Round"] + summed_round[3] + ["", "Where Elimated Candidates Votes Go", "Round"] + summed_round[3] + ["Suspended"])
        if loop_no == 0 and qualified_write_in == False:
            post_elimination_round = round_elim(summed_round[1], summed_round[2], summed_round[3], summed_round[4], summed_round[5], summed_round[6], True)
        else:
            post_elimination_round = round_elim(summed_round[1], summed_round[2], summed_round[3], summed_round[4], summed_round[5], summed_round[6])
        # print("POST ELIM ROUND AFTER: ", post_elimination_round[2:])
        if suspend_undervote == "False":
            export_report.append([race_name, precinct, batch, sum(summed_round[5]), loop_no] + summed_round[5] + ["","", loop_no] + post_elimination_round[3] + ["", sum(post_elimination_round[4]), loop_no] + post_elimination_round[4])
        else:
            export_report.append([race_name, precinct, batch, sum(summed_round[5]) + summed_round[6][1], loop_no] + summed_round[5] + [summed_round[6][0], summed_round[6][1], "","", loop_no] + post_elimination_round[3] + ["", sum(post_elimination_round[4]) + post_elimination_round[5][0], loop_no] + post_elimination_round[4] + [post_elimination_round[5][0]])
        # print("RUN FOR ONE SAMPLE Loop Ended: " , loop_no)
        loop_no += 1
    return




# def run_code(race_line, candidate_line, all_votes, entire_report_import, export_report):
#     races_only = check_races(race_line)
#     print("1 - races from check races: ", races_only)
#     races_with_info = check_rounds(races_only, candidate_line)
#     print("2 - races from check_rounds: ", races_with_info)
#     race1_ballots = prepare_race_data(races_with_info['Mayor - Oakland '], all_votes)
#     print("3 - race1 from prepare_race_data: ", race1_ballots[:10])
#     summed_round = sum_round(races_with_info['Mayor - Oakland '], race1_ballots)
#     print("4 - summed_round from sum_round: ", summed_round[2:])
#     post_elimination_round = round_elim(summed_round[1], summed_round[2], summed_round[3], summed_round[4], summed_round[5], True)
#     print("5 - round after elimination: ", post_elimination_round[1:])
#     summed_round1 = sum_round(races_with_info['Mayor - Oakland '], post_elimination_round[0], post_elimination_round[1], post_elimination_round[2], post_elimination_round[3])
#     print("6 - summed_round1 from sum_round: ", summed_round1[2:])
#     post_elimination_round1 = round_elim(summed_round1[1], summed_round1[2], summed_round1[3], summed_round1[4], summed_round1[5])
#     print("7 - round after elimination: ", post_elimination_round1[1:])
#     return

def check_races(race_line):
    """Outputs Dictionary where races["specific race"] = ["first index of race", "last index of race"] from race_line list"""
    global races_only
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
                races_only.append(race)
                start_index = ind
    return races



def check_rounds(races, candidate_line):
    """Outputs races = {"race1": [["first index of race", "last index of race"],[cand1, cand2, etc.],[[round1_start_ind, round1_end_ind], [round2_start_ind, round_2_end_ind], etc.], race_name]}"""
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
                races[race] = [races[race], candidate_list, race_round_tracker, race]
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
    for ind, whole_row_info in enumerate(all_votes):
        ballot_info = whole_row_info[0]
        whole_row = whole_row_info[1]
        race_row = whole_row[race_indexes[0]: race_indexes[1] + 1]
        ballot = []
        if race_row.count("0") + race_row.count("1") > (len(candidates) * 5) - 3:
            for round_pair in rounds_indexes:
                ballot.append(race_row[round_pair[0]: round_pair[1] + 1])
            all_ballots.append([ballot_info, ballot])
    return all_ballots

def prepare_race_data_by_precinct(all_ballots_from_race, race):
    print("Grouping Data By Precinct for Race: ", race)
    ballots_by_precinct = {}
    all_precinct_identifiers = []
    for whole_row_info in all_ballots_from_race:
        ballot_info = whole_row_info[0]
        whole_row = whole_row_info[1]
        identifier = str(race) + "/" + str(ballot_info[1]) + "/ALL"
        if identifier not in all_precinct_identifiers:
            all_precinct_identifiers.append(identifier)
        if identifier in ballots_by_precinct:
            ballots_by_precinct[identifier] = list(ballots_by_precinct[identifier]) + [whole_row_info]
        else:
            ballots_by_precinct[identifier] = [whole_row_info]
    all_precinct_identifiers.sort()
    return [ballots_by_precinct, all_precinct_identifiers]

def prepare_race_data_by_batch(all_ballots_from_race, race):
    print("Grouping Data By Batch for Race: ", race)
    ballots_by_batch = {}
    all_batch_identifiers = []
    for whole_row_info in all_ballots_from_race:
        ballot_info = whole_row_info[0]
        whole_row = whole_row_info[1]
        identifier = str(race) + "/ALL/" + str(ballot_info[2])
        if identifier not in all_batch_identifiers:
            all_batch_identifiers.append(identifier)
        if identifier in ballots_by_batch:
            ballots_by_batch[identifier] = list(ballots_by_batch[identifier]) + [whole_row_info]
        else:
            ballots_by_batch[identifier] = [whole_row_info]
    all_batch_identifiers.sort()
    return [ballots_by_batch, all_batch_identifiers]

def sum_round(race_from_races, race_votes, round_no = -1, categories = [], elimination_tracker =[], suspend_tracker="False"):
    """Outputs [race_from_races, ballot_tracker, round_no, categories, elimination_tracker, vote_tracker]"""
    suspended_tracker = ["False"]
    if suspend_tracker == "True":
        suspended_tracker = [0, 0]
    race_indexes = race_from_races[0]
    candidates = race_from_races[1]
    race_name = race_from_races[-1]
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
    for ballot_all in race_votes:
        if round_no >= 1:
            ballot = ballot_all
        else:
            ballot = ballot_all[1]
        ballot_no += 1
        blank_tracker = 0
        ballot_counted = False
        current_ballot = list(ballot)
        if ballot == ["BLANK"]:
            ballot_tracker.append(["BLANK"])
            vote_tracker[-3] += 1
        elif ballot == ["EXHAUSTED"]:
            ballot_tracker.append(["EXHAUSTED"])
            vote_tracker[-2] += 1
        elif ballot == ["OVERVOTE"]:
            ballot_tracker.append(["OVERVOTE"])
            vote_tracker[-1] += 1
        elif ballot == ["SUSPENDED"]:
            ballot_tracker.append(["SUSPENDED"])
            suspended_tracker[1] += 1
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
                    if suspended_tracker == ["False"]:
                        blank_tracker += 1
                        current_ballot = current_ballot[1:]
                    else:
                        ballot_tracker.append(["SUSPENDED"])
                        suspended_tracker[0] += 1
                        suspended_tracker[1] += 1
                        ballot_counted = True
                else:
                    vote_index = current_ballot[0].index("1")
                    if elimination_tracker[vote_index] != "x":
                        vote_tracker[vote_index] += 1
                        ballot_tracker.append(current_ballot)
                        ballot_counted = True
    # print("FROM SUM ROUND: ", str(len(race_votes)) + " Ballots Entered. " + str(len(ballot_tracker)) + "Votes Counted.")
    return [race_from_races, ballot_tracker, round_no, categories, elimination_tracker, vote_tracker, suspended_tracker]


def round_elim(ballot_tracker, round_no, categories, elimination_tracker, vote_tracker, suspended_tracker=["False"], round_0_no_write_in = False):
    if suspended_tracker != ["False"]:
        suspended_tracker = [0,0]
    elim_index = 0
    if round_0_no_write_in == False or round_no > 0:
        pre_elim_tracker = []
        for ind, val in enumerate(vote_tracker):
            if elimination_tracker[ind] == "x":
                pre_elim_tracker.append(9999999)
            else:
                pre_elim_tracker.append(val)
        sorted_vote_tracker = list(pre_elim_tracker[:-3])
        sorted_vote_tracker.sort()
        lowest_count_ind = pre_elim_tracker.index(sorted_vote_tracker[0])
        tb_eliminated = categories[lowest_count_ind]
        elimination_tracker[lowest_count_ind] = "x"
        elim_index = lowest_count_ind
        # print("TRIGGER A1, elim_after: ", elimination_tracker, elim_index, tb_eliminated)
    else:
        write_in_index = categories.index("Write-in")
        elimination_tracker[write_in_index] = "x"
        elim_index = write_in_index
    where_elim_go = []
    for n in categories:
        where_elim_go.append(0)
    new_ballot_tracker = []
    no_of_elimated_ballots = 0
    ballot_no = 0
    for ballot in ballot_tracker:
        # print("BALLOT: ", ballot, ballot_tracker)
        ballot_no += 1
        if ballot == ["EXHAUSTED"] or ballot == ["OVERVOTE"] or ballot == ["BLANK"] or ballot == ["SUSPENDED"]:
            new_ballot_tracker.append(ballot)
        elif ballot[0][elim_index] == "1" and ballot[0].count("1") == 1:
            current_ballot = ballot[1:]
            ballot_counted = False
            while ballot_counted == False:
                if current_ballot == []:
                    where_elim_go[-2] += 1
                    new_ballot_tracker.append(["EXHAUSTED"])
                    ballot_counted = True
                elif current_ballot[0].count("1") > 1:
                    where_elim_go[-1] += 1
                    new_ballot_tracker.append(["OVERVOTE"])
                    ballot_counted = True
                elif current_ballot[0].count("1") == 0:
                    if suspended_tracker == ["False"]:
                        current_ballot = current_ballot[1:]
                    else:
                        suspended_tracker[0] += 1
                        new_ballot_tracker.append(["SUSPENDED"])
                        ballot_counted = True
                else:
                    vote_index = current_ballot[0].index("1")
                    if elimination_tracker[vote_index] != "x":
                        where_elim_go[vote_index] += 1
                        new_ballot_tracker.append(current_ballot)
                        ballot_counted = True
                    else:
                        current_ballot = current_ballot[1:]
        else:
            new_ballot_tracker.append(ballot)
    # print("ROUND NO IN ROUND ELIM 2: ", round_no)
    # print("ROUND ELIM: ", str(len(ballot_tracker)) + " Ballots Entered. " + str(len(new_ballot_tracker)) + "Votes Counted.")
    return [new_ballot_tracker, round_no, categories, elimination_tracker, where_elim_go, suspended_tracker]









##########################################################################################
##########################################################################################
##########################################################################################






# Create the root window
root = Tk()

# Set root title
root.title('Python RCV Checker Parameters')

# Set root size
root.geometry("700x570")

#Set root background color
root.config()

frame = Frame(root)
frame.pack(fill=BOTH, expand=True, padx=30, pady=25)




input_file_input = ""
sample_grouping_input = ""
file_grouping_input = ""
output_file_input = ""
suspend_undervote = ""

##########################################################################
#Tkinter to select input file

file_label = Label(frame, text="CVR Report File:", height =1)
file_label.pack(pady=0, side= TOP, anchor="w")
top = Frame(frame)
top.pack(side=TOP)



def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "./",
                                          title = "Select a File",
                                          filetypes = (("CSV files",
                                                        "*.csv*"),
                                                      ("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Selected: " + filename, wraplength=325)
    global tkinter_file_input_name
    tkinter_file_input_name = filename
    return



# Create a File Explorer label
label_file_explorer = Label(frame,
                            text = "Select CVR Report to Process: ",
                            width = 50, height = 2,
                            fg = "blue")

button_explore = Button(frame,
                        text = "Browse Files",
                        command = browseFiles)

label_file_explorer.pack(in_=top, side=LEFT)
button_explore.pack(in_=top, side=LEFT)

########################################################################################
spacer = Label(frame, text="", height =1)
spacer.pack(pady=0, side= TOP, anchor="w")

########################################################################################
#Radio Buttons for Selecting Sample Type

sample_label = Label(frame, text="Select How Report Samples are Grouped:", height =2)
sample_label.pack(pady=0, side= TOP, anchor="w")
label_radios = Label(frame)


var = IntVar(None, 1)
R1 = Radiobutton(frame, text="By Race ONLY", variable=var, value=1)
R1.pack( anchor = W )

R2 = Radiobutton(frame, text="By Race and Precinct", variable=var, value=2
                  )
R2.pack( anchor = W )

R3 = Radiobutton(frame, text="By Race and Batch", variable=var, value=3)
R3.pack( anchor = W)

label_radios.pack()

##########################################################################################

save_type_label = Label(frame, text="How Would You Like the Report(s) generated?", height =2)
save_type_label.pack(pady=0, side= TOP, anchor="w")
save_label_radios = Label(frame)


var2 = IntVar(None, 4)
R4 = Radiobutton(frame, text="All Together in One .csv File", variable=var2, value=4)
R4.pack( anchor = W )

R5 = Radiobutton(frame, text="Separate .csv Files for All Races", variable=var2, value=5)
R5.pack( anchor = W )


save_label_radios.pack()
##########################################################################################

suspend_label = Label(frame, text="Should undervoted selections continue until they are exhausted or should they be suspended?", height =2)
suspend_label.pack(pady=0, side= TOP, anchor="w")
suspend_label_radios = Label(frame)


var3 = IntVar(None, 6)
R6 = Radiobutton(frame, text="Continue Ballot Upon Undervoted Column", variable=var3, value=6)
R6.pack( anchor = W )

R7 = Radiobutton(frame, text="Suspend Ballot (and the following columns will not count)", variable=var3, value=7)
R7.pack( anchor = W )


suspend_label_radios.pack()


##########################################################################################
save_name_label = Label(frame, text="What would you like to name your base report file? (optional)", height =2)
save_name_label.pack(pady=0, side= TOP, anchor="w")

input_txt = Entry(frame, width=50)
input_txt.insert(0, "RCV_Output_Report")
input_txt.pack()


##########################################################################################
def submit_input():
    global tkinter_file_input_name
    # print("VAR: ", var, var2, var.get(), var2.get())
    # print("INPUT FILE NAME: ", tkinter_file_input_name)
    input_file_input_raw = tkinter_file_input_name
    # input_raw_list = input_file_input_raw.split(":")
    # input_raw_list2 = input_raw_list[1].split("/")
    # input_file_input = input_raw_list2[-1]
    sample_grouping_input = ""
    file_grouping_input = ""
    suspend_undervote = ""
    if var.get() == 1:
       sample_grouping_input = "None"
    elif var.get() == 2:
       sample_grouping_input = "Precinct"
    elif var.get() == 3:
       sample_grouping_input = "Batch"
    if var2.get() == 4:
       file_grouping_input = "Together"
    elif var2.get() == 5:
       file_grouping_input = "Separate"
    if var3.get() == 6:
       suspend_undervote = "False"
    elif var3.get() == 7:
       suspend_undervote = "True"
    output_file_input = input_txt.get()
    # print("SUBMIT INPUT: ", input_file_input_raw, sample_grouping_input, file_grouping_input, output_file_input, suspend_undervote)
    new_processing_frame()
    run_alg_code(input_file_input_raw, sample_grouping_input, file_grouping_input, output_file_input, suspend_undervote)
    return


bottom = Frame(frame)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
button_exit = Button(frame,
                     text = "Exit",
                     command = exit)
button_exit.pack(in_=bottom, side=LEFT)

spacer2 = Label(frame, height =1, width=16)

spacer2.pack(in_=bottom, side=LEFT, anchor="w")

# button_README = Button(frame,
#                      text = "README File")
# button_README.pack(in_=bottom, side=LEFT)

button_run = Button(frame,
                     text = "Run Report",
                     command =submit_input)
button_run.pack(in_=bottom, side=RIGHT)
# Let the root wait for any events




def run_alg_code(import_report, sample_grouping = "None", file_grouping ="Together", output_file_name="RCV_Report", suspend_undervote = "False"):
    open_import_file(import_report, sample_grouping, file_grouping, output_file_name, suspend_undervote)
    return

def update_root():
    root.update()
    return

def destroy_root():
    root.destroy()
    root.update()
    return

frame2 = Frame(root)
processing_label = Label(frame2, text="The Report Is Being Run...\n This window will close automatically when the program is completed.", height =5, anchor="w")
processing_label.pack()
button_exit2 = Button(frame2,
                        text = "Exit Program Before Completion",
                        command =destroy_root)
button_exit2.pack()

def new_processing_frame():
    frame.destroy()
    frame2.pack(fill=BOTH, expand=True, padx=30, pady=25, side=TOP)
    root.update()
    # print("Frame should have been forgotten now.")
    return



root.mainloop()
