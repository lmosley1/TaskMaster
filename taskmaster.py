"""module providing GUI for the software"""
import tkinter
import tkinter.messagebox
import pickle
from pathlib import Path

root = tkinter.Tk()
root.title("TaskMaster")
# Makes the window unresizeable
root.resizable(0, 0)


def add_task():
    """Adds a task to the listbox from the entry widget"""
    task = task_entry.get()
    if len(task) > 100:
        tkinter.messagebox.showwarning(
            title="Error", message="The limit for tasks is 100 characters"
        )
    elif task != "":
        tasks_listbox.insert(tkinter.END, task)
        task_entry.delete(0, tkinter.END)
    else:
        # If the user hasn't entered a task, it shows a warning
        tkinter.messagebox.showwarning(title="Error", message="Enter a task first")


def delete_task():
    """Delets the selected task"""
    try:
        task_index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(task_index)
    except IndexError:
        # If the user hasn't selected a task before deleting, it shows a warning
        tkinter.messagebox.showwarning(title="Error", message="Select a task first")


def load_tasks():
    """Loads tasks that are saved in tasks.dat
    Deletes previous tasks in the listbox so it doesn't load on top of them
    """
    try:
        tasks = pickle.load(open("tasks.dat", "rb"))
        tasks_listbox.delete(0, tkinter.END)
        for task in tasks:
            tasks_listbox.insert(tkinter.END, task)
    except FileNotFoundError:
        # If a data file cannot be found in the directory
        # the user will be told to save a list
        tkinter.messagebox.showwarning(title="Error", message="Save a task list first")


def save_tasks():
    """Saves tasks to tasks.dat"""
    end_index = tasks_listbox.index("end")
    if end_index == 0:
        tkinter.messagebox.showwarning(title="Error", message="Enter some tasks first")
    else:
        tasks = tasks_listbox.get(0, tasks_listbox.size())
        pickle.dump(tasks, open("tasks.dat", "wb"))


# GUI

# Title label
title_label = tkinter.Label(root, text="TaskMaster")
title_label.pack()
title_label.config(font=("Helvetica", 30), foreground="lime")


# Creates a frame for the keybind labels
keybinds_frame = tkinter.Frame(root)
keybinds_frame.pack()

# Adds in labels which tell the user the keybinds for each button
add_label = tkinter.Label(keybinds_frame, text="Add task\nEnter")
add_label.pack(side=tkinter.LEFT, ipadx=25, ipady=5)
add_label.config(font=("Helvetica", 11))

delete_label = tkinter.Label(keybinds_frame, text="Delete task\nShift-Delete")
delete_label.pack(side=tkinter.LEFT, ipadx=25, ipady=5)
delete_label.config(font=("Helvetica", 11))

load_label = tkinter.Label(keybinds_frame, text="Load tasks\nCtrl-O")
load_label.pack(side=tkinter.LEFT, ipadx=25, ipady=5)
load_label.config(font=("Helvetica", 11))

save_label = tkinter.Label(keybinds_frame, text="Save tasks\nCtrl-S")
save_label.pack(side=tkinter.LEFT, ipadx=25, ipady=5)
save_label.config(font=("Helvetica", 11))


# Makes the frame for the buttons
buttons_frame = tkinter.Frame(root)
buttons_frame.pack()

# Adds the buttons to the GUI with their functions
add_icon = tkinter.PhotoImage(file="icons/icons8-add-24.png")
add_task_button = tkinter.Button(
    buttons_frame,
    image=add_icon,
    text="Add task",
    compound=tkinter.LEFT,
    command=add_task,
)
add_task_button.pack(side=tkinter.LEFT, ipadx=5, ipady=5)

delete_icon = tkinter.PhotoImage(file="icons/icons8-clear-symbol-24.png")
delete_task_button = tkinter.Button(
    buttons_frame,
    image=delete_icon,
    text="Delete task",
    compound=tkinter.LEFT,
    command=delete_task,
)
delete_task_button.pack(side=tkinter.LEFT, ipadx=5, ipady=5)

load_icon = tkinter.PhotoImage(file="icons/icons8-download-24.png")
load_tasks_button = tkinter.Button(
    buttons_frame,
    image=load_icon,
    text="Load tasks",
    compound=tkinter.LEFT,
    command=load_tasks,
)
load_tasks_button.pack(side=tkinter.LEFT, ipadx=5, ipady=5)

save_icon = tkinter.PhotoImage(file="icons/icons8-save-24.png")
save_tasks_button = tkinter.Button(
    buttons_frame,
    image=save_icon,
    text="Save tasks",
    compound=tkinter.LEFT,
    command=save_tasks,
)
save_tasks_button.pack(side=tkinter.LEFT, ipadx=5, ipady=5)


# Creates an entry box to input the task into
task_entry = tkinter.Entry(root, width=50)
task_entry.pack()

# Makes a frame to put the listbox and scrollbar together
tasks_frame = tkinter.Frame(root)
tasks_frame.pack()

tasks_listbox = tkinter.Listbox(tasks_frame, height=20, width=50)
tasks_listbox.pack(side=tkinter.LEFT)

tasks_scrollbar = tkinter.Scrollbar(tasks_frame)
tasks_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# Lets the listbox be controlled by the scrollbar
tasks_listbox.config(yscrollcommand=tasks_scrollbar.set)
tasks_scrollbar.config(command=tasks_listbox.yview)


# Binds the Enter key to the add a task
root.bind("<Return>", (lambda event: add_task()))

# Binds Shift-Backspace key to delete the selected task
root.bind("<Shift-BackSpace>", (lambda event: delete_task()))

# Binds Control-S to save the tasks
root.bind("<Control-s>", (lambda event: save_tasks()))

# Binds Control-O to load saved tasks
root.bind("<Control-o>", (lambda event: load_tasks()))


def on_closing():
    """Checks whether tasks.dat exists within the directory
    and if the window is closed without a saved task file
    it warns the user"""
    task_file = Path("tasks.dat")
    if task_file.is_file():
        root.destroy()
    elif tkinter.messagebox.askokcancel(
        "Quit", "You are about to quit without saving a task list"
    ):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()
