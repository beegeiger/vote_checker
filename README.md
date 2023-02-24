# Automatic RCV VCR Results Generator
#### Small Python program that will accept a VCR (Vote Count Record) .csv report exported from the Dominion system. The program then runs the RCV algorithm (as set by the user) and then outputs the report(s) for all RCV races included in the report. This was designed as a way to 1. Quickly produce reports broken down by precinct in case a recount by precinct is called, 2. Quickly produce reports broken down by batch in case a recount by batch is called, 3. Quickly produce reports that can be used to double-check the original Dominion algorithm, and 4. Produce reports both overall and by precinct so that the RCV algorithm can be run in smaller samples, allowing campaigns and other political/social/educational entities to do focused studies of how different precincts voted. 

## Instructions For Use:
### 1. Download this repo, unzip the folder, and open it.

### 2. Prepare Your VCR Input File:
The VCR input file should be in the basic ".csv" filetype (you can save any spreadsheet as a .csv in any spreadsheet program).

The VCR spreadsheet should be consistent with VCR reports exported from a Dominion System:
-The first line can be blank and everthing below will be increased by one line...but this is entirely optional.
-Otherwisem, the first line should look as follows (cell separated by a ","):
[#,TabulatorNum,BatchId,RecordId,ImprintedId,CountingGroup,PrecinctPortion,BallotType,,]after these columns, each cell describes the associated race.
-The second line has 8 cells of "0" followed by a "TOTAL" cell, which is then followed by candidates, one candidate (for one round) in each cell. 
-The third line has 8 cells of "0" followed by a blank line. (what's in this doesn't matter)
-The fourth+ lines will each have the first 8 cells consistent with the data labels in the second line. After that, is how that ballot was voted...If the ballot doesn't include a race, the cells are blank. If the ballot DOES include a race, a "0" indicates a possible, but unvoted-option and a "1" indicates a filled in selection.

### 3. Open the VCR Checker Software (double-click RCV_Checker.py)
2a. If Python 3 isn't installed on your machine, the software won't open immediately. Instead, follow the prompts to have your operating system install Python. Once it is installed, then open the VCR Checker Software.

### 4. Using the "Browse Files" button, select the input .csv file.

### 5. Select how you would like your race data grouped:
#### By Race ONLY (Default):
Choosing this option will have the algorithm simply combine all voting data (ignoring precinct or batch) to calculate the overall race outcomes (for each race separately).
#### By Race and Precinct:
Choosing this option will have the algorithm not only group the data by race, but will further divide the data by precinct so the report will show the result of the algorithm as if it had been run separately for each precinct. 
#### By Race and Batch:
Choosing this option will have the algorithm not only group the data by race, but will further divide the data by batch so the report will show the result of the algorithm as if it had been run separately for each batch. 

### 6. Select how you would line your report(s) generated:
#### All Together in One .csv File:
Choosing this option will produce the output data altogether in one file.
#### Separate .csv Files for All Races:
Choosing this option will produce a separate .csv report file for each race with the name of each file being "[Your Ouput File Name] [Name of Race].csv"

### 7. Select how undervotes should be handled by the algorithm:
#### Continue Ballot Upon Undervoted Column:
If the first choice on a ballot is undervoted, but the race is not blank, the algorithm keeps moving onto the next column until it reaches a voted column and/or the ballot is exhausted.
#### Suspend Ballot (and the following columns will not count) - IN BETA:
If the first column is blank for a race, but the race is not blank, the ballot gets put in the "Suspended Ballot" and is not counted. Note: This feature is in beta doesn't appear to act exactly like the Dominion algorithm yet, so use with caution.

### 8. In the text box in the bottom of the window, enter the name you would like for your report being generated. The ".csv" part of the name will be added automatically. Note: if you choose the same name as a report already in your RCV checker folder, the original report will be over-written.

### 9. Click the "Run Report" Button
Once it begins, if you close out either window opened by the program, it will kill it and no report will be generated. If you let it run through, depending on the size of your sample, the program will take anywhere from 2 to 20 minutes to complete. Once it does complete, both windows will dissapear and your new report should be in RCV Checker folder where the python script is.





How the GUI should look:

![image](https://user-images.githubusercontent.com/36778471/221251358-c48a9893-d68a-4bad-96b1-985121fd8e13.png)
