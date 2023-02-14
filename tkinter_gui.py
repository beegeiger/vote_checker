# Python program to create
# a file explorer in Tkinter
  
# import all components
# from the tkinter library
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


##########################################################################
#Tkinter to select input file

file_label = Label(frame, text="CVR Report File:", height =1)
file_label.pack(pady=0, side= TOP, anchor="w")
top = Frame(frame)
top.pack(side=TOP)

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "./",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Selected: " + filename, wraplength=325)
    print("File Opened: ", filename)    
                                                                                                   
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
R1 = Radiobutton(frame, text="By Race ONLY", variable=var, value=1,
                  command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(frame, text="By Race and Precinct", variable=var, value=2,
                  command=sel)
R2.pack( anchor = W )

R3 = Radiobutton(frame, text="By Race and Batch", variable=var, value=3,
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

button_README = Button(frame,
                     text = "README File")
button_README.pack(in_=bottom, side=LEFT)

button_run = Button(frame,
                     text = "Run Report",
                     command = exit)
button_run.pack(in_=bottom, side=RIGHT)
# Let the root wait for any events
root.mainloop()