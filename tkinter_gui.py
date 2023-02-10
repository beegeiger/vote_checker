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
root.geometry("600x600")
  
#Set root background color
root.config()

frame = Frame(root)
frame.pack(fill=BOTH, expand=True, padx=30, pady=25)


##########################################################################
#Tkinter to select input file

file_label = Label(frame, text="CVR Report File:", height =1)

file_label.pack(pady=0, side= TOP, anchor="w")

top = Frame(frame)
bottom = Frame(frame)
top.pack(side=TOP)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

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

button_exit = Button(frame,
                     text = "Exit",
                     command = exit)

button_exit.pack()


# Let the root wait for any events
root.mainloop()