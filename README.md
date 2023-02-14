# Automatic RCV VCR Results Generator

## Instructions For Use:
### 1. Prepare Your VCR Input File:
The VCR input file should be in the basic ".csv" filetype (you can save any spreadsheet as a .csv in any spreadsheet program). IT SHOULD BE SAVED IN THE SAME FOLDER as RCV_Checker.py and this README.md file.

The VCR spreadsheet should be consistent with VCR reports exported from a Dominion System:
-The first line should be blank. (what's in this doesn't matter)
-The second line should look as follows (cell separated by a ","):
[#,TabulatorNum,BatchId,RecordId,ImprintedId,CountingGroup,PrecinctPortion,BallotType,,]after these columns, each cell describes the associated race.
-The third line has 8 cells of "0" followed by a "TOTAL" cell, which is then followed by candidates, one candidate (for one round) in each cell. 
-The fourth line has 8 cells of "0" followed by a blank line. (what's in this doesn't matter)
-The fifth+ lines will each have the first 8 cells consistent with the data labels in the second line. After that, is how that ballot was voted...If the ballot doesn't include a race, the cells are blank. If the ballot DOES include a race, a "0" indicates a possible, but unvoted-option and a "1" indicates a filled in selection.

### 2. Open the VCR Checker Software (double-click RCV_Checker.py)
2a. If Python 3 isn't installed on your machine, the software won't open immediately. Instead, follow the prompts to have your operating system install Python. Once it is installed, then open the VCR Checker Software.

### 3. Using the "Browse Files" button, select the input .csv file.

### 4. Select how you would like your race data grouped:

