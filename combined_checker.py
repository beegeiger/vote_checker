import csv
from tkinter import *
  
# import filedialog module
from tkinter import filedialog


# Create the root window
root = Tk()
  
# Set root title
root.title('Python RCV Checker Parameters')
  
# Set root size
root.geometry("600x520")
  
#Set root background color
root.config()

frame = Frame(root)
frame.pack(fill=BOTH, expand=True, padx=30, pady=25)


input_file_input = ""
sample_grouping_input = ""
file_grouping_input = ""
output_file_input = ""

##########################################################################
#Tkinter to select input file

file_label = Label(frame, text="CVR Report File:", height =1)
file_label.pack(pady=0, side= TOP, anchor="w")
top = Frame(frame)
top.pack(side=TOP)

tkinter_file_input_name = ""

def browseFiles():
    tkinter_file_input_name = filedialog.askopenfilename(initialdir = "./",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Selected: " + tkinter_file_input_name, wraplength=325)
    print("File Opened: ", tkinter_file_input_name)    
                                                                                                   
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

def sel():
   selection = "You selected the option " + str(var.get())
   print(selection)
   label_radios.config(text = selection)

var = IntVar()
R1 = Radiobutton(frame, text="By Race ONLY", variable=var, value="None",
                  command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(frame, text="By Race and Precinct", variable=var, value="Precinct",
                  command=sel)
R2.pack( anchor = W )

R3 = Radiobutton(frame, text="By Race and Batch", variable=var, value="Batch",
                  command=sel)
R3.pack( anchor = W)

label_radios.pack()

##########################################################################################

save_type_label = Label(frame, text="How Would You Like the Report(s) generated?", height =2)
save_type_label.pack(pady=0, side= TOP, anchor="w")
save_label_radios = Label(frame)

def sel_repo():
   selection = "You selected the option " + str(var.get())
   print(selection)
   save_label_radios.config(text = selection)

var2 = IntVar()
R4 = Radiobutton(frame, text="All Together in One .csv File", variable=var2, value=4,
                  command=sel)
R4.pack( anchor = W )

R5 = Radiobutton(frame, text="Separate .csv Files for All Races", variable=var2, value=5,
                  command=sel)
R5.pack( anchor = W )


save_label_radios.pack()

##########################################################################################
save_name_label = Label(frame, text="What would you like to name your base report file? (optional)", height =2)
save_name_label.pack(pady=0, side= TOP, anchor="w")

input_txt = Entry(frame, width=50)
input_txt.insert(0, "RCV_Output_Report")
input_txt.pack()


##########################################################################################
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

def submit_input():
   input_file_input = tkinter_file_input_name
   sample_grouping_input = str(var.get())
   file_grouping_input = str(var2.get())
   output_file_input = input_txt.get()
   print("SUBMIT INPUT: ", input_file_input, sample_grouping_input, file_grouping_input, output_file_input)
   return



root.mainloop()



##########################################################################################
##########################################################################################
##########################################################################################

race_line =[]
candidate_line =[]
all_votes = []
entire_report_import = []
#ballot_info = [[ballot_id1, precinct1, ballot_batch1], [ballot_id2, precinct2, ballot_batch2]]
ballot_info = []
all_races = []
all_precincts = []
all_batches = []

export_report = []

def open_import_file(filename):
   with open(filename) as csv_file:
       csv_reader = csv.reader(csv_file, delimiter=',')
       line_count = 0
       start_index = 0
       for ind1, row_raw in enumerate(csv_reader):
           if ind1 == 0:
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
   return

def write_exported_file(export_report):
with open(output_file_name, 'w') as f:
   # using csv.writer method from CSV package
   write = csv.writer(f)
   write.writerows(export_report)
   return   


input = [race_line, candidate_line, all_votes]

def run_rcv_entire_report(race_line, candidate_line, all_votes, entire_report_import, export_report, report_grouping = "None"):
    races_only = check_races(race_line)
    races_with_info = check_rounds(races_only, candidate_line)
    for race in races_only:  
        print("NEW RACE FROM RUN ENTIRE REPORT: ", race)
        race_from_races = races_with_info[race]
        race_ballots = prepare_race_data(race_from_races, all_votes)
        if report_grouping == "None":
            run_rcv_for_one_race_sample(race_from_races, race_ballots, [race, "ALL", "ALL"])
        elif report_grouping == "Precinct":
            prepared_precinct_data = prepare_race_data_by_precinct(race_ballots, race)
            race_ballots_by_precinct = prepared_precinct_data[0]
            all_precinct_idents = prepared_precinct_data[1]
            for ident in all_precinct_idents:
            #     # print("RACE BALLOTS BY PRECINCT: ", rbp, race_ballots_by_precinct[rbp])
                run_rcv_for_one_race_sample(race_from_races, race_ballots_by_precinct[ident], ident)
        elif report_grouping == "Batch":
            race_ballots_by_batch = prepare_race_data_by_batch(race_ballots, race)
            for rbb in race_ballots_by_batch:
                run_rcv_for_one_race_sample(race_from_races, race_ballots_by_batch[rbb], rbb)

    return export_report



def run_rcv_for_one_race_sample(race_from_races, race_ballots, sample_details_raw, qualified_write_in = False):
    if isinstance(sample_details_raw, str):
        sample_details = sample_details_raw.split("/")
        print("RUNNING RCV FOR SAMPLE:", sample_details)
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
            summed_round = sum_round(race_from_races, race_ballots, -1, [], [])
        else:
            summed_round = sum_round(race_from_races, post_elimination_round[0], loop_no, post_elimination_round[2], post_elimination_round[3])
        # print("SUMMED ROUND AFTER: ", summed_round[2:])
        if len(post_elimination_round) > 2 or loop_no == 10:
            if post_elimination_round[3][:-3].count("I") <= 2  or loop_no == 10:
                # print("TRIGGER 2")
                highest_vote_count = max(summed_round[5])
                highest_vote_index = summed_round[5].index(highest_vote_count)
                export_report.append([race_name, precinct, batch, sum(summed_round[5]), loop_no] + summed_round[5] + ["","", loop_no] + post_elimination_round[3] + ["", sum(post_elimination_round[4]), loop_no] + post_elimination_round[4])
                export_report.append(["", "", "", "WINNER: ", summed_round[3][highest_vote_index]])
                export_report.append([])
                all_rounds_complete = True
                # print("RUN FOR ONE SAMPLE completed.")
                break
        # print("POST ELIM ROUND BEFORE: ", post_elimination_round)        
        if loop_no == 0:
            export_report.append(["Race","Precinct", "Batch", "Total Votes", "Round"] + summed_round[3] + ["", "Candidates Eliminated", "Round"] + summed_round[3] + ["", "Where Elimated Candidates Votes Go", "Round"] + summed_round[3])
        if loop_no == 0 and qualified_write_in == False:
            post_elimination_round = round_elim(summed_round[1], summed_round[2], summed_round[3], summed_round[4], summed_round[5], True)
        else:
            post_elimination_round = round_elim(summed_round[1], summed_round[2], summed_round[3], summed_round[4], summed_round[5])
        # print("POST ELIM ROUND AFTER: ", post_elimination_round[2:])  
        export_report.append([race_name, precinct, batch, sum(summed_round[5]), loop_no] + summed_round[5] + ["","", loop_no] + post_elimination_round[3] + ["", sum(post_elimination_round[4]), loop_no] + post_elimination_round[4])
        # print("RUN FOR ONE SAMPLE Loop Ended: " , loop_no)
        loop_no += 1
        
    return sample_report




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
    ballots_by_batch = {}
    all_batch_identifiers = []
    for whole_row_info in all_ballots_from_race:
        ballot_info = whole_row_info[0]
        whole_row = whole_row_info[1]
        identifier = str(race) + "/ALL/" + str(ballot_info[2])
        if identifier not in all_precinct_identifiers:
            all_batch_identifiers.append(identifier)
        if identifier in ballots_by_batch:
            ballots_by_batch[identifier] = list(ballots_by_batch[identifier]) + [whole_row_info]
        else:
            ballots_by_batch[identifier] = [whole_row_info]
    all_batch_identifiers.sort()
    return [ballots_by_batch, all_batch_identifiers]

def sum_round(race_from_races, race_votes, round_no = -1, categories = [], elimination_tracker =[]):
    """Outputs [race_from_races, ballot_tracker, round_no, categories, elimination_tracker, vote_tracker]"""
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
    # print(str(len(race_votes)) + " Ballots Entered. " + str(sum(vote_tracker)) + "Votes Counted.")
    return [race_from_races, ballot_tracker, round_no, categories, elimination_tracker, vote_tracker]


def round_elim(ballot_tracker, round_no, categories, elimination_tracker, vote_tracker, round_0_no_write_in = False):
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
        if ballot == ["EXHAUSTED"] or ballot == ["OVERVOTE"] or ballot == ["BLANK"]:
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
                    current_ballot = current_ballot[1:]
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
    return [new_ballot_tracker, round_no, categories, elimination_tracker, where_elim_go]

def run_code(import_report, sample_grouping = "None", file_grouping ="None", output_file_name="RCV_Report"):
    open_import_file(import_report)
    run_rcv_entire_report(race_line, candidate_line, all_votes, entire_report_import, export_report)
    return

run_code(race_line, candidate_line, all_votes, entire_report_import, export_report)

output_file_name = "RCV_Report"






##########################################################################################
##########################################################################################
##########################################################################################