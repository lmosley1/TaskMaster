"""module providing GUI for the software"""
import tkinter
import tkinter.messagebox
import pickle

root = tkinter.Tk()
root.title("TaskMaster")
# Makes the window unresizeable
root.resizable(0, 0)


def add_task():
    """Adds a task to the listbox from the entry widget"""
    task = task_entry.get()
    if task != "":
        tasks_listbox.insert(tkinter.END, task)
        task_entry.delete(0, tkinter.END)
    else:
        tkinter.messagebox.showwarning(title="Error", message="Enter a task first")


def delete_task():
    """Delets the selected task"""
    try:
        task_index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(task_index)
    except IndexError:
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
        tkinter.messagebox.showwarning(title="Error", message="Save a task list first")


def save_tasks():
    """Saves tasks to tasks.dat"""
    tasks = tasks_listbox.get(0, tasks_listbox.size())
    pickle.dump(tasks, open("tasks.dat", "wb"))


# GUI

title_text = tkinter.Label(root, text="TaskMaster")
title_text.pack()
title_text.config(font=("Helvetica", 30), foreground="lime")

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

# Creates an entry box to input the task into
task_entry = tkinter.Entry(root, width=50)
task_entry.pack()


# Adds the buttons to the GUI with their functions
add_task_button = tkinter.Button(
    root,
    text="Add task",
    highlightbackground="black",
    fg="lime",
    width=48,
    command=add_task,
)
add_task_button.pack()

delete_task_button = tkinter.Button(
    root,
    text="Delete task",
    highlightbackground="black",
    fg="lime",
    width=48,
    command=delete_task,
)
delete_task_button.pack()

load_tasks_button = tkinter.Button(
    root,
    text="Load tasks",
    highlightbackground="black",
    fg="lime",
    width=48,
    command=load_tasks,
)
load_tasks_button.pack()

save_tasks_button = tkinter.Button(
    root,
    text="Save tasks",
    highlightbackground="black",
    fg="lime",
    width=48,
    command=save_tasks,
)
save_tasks_button.pack()


# Binds the Enter key to the add_task function
root.bind("<Return>", (lambda event: add_task()))

# Binds the Delete/Backspace key to the delete_task function
root.bind("<BackSpace>", (lambda event: delete_task()))

root.mainloop()
