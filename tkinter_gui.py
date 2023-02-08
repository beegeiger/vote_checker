# Python program to create
# a file explorer in Tkinter
  
# import all components
# from the tkinter library
from tkinter import *
  
# import filedialog module
from tkinter import filedialog


# Create the root window
window = Tk()
  
# Set window title
window.title('Python RCV Checker Parameters')
  
# Set window size
window.geometry("500x500")
  
#Set window background color
window.config(background = "white")




##########################################################################
#Tkinter to select input file

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "./",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
      
      
                                                                                                  

  
# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "File Explorer using Tkinter",
                            width = 75, height = 6,
                            fg = "blue")


      
button_explore = Button(window,
                        text = "Browse Files",
                        command = browseFiles)
  



label_file_explorer.pack()
  
button_explore.pack()
  



label_file_explorer.pack()




########################################################################################
#Radio Buttons for Selecting Sample Type

label_radios = Label(window)

def sel():
   selection = "You selected the option " + str(var.get())
   label_radios.config(text = selection)

var = IntVar()

R1 = Radiobutton(window, text="By Race ONLY", variable=var, value=1,
                  command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(window, text="By Race and Precinct", variable=var, value=2,
                  command=sel)
R2.pack( anchor = W )

R3 = Radiobutton(window, text="By Race and Batch", variable=var, value=3,
                  command=sel)
R3.pack( anchor = W)

label_radios.pack()



##########################################################################################

button_exit = Button(window,
                     text = "Exit",
                     command = exit)

button_exit.pack()


# Let the window wait for any events
window.mainloop()